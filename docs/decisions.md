# Engineering Decision Log

Dokumen ini mencatat setiap keputusan teknis yang diambil selama build pipeline, beserta alasan dan hasilnya.

---

## 1. Aggregate Payments Before JOIN

**Temuan:** 3,039 orders memiliki lebih dari 1 payment method (credit card + voucher, dll).

**Masalah:** Direct JOIN payments ke master table → setiap item di order akan duplikat sebanyak jumlah payment methods → revenue double-count.

**Bukti sebelum fix:**
```
Source payments total : Rp 16,008,872.12
Master table total    : Rp 15,991,002.84
Difference            : Rp 17,869.28 ← double-count
```

**Keputusan:** Aggregate payments per order_id dulu sebelum JOIN:
```python
payments_agg = (
    data["payments"]
    .groupby("order_id")
    .agg(
        payment_value=("payment_value", "sum"),
        payment_type=("payment_type", lambda x: ",".join(x.unique()))
    )
    .reset_index()
)
```

**Hasil setelah fix:**
```
Difference : Rp 0.00 ✓
```

---

## 2. fillna('unknown') bukan DROP

**Temuan:** 610 produk tidak punya nama kategori (NULL di `product_category_name`).

**Opsi yang dipertimbangkan:**
- **DROP** — berisiko kehilangan data penting, bias analisis
- **Imputation** — misleading, seolah kategori diketahui padahal tidak
- **fillna('unknown')** ✅ — data tetap utuh, temuan tetap valid

<<<<<<< Updated upstream
**Keputusan:** Tandai sebagai 'unknown' - menghapus berisiko kehilangan data penting, mengisi kategori lain justru misleading.
=======
**Keputusan:** Tandai sebagai 'unknown' — menghapus berisiko kehilangan data penting, mengisi kategori lain justru misleading.
>>>>>>> Stashed changes

**Hasil:** 164 cancelled orders tanpa kategori berhasil terdeteksi → Rp 37,337 revenue lost yang tidak akan terlihat kalau data langsung dihapus.

---

## 3. LEFT JOIN bukan INNER JOIN

**Keputusan:** Semua JOIN di master table menggunakan `how="left"`.

<<<<<<< Updated upstream
**Alasan:** INNER JOIN akan drop rows yang tidak match di kedua table - misalnya order yang tidak punya payment record akan hilang dari analisis secara diam-diam. LEFT JOIN mempertahankan semua orders sebagai base, rows yang tidak match akan NULL dan masih bisa diinvestigasi.

**Prinsip:** Jangan biarkan data hilang secara diam-diam - lebih baik NULL yang terlihat daripada data yang hilang tanpa jejak.
=======
**Alasan:** INNER JOIN akan drop rows yang tidak match di kedua table — misalnya order yang tidak punya payment record akan hilang dari analisis secara diam-diam. LEFT JOIN mempertahankan semua orders sebagai base, rows yang tidak match akan NULL dan masih bisa diinvestigasi.

**Prinsip:** Jangan biarkan data hilang secara diam-diam — lebih baik NULL yang terlihat daripada data yang hilang tanpa jejak.
>>>>>>> Stashed changes

---

## 4. Database-Agnostic via SQLAlchemy

**Keputusan:** Pakai SQLAlchemy sebagai abstraction layer untuk koneksi database.

**Tiga opsi database yang bisa dipakai:**
- **SQLite** ✅ — digunakan di project ini, portable, tidak perlu server
- **PostgreSQL** — cocok untuk production, multi-user
- **BigQuery** — cocok untuk skala enterprise

<<<<<<< Updated upstream
**Kenapa SQLAlchemy:** Migrasi antar database hanya perlu ganti 1 baris connection string - logic pipeline tidak berubah sama sekali:
=======
**Kenapa SQLAlchemy:** Migrasi antar database hanya perlu ganti 1 baris connection string — logic pipeline tidak berubah sama sekali:
>>>>>>> Stashed changes
```python
# SQLite (sekarang)
engine = create_engine("sqlite:///output/olist.db")

# PostgreSQL (production)
engine = create_engine("postgresql://user:password@localhost:5432/olist_db")
```

---

## 5. Exclude olist_order_reviews & olist_geolocation

**Keputusan:** 2 dari 9 CSV files tidak diload ke pipeline.

| File | Alasan exclude |
|---|---|
<<<<<<< Updated upstream
| olist_order_reviews | Data rating/komentar - tidak relevan untuk analisis revenue |
| olist_geolocation | Data koordinat lokasi - tidak masuk ke business question |

**Prinsip:** Hanya load data yang relevan dengan business question - pipeline yang efisien tidak memproses data yang tidak dibutuhkan.
=======
| olist_order_reviews | Data rating/komentar — tidak relevan untuk analisis revenue |
| olist_geolocation | Data koordinat lokasi — tidak masuk ke business question |

**Prinsip:** Hanya load data yang relevan dengan business question — pipeline yang efisien tidak memproses data yang tidak dibutuhkan.
>>>>>>> Stashed changes

---

## 6. NaN di product_category_name_english

**Penjelasan:** Setelah LEFT JOIN products ke category_name_translation, beberapa produk menghasilkan NULL di kolom `product_category_name_english`.

<<<<<<< Updated upstream
**Root cause:** 610 produk tidak memiliki terjemahan kategori di table category_translation - kemungkinan produk baru yang belum terdaftar atau kategori yang tidak ter-cover di translation table.

**Dampak yang terdeteksi:** 164 cancelled orders masuk ke grup NaN ini dengan Rp 37,337 revenue lost - ini yang menjadi data quality finding di analisis.
=======
**Root cause:** 610 produk tidak memiliki terjemahan kategori di table category_translation — kemungkinan produk baru yang belum terdaftar atau kategori yang tidak ter-cover di translation table.

**Dampak yang terdeteksi:** 164 cancelled orders masuk ke grup NaN ini dengan Rp 37,337 revenue lost — ini yang menjadi data quality finding di analisis.
>>>>>>> Stashed changes
