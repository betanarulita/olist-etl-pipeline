import pandas as pd
from sqlalchemy import create_engine
import os
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from extract_01 import extract_data
from transform_03 import transform_data

OUTPUT_PATH = "output/"
DB_PATH = f"{OUTPUT_PATH}olist.db"

# ── VALIDATION ─────────────────────────────────────────
def validate_data(data, master):
    print("=" * 50)
    print("=== VALIDATION PHASE ===")
    print("=" * 50)
    
    passed = True

    # 1. Row count check
    print("\n📊 Row Count Check:")
    print(f"   orders source      : {data['orders'].shape[0]:,}")
    print(f"   master table       : {master.shape[0]:,}")
    # Master boleh lebih banyak karena multiple items & payments
    if master.shape[0] >= data["orders"].shape[0]:
        print(f"   ✅ Row count makes sense")
    else:
        print(f"   ❌ WARNING: Master table lebih kecil dari orders!")
        passed = False

    # 2. Revenue check
    print("\n💰 Revenue Integrity Check:")
    source_revenue = data["payments"]["payment_value"].sum()
    # Master bisa duplikat payment karena join items
    # Jadi kita cek unique order_id + payment_value
    master_revenue = (
        master.drop_duplicates(subset=["order_id", "payment_value"])
        ["payment_value"].sum()
    )
    diff = abs(source_revenue - master_revenue)
    print(f"   Source payments total : Rp {source_revenue:,.2f}")
    print(f"   Master table total    : Rp {master_revenue:,.2f}")
    print(f"   Difference            : Rp {diff:,.2f}")
    if diff < 1:
        print(f"   ✅ Revenue matches!")
    else:
        print(f"   ⚠️  Revenue difference detected — investigate!")
        passed = False

    # 3. Null check pada kolom kritis
    print("\n🔍 Null Check (critical columns):")
    critical_cols = ["order_id", "customer_id", "order_status", "payment_value"]
    for col in critical_cols:
        if col in master.columns:
            nulls = master[col].isnull().sum()
            if nulls == 0:
                print(f"   ✅ {col}: no nulls")
            else:
                print(f"   ⚠️  {col}: {nulls:,} nulls found")

    # 4. Duplicate order_id + product_id check
    print("\n🔁 Duplicate Check:")
    dupes = master.duplicated(subset=["order_id", "product_id"]).sum()
    if dupes == 0:
        print(f"   ✅ No duplicates on order_id + product_id")
    else:
        print(f"   ⚠️  {dupes:,} duplicates found on order_id + product_id")

    print(f"\n{'✅ ALL VALIDATION PASSED' if passed else '⚠️  VALIDATION HAS WARNINGS'}")
    return passed

# ── LOAD ───────────────────────────────────────────────
def load_data(orders, products, master):
    print("\n" + "=" * 50)
    print("=== LOAD PHASE ===")
    print("=" * 50)

    os.makedirs(OUTPUT_PATH, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")

    tables = {
        "tbl_orders"  : orders,
        "tbl_products": products,
        "tbl_master"  : master
    }

    for name, df in tables.items():
        df.to_sql(name, engine, if_exists="replace", index=False)
        print(f"   ✅ Loaded {name}: {df.shape[0]:,} rows")

    print(f"\n   📁 Database saved: {DB_PATH}")

if __name__ == "__main__":
    data = extract_data()
    orders, products, master = transform_data(data)
    
    is_valid = validate_data(data, master)
    
    if is_valid:
        load_data(orders, products, master)
    else:
        print("\n⛔ Load dibatalkan — fix validation warnings dulu!")