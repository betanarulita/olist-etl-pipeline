import pandas as pd
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from extract_01 import extract_data

PROCESSED_PATH = "data/processed/"

def transform_data(data):
    print("=" * 50)
    print("=== TRANSFORM PHASE ===")
    print("=" * 50)

    # ── 1. ORDERS ──────────────────────────────────
    # Keputusan: konversi kolom tanggal str → datetime
    # Alasan: dibutuhkan untuk hitung keterlambatan pengiriman
    print("\n📦 Transforming ORDERS...")
    orders = data["orders"].copy()
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")
    
    # Tambah kolom: apakah order terlambat?
    # Alasan: ini metric utama untuk analisis keterlambatan
    orders["is_late"] = (
        orders["order_delivered_customer_date"] > 
        orders["order_estimated_delivery_date"]
    ).astype(int)
    
    print(f"   ✅ Date columns converted to datetime")
    print(f"   ✅ Added 'is_late' flag")
    print(f"   ℹ️  Late orders: {orders['is_late'].sum():,} ({orders['is_late'].mean()*100:.1f}%)")

    # ── 2. PRODUCTS ────────────────────────────────
    # Keputusan: isi NULL category dengan "unknown"
    # Alasan: category_name dipakai analisis revenue per kategori
    # Kolom lain (weight, dimensions) dibiarkan — tidak relevan untuk analisis kita
    print("\n📦 Transforming PRODUCTS...")
    products = data["products"].copy()
    products["product_category_name"] = products["product_category_name"].fillna("unknown")
    
    # Join ke category translation
    # Alasan: nama kategori asli dalam bahasa Portugis — tidak readable
    products = products.merge(
        data["category"],
        on="product_category_name",
        how="left"
    )
    products["product_category_name_english"] = (
        products["product_category_name_english"].fillna("unknown")
    )
    print(f"   ✅ NULL categories filled with 'unknown'")
    print(f"   ✅ Joined with English category translation")

    # ── 3. MASTER TABLE ────────────────────────────
    # Gabungkan semua table yang relevan untuk analisis
    # ── 3. MASTER TABLE ────────────────────────────
    # Gabungkan semua table yang relevan untuk analisis
    print("\n📦 Building MASTER TABLE...")
    
    # Aggregate payments per order_id dulu sebelum JOIN
    # Alasan: 1 order bisa punya multiple payment methods
    # → kalau langsung JOIN = duplikat rows & revenue kehitung berkali-kali
    payments_agg = (
        data["payments"]
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_type=("payment_type", lambda x: ",".join(x.unique()))
        )
        .reset_index()
    )

    master = (
        orders
        .merge(data["customers"][["customer_id", "customer_state"]], 
               on="customer_id", how="left")
        .merge(data["order_items"][["order_id", "product_id", "price", "freight_value"]], 
               on="order_id", how="left")
        .merge(payments_agg, 
               on="order_id", how="left")
        .merge(products[["product_id", "product_category_name_english"]], 
               on="product_id", how="left")
    )
    
    print(f"   ✅ Master table built: {master.shape[0]:,} rows x {master.shape[1]} cols")
    print(f"   ✅ Columns: {list(master.columns)}")

    return orders, products, master

if __name__ == "__main__":
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    data = extract_data()
    orders, products, master = transform_data(data)