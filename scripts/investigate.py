import pandas as pd

payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")

# Cek berapa order yang punya lebih dari 1 payment
multi_pay = payments.groupby("order_id")["payment_sequential"].max()
print("Order dengan lebih dari 1 payment method:")
print(multi_pay[multi_pay > 1].count())
print()
print("Contoh order_id nya:")
print(multi_pay[multi_pay > 1].head(10))