# Gunakan base image Python yang ringan
FROM python:3.10-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu untuk caching layer
COPY requirements.txt .

# Install semua dependensi, termasuk waitress
RUN pip install --no-cache-dir -r requirements.txt

# Salin skrip aplikasi dan folder model Anda
COPY ./prometheus_exporter.py .
COPY ./tuned-churn-model-dagshub/ ./model_artifact/

# Jalankan dengan waitress, server yang sederhana dan single-process
# Ini menghindari semua kerumitan multi-worker dari Gunicorn
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5001", "prometheus_exporter:dispatcher"]
