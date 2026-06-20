import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import validate_data, load_data
from scripts.analyze import analyze

if __name__ == "__main__":
    print("STARTING OLIST ETL PIPELINE")
    print("=" * 50)
    
    # EXTRACT
    data = extract_data()
    
    # TRANSFORM
    orders, products, master = transform_data(data)
    
    # VALIDATE + LOAD
    is_valid = validate_data(data, master)
    
    if is_valid:
        load_data(orders, products, master)
        
        # ANALYZE
        analyze()
        
        print("\nPIPELINE COMPLETED SUCCESSFULLY!")
    else:
        print("\nPIPELINE STOPPED — fix validation issues first!")