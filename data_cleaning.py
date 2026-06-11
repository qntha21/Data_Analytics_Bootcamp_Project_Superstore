# =============================================================================
# DATA CLEANING - SUPERSTORE DATASET
# =============================================================================
# Deskripsi   : Script pembersihan data untuk dataset Sample Superstore
#               sebelum divisualisasikan di Tableau
# =============================================================================

import pandas as pd


# =============================================================================
# 1. IMPORT DATA
# =============================================================================

df = pd.read_csv('Sample_Superstore.csv', encoding='latin-1')
df_asli = df.copy()  # simpan salinan data asli sebagai cadangan

print("=" * 55)
print("DATA CLEANING - SAMPLE SUPERSTORE")
print("=" * 55)
print(f"\nDataset berhasil dimuat.")
print(f"Jumlah baris : {df.shape[0]:,}")
print(f"Jumlah kolom : {df.shape[1]}")


# =============================================================================
# 2. PENGENALAN DATA
# =============================================================================

print("\n" + "=" * 55)
print("PENGENALAN DATA")
print("=" * 55)

print("\n--- Informasi Umum Dataset ---")
df.info()

print("\n--- Statistik Deskriptif ---")
print(df.describe().round(2))

print("\n--- 5 Baris Pertama ---")
print(df.head())


# =============================================================================
# 3. DETEKSI MISSING VALUES
# =============================================================================

print("\n" + "=" * 55)
print("CEK MISSING VALUES")
print("=" * 55)

missing       = df.isnull().sum()
missing_pct   = (missing / len(df) * 100).round(2)
missing_df    = pd.DataFrame({
    'Jumlah Missing' : missing,
    'Persentase (%)'  : missing_pct
})

missing_ada = missing_df[missing_df['Jumlah Missing'] > 0]

if missing_ada.empty:
    print("\n✅ Tidak ditemukan missing values pada semua kolom.")
else:
    print("\n⚠️  Missing values ditemukan:")
    print(missing_ada)


# =============================================================================
# 4. DETEKSI DUPLIKAT
# =============================================================================

print("\n" + "=" * 55)
print("CEK DUPLIKAT")
print("=" * 55)

jumlah_duplikat = df.duplicated().sum()

if jumlah_duplikat == 0:
    print(f"\n✅ Tidak ditemukan baris duplikat.")
else:
    print(f"\n⚠️  Ditemukan {jumlah_duplikat} baris duplikat.")
    df = df.drop_duplicates()
    print(f"   Baris duplikat telah dihapus.")
    print(f"   Jumlah baris setelah pembersihan: {len(df):,}")


# =============================================================================
# 5. CEK TIPE DATA
# =============================================================================

print("\n" + "=" * 55)
print("CEK TIPE DATA")
print("=" * 55)

print("\n--- Tipe Data Per Kolom ---")
print(df.dtypes)


# =============================================================================
# 6. STANDARDISASI NAMA KOLOM
# =============================================================================

print("\n" + "=" * 55)
print("STANDARDISASI NAMA KOLOM")
print("=" * 55)

df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_'))

print("\n✅ Nama kolom berhasil distandarisasi:")
print(df.columns.tolist())

# hapus spasi tersembunyi pada semua kolom bertipe string
string_cols = df.select_dtypes(include='object').columns
for col in string_cols:
    df[col] = df[col].str.strip()

print(f"\n✅ Whitespace dihapus dari {len(string_cols)} kolom string.")


# =============================================================================
# 7. KONVERSI TIPE DATA
# =============================================================================

print("\n" + "=" * 55)
print("KONVERSI TIPE DATA")
print("=" * 55)

# tanggal → datetime (jika kolom tersedia)
for col_date, fmt in [('order_date','%m/%d/%Y'), ('ship_date','%m/%d/%Y')]:
    if col_date in df.columns:
        df[col_date] = pd.to_datetime(df[col_date], format=fmt)
        print(f"   ✅ {col_date} → datetime64")
    else:
        print(f"   ⏭️  {col_date} tidak ditemukan, dilewati")

