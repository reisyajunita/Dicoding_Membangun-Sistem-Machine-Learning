import requests
import json
import pandas as pd
import random
import time

# URL dari aplikasi serving modelmu
API_URL = "http://localhost:5001/predict"

def create_sample_data(num_samples=1):
    """Membuat beberapa contoh data pelanggan acak untuk inferensi."""
    data = []
    for _ in range(num_samples):
        sample = {
            "gender": random.choice(["Male", "Female"]),
            "SeniorCitizen": "No", # Diubah menjadi string 'No' atau 'Yes'
            "Partner": random.choice(["Yes", "No"]),
            "Dependents": random.choice(["Yes", "No"]),
            "tenure": random.randint(1, 72),
            "PhoneService": random.choice(["Yes", "No"]),
            "MultipleLines": random.choice(["Yes", "No", "No phone service"]),
            "InternetService": random.choice(["DSL", "Fiber optic", "No"]),
            "OnlineSecurity": random.choice(["Yes", "No", "No internet service"]),
            "OnlineBackup": random.choice(["Yes", "No", "No internet service"]),
            "DeviceProtection": random.choice(["Yes", "No", "No internet service"]),
            "TechSupport": random.choice(["Yes", "No", "No internet service"]),
            "StreamingTV": random.choice(["Yes", "No", "No internet service"]),
            "StreamingMovies": random.choice(["Yes", "No", "No internet service"]),
            
            # --- TAMBAHKAN BARIS INI ---
            "Contract": random.choice(["Month-to-month", "One year", "Two year"]),
            
            "PaperlessBilling": random.choice(["Yes", "No"]),
            "PaymentMethod": random.choice(["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]),
            "MonthlyCharges": round(random.uniform(18.0, 118.0), 2),
            "TotalCharges": round(random.uniform(20.0, 8000.0), 2)
        }
        data.append(sample)
    
    return data

def send_request(data):
    headers = {"Content-Type": "application/json"}
    try:
        # Mengirim data sebagai JSON array
        response = requests.post(API_URL, json=data)
        response.raise_for_status() 
        
        print(f"Request berhasil dikirim ke {API_URL}")
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(response.json())
        
    except requests.exceptions.RequestException as e:
        print(f"Request GAGAL: {e}")
        # Jika server mengembalikan respons error (seperti 400), cetak juga isinya
        if e.response is not None:
            print("Server Response:")
            try:
                print(e.response.json())
            except json.JSONDecodeError:
                print(e.response.text)

if __name__ == "__main__":
    print("--- Membuat dan Mengirim Data Contoh untuk Prediksi Churn ---")
    
    # Buat satu data contoh
    sample_customer = create_sample_data(num_samples=1)
    
    print("Data yang akan dikirim:")
    print(json.dumps(sample_customer, indent=2))
    print("-" * 50)
    
    # Kirim request ke API
    send_request(sample_customer)