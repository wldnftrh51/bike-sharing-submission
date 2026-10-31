# Bike Sharing — Submission Analisis Data

## Struktur proyek

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   ├── day_clean.csv
│   └── hour_clean.csv
├── data/
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── notebook.ipynb
├── requirements.txt
├── README.md
└── url.txt
```

## Menjalankan notebook

1. Ekstrak ZIP dan buka folder proyek.
2. Jalankan `notebook.ipynb` dari direktori utama proyek agar path `data/day.csv` dan `data/hour.csv` ditemukan.
3. Notebook berisi analisis dataset Bike Sharing.

## Menjalankan dashboard secara lokal

Dashboard membaca file hasil pembersihan `day_clean.csv` dan `hour_clean.csv` yang sudah disertakan di folder `dashboard/`. Karena itu, dashboard dapat dijalankan langsung tanpa menjalankan notebook terlebih dahulu.

```bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

Dashboard menyediakan pilihan data harian/per jam, filter tanggal dan musim, ringkasan metrik, visualisasi, serta unduhan data hasil filter.

## Dataset

Dataset mentah `day.csv` dan `hour.csv` disertakan di folder `data/`. File bersih untuk dashboard disertakan di folder `dashboard/`.
