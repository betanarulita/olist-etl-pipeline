import pandas as pd
import os

RAW_PATH = "data/raw/"

def load_data():
    files = {
        "customers"   : "olist_customers_dataset.csv",
        "orders"      : "olist_orders_dataset.csv",
        "order_items" : "olist_order_items_dataset.csv",
        "payments"    : "olist_order_payments_dataset.csv",
        "products"    : "olist_products_dataset.csv",
        "sellers"     : "olist_sellers_dataset.csv",
        "category"    : "product_category_name_translation.csv"
    }
    return {name: pd.read_csv(os.path.join(RAW_PATH, file)) 
            for name, file in files.items()}

def explore(data):
    print("=" * 50)
    print("=== EXPLORE PHASE ===")
    print("=" * 50)

    for name, df in data.items():
        print(f"\n📦 TABLE: {name.upper()}")
        print(f"   Shape   : {df.shape[0]:,} rows x {df.shape[1]} cols")
        
        # Missing values
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            print(f"   ⚠️  Missing values:")
            for col, count in missing.items():
                pct = count / len(df) * 100
                print(f"      - {col}: {count:,} ({pct:.1f}%)")
        else:
            print(f"   ✅ No missing values")

        # Duplicates
        dupes = df.duplicated().sum()
        if dupes > 0:
            print(f"   ⚠️  Duplicates: {dupes:,} rows")
        else:
            print(f"   ✅ No duplicates")

        # Data types
        print(f"   📋 Data types:")
        for col, dtype in df.dtypes.items():
            print(f"      - {col}: {dtype}")

if __name__ == "__main__":
    data = load_data()
    explore(data)