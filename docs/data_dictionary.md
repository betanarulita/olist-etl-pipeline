# Data Dictionary

Dokumentasi kolom-kolom yang ada di tabel hasil pipeline.

---

## tbl_master (113,425 rows x 16 cols)

Tabel utama hasil JOIN dari 7 source tables. Digunakan untuk semua SQL analysis queries.

| Kolom | Tipe Data | Sumber Table | Deskripsi |
|---|---|---|---|
| order_id | str | olist_orders | ID unik per order |
| customer_id | str | olist_orders | ID customer yang melakukan order |
| order_status | str | olist_orders | Status order: delivered, shipped, canceled, dll |
| order_purchase_timestamp | datetime | olist_orders | Waktu order dibuat |
| order_approved_at | datetime | olist_orders | Waktu order diapprove (nullable) |
| order_delivered_carrier_date | datetime | olist_orders | Waktu order diserahkan ke kurir (nullable) |
| order_delivered_customer_date | datetime | olist_orders | Waktu order sampai ke customer (nullable) |
| order_estimated_delivery_date | datetime | olist_orders | Estimasi waktu delivery |
| is_late | int | engineered | Flag keterlambatan: 1 = terlambat, 0 = on time |
| customer_state | str | olist_customers | Negara bagian customer |
| product_id | str | olist_order_items | ID produk yang dibeli |
| price | float | olist_order_items | Harga produk per item (Rp) |
| freight_value | float | olist_order_items | Biaya pengiriman (Rp) |
| payment_value | float | olist_payments (aggregated) | Total payment per order — di-aggregate dari multiple payment methods |
| payment_type | str | olist_payments (aggregated) | Metode pembayaran — concat jika multiple |
| product_category_name_english | str | category_name_translation | Nama kategori dalam bahasa Inggris (nullable — lihat catatan) |

### Catatan Penting

**is_late flag:**
```
is_late = 1 → order_delivered_customer_date > order_estimated_delivery_date
is_late = 0 → on time atau belum delivered (order_delivered_customer_date = NULL)
```

**payment_value:**
Kolom ini hasil aggregate dari tbl_payments — bukan raw payment value. Satu order bisa punya multiple payment methods (credit card + voucher), sehingga di-groupby order_id dan di-sum sebelum JOIN ke master table.

**product_category_name_english (nullable):**
NULL muncul ketika produk tidak memiliki terjemahan kategori di category_name_translation table. Ini bukan error pipeline — ini data quality issue dari source. 164 cancelled orders masuk ke grup NULL ini dengan Rp 37,337 revenue lost.

---

## tbl_orders (99,441 rows)

Tabel orders yang sudah ditransform — kolom tanggal sudah dikonversi ke datetime dan ditambah kolom `is_late`.

| Kolom | Tipe Data | Deskripsi |
|---|---|---|
| order_id | str | ID unik per order |
| customer_id | str | ID customer |
| order_status | str | Status order |
| order_purchase_timestamp | datetime | Waktu order dibuat |
| order_approved_at | datetime | Waktu diapprove (nullable) |
| order_delivered_carrier_date | datetime | Waktu ke kurir (nullable) |
| order_delivered_customer_date | datetime | Waktu sampai customer (nullable) |
| order_estimated_delivery_date | datetime | Estimasi delivery |
| is_late | int | 1 = terlambat, 0 = on time |

---

## tbl_products (32,951 rows)

Tabel products yang sudah di-join dengan category translation.

| Kolom | Tipe Data | Deskripsi |
|---|---|---|
| product_id | str | ID unik produk |
| product_category_name | str | Nama kategori dalam bahasa Portugis (NULL diisi 'unknown') |
| product_name_lenght | float | Panjang karakter nama produk |
| product_description_lenght | float | Panjang karakter deskripsi produk |
| product_photos_qty | float | Jumlah foto produk |
| product_weight_g | float | Berat produk dalam gram (nullable) |
| product_length_cm | float | Panjang produk dalam cm (nullable) |
| product_height_cm | float | Tinggi produk dalam cm (nullable) |
| product_width_cm | float | Lebar produk dalam cm (nullable) |
| product_category_name_english | str | Nama kategori dalam bahasa Inggris (nullable) |