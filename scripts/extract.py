import pandas as pd
import os

# Path
RAW_PATH = "data/raw/"

def extract_data():
    print("=== EXTRACT PHASE ===")
    
    datasets = {}
    files = {
        "customers"   : "olist_customers_dataset.csv",
        "orders"      : "olist_orders_dataset.csv",
        "order_items" : "olist_order_items_dataset.csv",
        "payments"    : "olist_order_payments_dataset.csv",
        "products"    : "olist_products_dataset.csv",
        "sellers"     : "olist_sellers_dataset.csv",
        "category"    : "product_category_name_translation.csv"
    }
    
    for name, file in files.items():
        path = os.path.join(RAW_PATH, file)
        datasets[name] = pd.read_csv(path)
        print(f"✓ Loaded {name}: {datasets[name].shape[0]:,} rows x {datasets[name].shape[1]} cols")
    
    return datasets

if __name__ == "__main__":
    data = extract_data()