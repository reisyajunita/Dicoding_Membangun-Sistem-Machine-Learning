import os
import mlflow

# --- KONFIGURASI ---
DAGSHUB_TOKEN = "c50480f790b1b255db0035e85eeba29b5f6ced11" 

# Set environment variables untuk otentikasi ke DagsHub
os.environ['MLFLOW_TRACKING_URI'] = "https://dagshub.com/reisyajunita/membangun_model.mlflow"
os.environ['MLFLOW_TRACKING_USERNAME'] = "reisyajunita"
os.environ['MLFLOW_TRACKING_PASSWORD'] = DAGSHUB_TOKEN

# URI dari model yang ingin diunduh
model_uri = "runs:/95b0f2b6e89a433d9081f56ef8e99a98/tuned-churn-model-dagshub"

# Path tujuan di komputer lokal Anda
output_path = "./tuned-churn-model-dagshub"

print(f"Mencoba mengunduh artefak dari URI:\n{model_uri}")
print(f"Akan disimpan di folder: {output_path}")

try:
    # Perintah inti untuk mengunduh artefak
    mlflow.artifacts.download_artifacts(
        artifact_uri=model_uri,
        dst_path=output_path
    )
    print("\n--- BERHASIL! ---")
    print(f"Folder model telah berhasil diunduh ke '{output_path}'")

except Exception as e:
    print("\n--- GAGAL! Terjadi error saat mengunduh: ---")
    print(e)
    print("\nPastikan token DagsHub Anda sudah benar dan valid.")