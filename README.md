# Proyek Machine Learning: Prediksi Churn Pelanggan Telco

Proyek ini dibuat sebagai submission untuk kelas **"Membangun Sistem Machine Learning"** dari [Dicoding Indonesia](https://www.dicoding.com/).

Tujuan utama dari proyek ini adalah untuk membangun dan mengevaluasi model machine learning yang dapat memprediksi *churn* (berhentinya pelanggan) pada perusahaan telekomunikasi. Proyek ini mencakup seluruh siklus hidup machine learning, mulai dari eksperimen, *hyperparameter tuning*, hingga *serving* dan *monitoring* model.

## 📊 Dataset

Dataset yang digunakan adalah **"Telco Customer Churn"** yang telah melalui tahap pra-pemrosesan (`dataset_processed.csv`). Fitur-fitur dalam dataset ini mencakup informasi demografis pelanggan, layanan yang mereka gunakan, dan status *churn* mereka.

## ⚙️ Alur Kerja & Metodologi

Proyek ini dibagi menjadi beberapa tahap utama:

### 1. Eksperimen dan Pemodelan
* **Eksperimen Awal (`modeling.py`):**
    * Melakukan eksperimen dasar menggunakan **Logistic Regression**.
    * Menggunakan **MLflow Autologging** untuk secara otomatis mencatat parameter, metrik (akurasi, presisi, recall, F1-score), dan model yang dihasilkan dari setiap *run*.
* **Eksperimen Lanjutan dengan Tuning (`modeling_tuning.py`):**
    * Menerapkan *hyperparameter tuning* menggunakan **GridSearchCV** pada model seperti **Logistic Regression** dan **Random Forest**.
    * Mengintegrasikan eksperimen dengan **DagsHub** untuk versioning data dan tracking eksperimen yang lebih terpusat.
    * Menyimpan artefak penting seperti plot evaluasi (*confusion matrix*) dan model terbaik dari setiap eksperimen.

### 2. Monitoring dan Logging
Bagian ini berfokus pada deployment dan pemantauan model di lingkungan produksi.
* **Model Serving:** Model *churn* yang telah dilatih di-*serve* sebagai sebuah service, siap menerima request untuk prediksi.
* **Monitoring dengan Prometheus & Grafana:**
    * **Prometheus** digunakan untuk mengumpulkan metrik performa dari model yang sedang berjalan (misalnya, jumlah request, latensi, probabilitas *churn* rata-rata).
    * **Grafana** digunakan untuk memvisualisasikan metrik dari Prometheus ke dalam dashboard yang interaktif, memungkinkan pemantauan secara *real-time*.
* **Alerting:** Aturan peringatan (*alerting rules*) dikonfigurasi di Grafana untuk memberikan notifikasi jika terjadi anomali, seperti penurunan performa model atau lonjakan *failure rate*.

## 🚀 Instalasi & Penggunaan

Untuk menjalankan bagian eksperimen dari proyek ini:

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/reisyajunita/Dicoding_Membangun-Sistem-Machine-Learning.git](https://github.com/reisyajunita/Dicoding_Membangun-Sistem-Machine-Learning.git)
    ```

2.  **Instal Dependensi:**
    Disarankan untuk membuat *virtual environment*.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Jalankan Eksperimen:**
    * Untuk eksperimen dasar:
        ```bash
        python modeling.py
        ```
    * Untuk eksperimen dengan tuning (pastikan DagsHub sudah terkonfigurasi):
        ```bash
        python modeling_tuning.py
        ```

4.  **Lihat Hasil Eksperimen:**
    Jalankan MLflow UI untuk melihat perbandingan antar *run*.
    ```bash
    mlflow ui
    ```

*Catatan: Untuk menjalankan bagian monitoring, diperlukan pengaturan tambahan menggunakan Docker, Prometheus, dan Grafana sesuai dengan file konfigurasi (`docker-compose.yml`, `prometheus.yml`).*

## 🧑‍💻 Author

* **Nama:** Reisya Junita
* **GitHub:** [@reisyajunita](https://github.com/reisyajunita)
