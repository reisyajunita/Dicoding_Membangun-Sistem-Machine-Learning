import time
import pandas as pd
import numpy as np
import mlflow.sklearn
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, make_wsgi_app, generate_latest
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os 

# --- 1. Inisialisasi Aplikasi Flask ---
app = Flask(__name__)

# --- 2. Load Model ---
model = None
MODEL_PATH = "./model_artifact/tuned-churn-model-dagshub"
try:
    # Periksa apakah path model ada dan bisa diakses
    if os.path.exists(MODEL_PATH):
        model = mlflow.sklearn.load_model(MODEL_PATH)
        print(f"[INFO] Model berhasil dimuat dari {MODEL_PATH}.")
    else:
        print(f"[ERROR] Path model tidak ditemukan: {MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Gagal memuat model: {e}")

# --- 3. Definisikan 10 Metrik Lengkap Anda ---
PREDICTION_REQUESTS = Counter('prediction_requests_total', 'Total prediction requests received')
PREDICTION_COUNT = Counter('prediction_class_count', 'Count of predictions per class', ['class_name'])
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Latency of prediction requests in seconds')
PREDICTION_FAILURES = Gauge('prediction_failures_total', 'Total prediction requests that failed')
AVG_CHURN_PROBABILITY = Gauge('average_churn_probability', 'Average probability of churn prediction')
TENURE_DISTRIBUTION = Histogram('input_feature_tenure_distribution', 'Distribution of tenure feature in requests')
MONTHLY_CHARGES_DISTRIBUTION = Histogram('input_feature_monthlycharges_distribution', 'Distribution of MonthlyCharges feature in requests')
TOTAL_CHARGES_DISTRIBUTION = Histogram('input_feature_totalcharges_distribution', 'Distribution of TotalCharges feature in requests')
CONTRACT_TYPE_COUNT = Counter('input_feature_contract_type_count', 'Count of contract types in requests', ['contract'])
LAST_SUCCESSFUL_PREDICTION_TIME = Gauge('last_successful_prediction_timestamp_seconds', 'Timestamp of the last successful prediction')

# --- 4. Logika Endpoint Prediksi ---
final_columns = [
    'tenure', 'MonthlyCharges', 'TotalCharges', 'gender_Male',
    'SeniorCitizen_Yes', 'Partner_Yes', 'Dependents_Yes',
    'PhoneService_Yes', 'MultipleLines_No phone service',
    'MultipleLines_Yes', 'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        PREDICTION_FAILURES.inc()
        print("[ERROR] Predict request received but model is not loaded.")
        return jsonify({"error": "Model not loaded"}), 500

    start_time = time.time()
    PREDICTION_REQUESTS.inc() # Increment total requests saat request diterima

    try:
        raw_data = request.json
        
        # --- PERBAIKAN PENTING DI SINI UNTUK PENANGANAN DATAFRAME PANDAS ---
        if isinstance(raw_data, dict):
            # Jika input adalah single dictionary (misal: {"feature1": val}), bungkus dengan list
            df_raw = pd.DataFrame([raw_data])
        elif isinstance(raw_data, list):
            # Jika input sudah berupa list of dictionaries (misal: [{"feature1": val}]), gunakan langsung
            df_raw = pd.DataFrame(raw_data)
        else:
            # Jika format tidak dikenali
            raise ValueError("Input data must be a dictionary or a list of dictionaries.")
        
        # --- DEBUGGING PRINTS (HAPUS SETELAH BERHASIL) ---
        print(f"DEBUG IN SERVER: Tipe raw_data setelah konversi: {type(df_raw)}")
        print(f"DEBUG IN SERVER: df_raw.head():\n{df_raw.head()}")
        print(f"DEBUG IN SERVER: df_raw.shape: {df_raw.shape}")
        # --- END DEBUGGING PRINTS ---

        # Logging metrik distribusi fitur input
        for feature, metric_hist in [
            ('tenure', TENURE_DISTRIBUTION),
            ('MonthlyCharges', MONTHLY_CHARGES_DISTRIBUTION)
        ]:
            if feature in df_raw and not df_raw[feature].empty:
                for val in df_raw[feature]:
                    try:
                        metric_hist.observe(float(val))
                    except (ValueError, TypeError):
                        print(f"[WARNING] Skipping non-numeric value for {feature}: {val}")

        if 'TotalCharges' in df_raw and not df_raw['TotalCharges'].empty:
            total_charges_numeric = pd.to_numeric(df_raw['TotalCharges'], errors='coerce').dropna()
            if not total_charges_numeric.empty:
                for tc in total_charges_numeric: TOTAL_CHARGES_DISTRIBUTION.observe(tc)
            else:
                print("[WARNING] 'TotalCharges' column is empty after conversion.")

        if 'Contract' in df_raw and not df_raw['Contract'].empty:
            for c in df_raw['Contract']:
                # Pastikan label contract diinc() jika ada nilainya
                CONTRACT_TYPE_COUNT.labels(contract=c).inc()

        # Preprocessing data untuk prediksi
        df_encoded = pd.get_dummies(df_raw).astype(float)
        df_final = df_encoded.reindex(columns=final_columns, fill_value=0)
        
        # Prediksi
        predictions = model.predict(df_final)
        
        # Probabilitas Churn
        try:
            probabilities = model.predict_proba(df_final)
            # Ambil probabilitas untuk kelas '1' (Churn)
            churn_probabilities = probabilities[:, 1] 
            # Set rata-rata probabilitas churn untuk semua prediksi dalam batch
            AVG_CHURN_PROBABILITY.set(np.mean(churn_probabilities)) 
        except Exception as prob_e:
            print(f"[WARNING] Gagal menghitung probabilitas: {prob_e}. Menggunakan default 0.")
            churn_probabilities = [0.0] * len(predictions)
            AVG_CHURN_PROBABILITY.set(0)

        # Increment PREDICTION_COUNT per class
        for pred_val in predictions:
            class_name = 'Churn' if int(pred_val) == 1 else 'No_Churn'
            PREDICTION_COUNT.labels(class_name=class_name).inc()
        
        latency = time.time() - start_time
        PREDICTION_LATENCY.observe(latency)
        
        LAST_SUCCESSFUL_PREDICTION_TIME.set(time.time()) # Set timestamp saat ini

        response = {
            'predictions': predictions.tolist(),
            'probabilities_churn': churn_probabilities.tolist()
        }
        
        return jsonify(response)

    except Exception as e:
        PREDICTION_FAILURES.inc() # Increment kegagalan
        print(f"[ERROR] Prediksi gagal karena: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/')
def home():
    return "Churn Prediction Model Serving App. Gunakan endpoint /predict untuk prediksi."

# --- 5. Sajikan Aplikasi dan Metrik dengan cara paling sederhana ---
dispatcher = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app() 
})