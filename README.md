# Olist E-Commerce ETL Pipeline

## Business Problem
Sebagai Data Engineer, saya diminta membangun pipeline data untuk menjawab pertanyaan bisnis:

> **"Di mana titik kebocoran revenue terbesar pada platform e-commerce Olist — apakah dari pembatalan order, keterlambatan pengiriman, atau kategori produk tertentu?"**

## Pipeline Architecture
```
[Raw CSV Files]
      ↓ Extract
[Python/Pandas]
      ↓ Transform
[Cleaned & Joined DataFrames]
      ↓ Validate
[Data Quality Checks]
      ↓ Load
[SQLite Database]
      ↓ Analyze
[SQL Query Results]
```

## Dataset
- Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 9 CSV files, 99,441 orders, 2016-2018
- Tables: customers, orders, order_items, payments, products, sellers, category

## Tech Stack
- Python 3.13
- Pandas - data transformation & manipulation
- SQLAlchemy - database connection
- SQLite - data storage
- SQL - analysis queries

## Project Structure
```
olist_etl_pipeline/
├── main.py                  # Run full pipeline
├── requirements.txt
├── data/
│   ├── raw/                 # Source CSV files
│   └── processed/           # Processed outputs
├── scripts/
│   ├── extract_01.py        # Load CSV to DataFrames
│   ├── explore_02.py        # Data profiling & EDA
│   ├── transform_03.py      # Cleaning, joining, feature engineering
│   ├── load_04.py           # Validation + load to SQLite
│   └── analyze_05.py        # SQL-based business analysis
├── output/
│   └── olist.db             # SQLite database
└── docs/
    ├── screenshots/         # Pipeline execution screenshots
    └── txt/                 # Pipeline output logs
```

## How to Run
```bash
# 1. Clone repo
git clone https://github.com/betanarulita/olist-etl-pipeline.git
cd olist-etl-pipeline

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run full pipeline
python main.py
```

## Key Findings

### 1. Revenue Leakage from Cancelled Orders
- 625 orders cancelled dengan payment sudah masuk
- Total revenue at risk: **Rp 186,964**
- Avg order value cancelled (264) lebih tinggi dari delivered (179)
- Indikasi: customer premium lebih sering cancel

### 2. Late Delivery Impact
- **7,827 orders (7.9%) terlambat** dari estimasi pengiriman
- Order yang terlambat memiliki avg value lebih tinggi (185 vs 180)
- Indikasi: produk bernilai tinggi lebih rentan keterlambatan

### 3. Top Revenue Categories
| Category | Total Orders | Revenue |
|---|---|---|
| bed_bath_table | 9,399 | Rp 1,711,258 |
| health_beauty | 8,800 | Rp 1,653,730 |
| computers_accessories | 6,654 | Rp 1,571,544 |

### 4. Unidentified Cancelled Orders
- **164 cancelled orders tanpa kategori produk** → Rp 37,337 revenue lost
- Root cause: produk mungkin sudah dihapus dari katalog
- Rekomendasi: implementasi soft delete pada katalog produk

### 5. Revenue Growth Trend
- Growth dari 300 orders/bulan (Oct 2016) → 7,500 orders/bulan (Nov 2017)
- Peak November 2017 → kemungkinan Black Friday effect
- Revenue stabil di Rp 1.2-1.5M/bulan sepanjang 2018

## Data Quality Notes
- 3 orders tidak memiliki payment record (known data characteristic)
- 10,225 duplicate order_id + product_id - expected behavior (1 order bisa beli produk sama lebih dari 1)
- Missing category names diisi "unknown" untuk mempertahankan data completeness

## Author
**Beta Narulita Aprilia**  
Data Engineer | Information Systems Graduate  
[LinkedIn](https://www.linkedin.com/in/betana/) · [GitHub](https://github.com/betanarulita)