# kode pos & row_id → string (jika kolom tersedia)
for col_str in ['postal_code', 'row_id']:
    if col_str in df.columns:
        df[col_str] = df[col_str].astype(str)
        print(f"   ✅ {col_str} → string")
    else:
        print(f"   ⏭️  {col_str} tidak ditemukan, dilewati")

print("\n✅ Konversi tipe data selesai:")
print(df.dtypes)


# =============================================================================
# 8. DETEKSI OUTLIER (metode IQR)
# =============================================================================

print("\n" + "=" * 55)
print("DETEKSI OUTLIER")
print("=" * 55)

numeric_cols    = ['sales', 'profit', 'discount', 'quantity']
outlier_summary = []

print()
for col in numeric_cols:
    Q1      = df[col].quantile(0.25)
    Q3      = df[col].quantile(0.75)
    IQR     = Q3 - Q1
    lower   = Q1 - 1.5 * IQR
    upper   = Q3 + 1.5 * IQR
    outlier = df[(df[col] < lower) | (df[col] > upper)]

    outlier_summary.append({
        'Kolom'            : col,
        'Batas Bawah'      : round(lower, 2),
        'Batas Atas'       : round(upper, 2),
        'Jumlah Outlier'   : len(outlier),
        'Persentase (%)'   : round(len(outlier) / len(df) * 100, 1)
    })

    print(f"{col:12} | Outlier: {len(outlier):>4} ({len(outlier)/len(df)*100:.1f}%)"
          f" | Rentang valid: [{lower:.2f}, {upper:.2f}]")

print("""
📌 KEPUTUSAN: Outlier DIPERTAHANKAN karena:
   1. Merepresentasikan transaksi bisnis nyata
   2. Justru menjadi insight utama analisis (diskon ekstrem → rugi)
   3. Bukan hasil input error atau data corruption
""")


# =============================================================================
# 9. FEATURE ENGINEERING
# =============================================================================

print("=" * 55)
print("FEATURE ENGINEERING")
print("=" * 55)

# --- kolom kelompok diskon ---
def discount_bucket(d):
    """Mengelompokkan nilai diskon ke dalam rentang kategori."""
    if d == 0:        return "0%"
    elif d <= 0.10:   return "1-10%"
    elif d <= 0.20:   return "11-20%"
    elif d <= 0.30:   return "21-30%"
    elif d <= 0.50:   return "31-50%"
    else:             return "51-80%"

df['discount_bucket'] = df['discount'].apply(discount_bucket)

# --- kolom indikator rugi ---
df['is_loss'] = df['profit'] < 0

print("\n✅ Kolom baru berhasil dibuat:")
print("   - discount_bucket : kelompok rentang diskon")
print("   - is_loss         : True jika transaksi menghasilkan kerugian")

print("\n--- Distribusi Discount Bucket ---")
print(df['discount_bucket'].value_counts().sort_index())

verify_cols = [c for c in ['sales','discount','discount_bucket','profit','is_loss'] if c in df.columns]
print("\n--- Verifikasi 5 Baris Pertama ---")
print(df[verify_cols].head())


# =============================================================================
# 10. RINGKASAN HASIL CLEANING
# =============================================================================

print("\n" + "=" * 55)
print("RINGKASAN HASIL CLEANING")
print("=" * 55)

print(f"""
  Dataset awal   : {df_asli.shape[0]:,} baris, {df_asli.shape[1]} kolom
  Dataset bersih : {df.shape[0]:,} baris, {df.shape[1]} kolom

  Perubahan yang dilakukan:
  ✅ Nama kolom distandarisasi (lowercase + underscore)
  ✅ Whitespace dihapus dari kolom string
  ✅ order_date & ship_date → datetime64
  ✅ postal_code & row_id   → string
  ✅ Outlier diinvestigasi & dipertahankan (transaksi valid)
  ✅ Kolom baru: discount_bucket, is_loss
""")


# =============================================================================
# 11. EKSPOR DATA BERSIH
# =============================================================================

output_file = 'Superstore_Bersih.xlsx'
df.to_excel(output_file, index=False, sheet_name='Superstore')

print(f"✅ Data bersih berhasil disimpan ke '{output_file}'")
print("   File siap digunakan untuk visualisasi di Tableau.\n")
