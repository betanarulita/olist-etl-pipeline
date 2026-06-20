# Data Engineering Decision Log

## 1. Kenapa SQLite bukan PostgreSQL?
**Keputusan:** Pakai SQLite sebagai database storage.

**Alasan:**
- SQLite adalah file tunggal (.db) — mudah di-share dan di-upload ke GitHub
- Tidak perlu install database server — siapapun bisa langsung clone dan run
- Cukup untuk dataset skala ini (113K rows)
- Untuk production environment, arsitektur ini bisa di-migrate ke PostgreSQL/BigQuery dengan mengganti connection string di SQLAlchemy

---

## 2. Kenapa LEFT JOIN bukan INNER JOIN?
**Keputusan:** Semua JOIN di master table menggunakan `how="left"`.

**Alasan:**
- INNER JOIN akan drop rows yang tidak match di kedua table
- Contoh: order yang tidak punya payment record → hilang dari analisis
- LEFT JOIN mempertahankan semua orders sebagai base — rows yang tidak match akan NULL
- Lebih aman untuk analisis bisnis karena tidak ada data yang hilang secara diam-diam

---

## 3. Kenapa payments di-aggregate sebelum JOIN?
**Keputusan:** `payments` di-groupby `order_id` dulu sebelum di-JOIN ke master table.

**Alasan:**
- 1 order bisa bayar pakai multiple payment methods (credit card + voucher)
- Kalau langsung JOIN → setiap item di order akan duplikat sebanyak jumlah payment methods
- Investigasi menemukan 3,039 orders punya lebih dari 1 payment method
- Solusi: aggregate dulu → `payment_value` di-sum, `payment_type` di-concat

**Validasi:** Revenue sebelum fix = Rp 15,991,002 vs source Rp 16,008,872 (selisih Rp 17,869). Setelah fix = Rp 0 difference ✅

---

## 4. Kenapa `product_category_name` NULL diisi "unknown"?
**Keputusan:** NULL category diisi string "unknown", bukan di-drop.

**Alasan:**
- 610 products (1.9%) tidak punya category name
- Kalau di-drop → 610 produk hilang dari analisis revenue per kategori
- Dengan "unknown", produk tetap ikut analisis dan justru teridentifikasi sebagai temuan:
  → 164 cancelled orders tanpa kategori = Rp 37,337 revenue lost
- Prinsip: jangan drop data yang tidak kamu pahami — flag dulu, investigasi kemudian

---

## 5. Kenapa kolom dimensi produk tidak difix?
**Keputusan:** `product_weight_g`, `product_length_cm`, dst dibiarkan NULL.

**Alasan:**
- Fokus analisis adalah revenue leakage — bukan shipping cost calculation
- Kolom dimensi tidak masuk ke master table dan tidak dipakai di SQL analysis
- Prinsip: hanya fix kolom yang relevan dengan pertanyaan bisnis

---

## 6. Kenapa kolom tanggal dikonversi ke datetime?
**Keputusan:** Semua kolom tanggal di orders dikonversi dari string ke datetime.

**Alasan:**
- Data asli menyimpan tanggal sebagai string (object) — tidak bisa dihitung
- Untuk bisa hitung keterlambatan: `delivered_date - estimated_date` → butuh datetime
- `errors="coerce"` dipakai supaya nilai yang tidak valid jadi NaT, bukan error

---

## 7. Kenapa pakai `is_late` flag (0/1) bukan boolean?
**Keputusan:** Kolom keterlambatan disimpan sebagai integer (0/1), bukan True/False.

**Alasan:**
- Integer lebih mudah di-aggregate di SQL: `SUM(is_late)` langsung kasih total late orders
- Boolean di SQLite tidak native — disimpan sebagai 0/1 anyway
- Konsisten dengan konvensi data warehouse (flag columns sebagai integer)