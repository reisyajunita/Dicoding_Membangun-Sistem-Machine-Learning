# Proyek Machine Learning: Prediksi Churn Pelanggan Telco

Proyek ini dibuat sebagai submission untuk kelas **"Belajar Membangun Sistem Machine Learning"** dari [Dicoding Indonesia](https://www.dicoding.com/).

Tujuan utama dari proyek ini adalah untuk membangun dan mengevaluasi model machine learning yang dapat memprediksi *churn* (berhentinya pelanggan) pada perusahaan telekomunikasi. Proyek ini mencakup seluruh siklus hidup machine learning (MLOps), mulai dari **eksperimen data**, **otomatisasi preprocessing**, **pelacakan eksperimen**, *hyperparameter tuning*, hingga *serving* dan *monitoring* model di lingkungan produksi.

## ⚙️ Alur Kerja & Metodologi

Proyek ini dibagi menjadi beberapa tahap utama yang saling berkesinambungan:

### Tahap 1: Analisis dan Otomatisasi Preprocessing
Bagian ini berfokus pada persiapan data sebelum pemodelan.
* **Analisis Data Eksplorasi (EDA):** Memahami karakteristik dan pola dalam dataset mentah `telco_dataset.csv`.
* **Pipeline Preprocessing:** Mengembangkan langkah-langkah untuk membersihkan data, menangani nilai yang hilang, melakukan *encoding* pada fitur kategorikal, dan *scaling* pada fitur numerik.
* **Otomatisasi dengan GitHub Actions:** Sebuah *workflow* CI/CD diimplementasikan untuk menjalankan skrip preprocessing (`automate_Reisya-Junita.py`) secara otomatis setiap kali ada perubahan pada data mentah atau skrip itu sendiri. Hasilnya, `dataset_processed.csv`, akan selalu diperbarui.

### Tahap 2: Eksperimen dan Pelacakan Model
Setelah data siap, tahap ini berfokus pada pembangunan model.
* **Eksperimen Awal (`modeling.py`):** Melakukan eksperimen dasar menggunakan **Logistic Regression** dan melacak hasilnya (parameter, metrik, dan artefak) secara lokal dengan **MLflow**.
* **Eksperimen Lanjutan & Tuning (`modeling_tuning.py`):** Menerapkan *hyperparameter tuning* menggunakan **GridSearchCV** pada model **Logistic Regression** dan **Random Forest**. Eksperimen ini dilacak dan di-versioning secara terpusat menggunakan **DagsHub**.

### Tahap 3: Monitoring dan Logging
Bagian ini berfokus pada deployment dan pemantauan model di lingkungan produksi.
* **Model Serving:** Model *churn* terbaik di-*serve* sebagai sebuah service, siap menerima request untuk prediksi secara *real-time*.
* **Monitoring dengan Prometheus & Grafana:**
    * **Prometheus** digunakan untuk mengumpulkan metrik performa dari model yang sedang berjalan (misalnya, jumlah request, latensi, probabilitas *churn* rata-rata).
    * **Grafana** digunakan untuk memvisualisasikan metrik dari Prometheus ke dalam dashboard yang interaktif.
* **Alerting:** Aturan peringatan dikonfigurasi di Grafana untuk memberikan notifikasi jika terjadi anomali, seperti penurunan performa model atau lonjakan *failure rate*.

## 🚀 Instalasi & Penggunaan

Untuk menjalankan bagian-bagian dari proyek ini:

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/reisyajunita/Dicoding_Membangun-Sistem-Machine-Learning.git](https://github.com/reisyajunita/Dicoding_Membangun-Sistem-Machine-Learning.git)
    cd Dicoding_Membangun-Sistem-Machine-Learning
    ```
2.  **Instal Dependensi:**
    Disarankan untuk membuat *virtual environment*.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Jalankan Eksperimen Pemodelan:**
    * Untuk eksperimen dasar dengan MLflow lokal:
        ```bash
        python modeling.py
        ```
    * Untuk eksperimen dengan tuning dan DagsHub (pastikan DagsHub sudah terkonfigurasi):
        ```bash
        python modeling_tuning.py
        ```
    * Lihat hasil eksperimen dengan menjalankan MLflow UI:
        ```bash
        mlflow ui
        ```

*Catatan: Untuk menjalankan bagian **Otomatisasi Preprocessing** dan **Monitoring**, diperlukan penyesuaian path dan pengaturan tambahan sesuai dengan struktur folder masing-masing, serta instalasi Docker untuk Prometheus & Grafana.*

## 📂 Struktur Proyek (Ringkasan)

* **.github/workflows/main.yml**: Konfigurasi GitHub Actions untuk otomatisasi preprocessing.
* **membangun_model/**: Berisi skrip untuk eksperimen, tuning, dan pelacakan model dengan MLflow & DagsHub.
* **Monitoring_dan_Logging/**: Berisi konfigurasi Docker, Prometheus, Grafana, dan skrip untuk model serving & monitoring.
* **preprocessing/**: Berisi notebook EDA, skrip otomatisasi preprocessing, dan data mentah serta data yang telah diproses.
* **requirements.txt**: Daftar semua dependensi Python yang dibutuhkan.

## 🧑‍💻 Author

* **Nama:** Reisya Junita
* **GitHub:** [@reisyajunita](https://github.com/reisyajunita)
