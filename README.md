# Olist E-Commerce ETL Pipeline

## Business Problem

> "Di mana titik kebocoran revenue terbesar pada platform e-commerce Olist — dari pembatalan order, keterlambatan pengiriman, atau kategori produk tertentu?"

## Pipeline Architecture

```
[7 of 9 CSV Files]
      ↓ Extract
[Python/Pandas]
      ↓ Explore
[Data Profiling — missing values, data types]
      ↓ Transform
[Cleaning, JOIN, Feature Engineering]
      ↓ Validate
[Revenue Integrity Check, Row Count, Null Check]
      ↓ Load
[SQLite Database — 3 tables]
      ↓ Analyze
[SQL Queries — Business Insight]
```

## Dataset
- Source: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 9 CSV files total, 7 digunakan (reviews & geolocation excluded — tidak relevan untuk analisis revenue)
- 99,441 orders | 2016–2018

### Tables Used (7 of 9)

| Table | Rows | Key | Note |
|---|---|---|---|
| olist_orders | 99,441 | order_id | Base table |
| olist_customers | 99,441 | customer_id | Customer info |
| olist_order_items | 112,650 | order_id | Multi-item per order |
| olist_payments | 103,886 | order_id | Multi-method per order |
| olist_products | 32,951 | product_id | Product catalog |
| olist_sellers | 3,095 | seller_id | Seller info |
| category_name_translation | 71 | category_name | PT→EN translation |

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 | Pipeline scripting |
| Pandas | 3.0 | Data transformation |
| SQLAlchemy | 2.0 | Database connection (agnostic) |
| SQLite | 3 | Data storage |
| SQL | — | Business analysis queries |

## Project Structure

```
olist_etl_pipeline/
├── main.py                  # Run full pipeline
├── requirements.txt
├── data/
│   ├── raw/                 # Source CSV files (not tracked)
│   └── processed/
├── scripts/
│   ├── extract_01.py           # Load CSV to DataFrames
│   ├── explore_02.py           # Data profiling & EDA
│   ├── transform_03.py         # Cleaning, joining, feature engineering
│   ├── load_04.py              # Validation + load to SQLite
│   └── analyze_05.py           # SQL-based business analysis
├── output/
│   └── olist.db             # SQLite database (generated)
└── docs/
    ├── decisions.md         # Engineering decision log
    ├── screenshots/         # Pipeline execution screenshots
    └── txt/                 # Pipeline output logs
```

## How to Run

```bash
# 1. Clone repo
git clone https://github.com/betanarulita/olist-etl-pipeline.git
cd olist-etl-pipeline

# 2. Download dataset from Kaggle
# https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
# Extract all CSV files to data/raw/

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run full pipeline
python main.py
```

## Key Findings

### 1. Revenue Leakage from Cancelled Orders
- 625 orders cancelled dengan payment sudah masuk sistem
- Total revenue at risk: **Rp 186,964**
- Avg order value cancelled (Rp 264) lebih tinggi dari delivered (Rp 179)
- Indikasi: customer dengan order bernilai tinggi lebih sering cancel

### 2. Late Delivery Impact
- **7,827 orders (7.9%) terlambat** dari estimasi pengiriman
- `is_late` flag: 1 = order_delivered_customer_date > order_estimated_delivery_date
- Avg order value late (Rp 185.45) vs on-time (Rp 180.07) — selisih Rp 5.38
- Bukan asumsi — dihitung langsung dari tbl_master

### 3. Revenue by Category
- Top category: bed_bath_table → Rp 1,711,258
- Highest avg order value: watches_gifts → Rp 238 per transaksi
- **164 cancelled orders dengan `product_category_name_english` = NULL** → Rp 37,337 revenue lost
- NULL muncul karena LEFT JOIN products → category_translation tidak menemukan pasangan

### 4. Revenue Integrity Validation
```
Source payments total : Rp 16,008,872.12
Master table total    : Rp 16,008,872.12
Difference            : Rp 0.00 ✓
```

## Engineering Decisions

Lihat [`docs/decisions.md`](docs/decisions.md) untuk penjelasan lengkap setiap keputusan teknis.

Ringkasan:
- **Aggregate Before JOIN** — 3,039 orders punya multiple payment methods → aggregate dulu untuk hindari double-count
- **fillna('unknown') bukan DROP** — 610 NULL di product_category_name → menghapus berisiko kehilangan data penting
- **Database-Agnostic via SQLAlchemy** — migrasi ke PostgreSQL/BigQuery cukup ganti 1 baris connection string

## Data Quality Notes
- 3 orders tidak memiliki payment record (known data characteristic dari source)
- 10,225 duplicate order_id + product_id — expected behavior (1 order bisa beli produk sama lebih dari 1)

## Author
**Beta Narulita Aprilia**
Data Engineer | Information Systems Graduate
[LinkedIn](https://www.linkedin.com/in/betana/) · [GitHub](https://github.com/betanarulita)
