# =============================================================================
# DATA CLEANING - SUPERSTORE DATASET
# =============================================================================

# Description : Data cleaning script for the Sample Superstore dataset
#               in preparation for visualization in Tableau
# =============================================================================

import pandas as pd


# =============================================================================
# 1. LOAD DATA
# =============================================================================

df         = pd.read_csv('Sample_Superstore.csv', encoding='latin-1')
df_original = df.copy()  # keep a copy of the raw data as a backup

print("=" * 55)
print("DATA CLEANING - SAMPLE SUPERSTORE")
print("=" * 55)
print(f"\nDataset loaded successfully.")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")


# =============================================================================
# 2. DATA OVERVIEW
# =============================================================================

print("\n" + "=" * 55)
print("DATA OVERVIEW")
print("=" * 55)

print("\n--- General Dataset Info ---")
df.info()

print("\n--- Descriptive Statistics ---")
print(df.describe().round(2))

print("\n--- First 5 Rows ---")
print(df.head())


# =============================================================================
# 3. CHECK MISSING VALUES
# =============================================================================

print("\n" + "=" * 55)
print("CHECK MISSING VALUES")
print("=" * 55)

missing     = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df  = pd.DataFrame({
    'Missing Count'  : missing,
    'Missing % '     : missing_pct
})

has_missing = missing_df[missing_df['Missing Count'] > 0]

if has_missing.empty:
    print("\n✅ No missing values found across all columns.")
else:
    print("\n⚠️  Missing values detected:")
    print(has_missing)


# =============================================================================
# 4. CHECK DUPLICATES
# =============================================================================

print("\n" + "=" * 55)
print("CHECK DUPLICATES")
print("=" * 55)

n_duplicates = df.duplicated().sum()

if n_duplicates == 0:
    print(f"\n✅ No duplicate rows found.")
else:
    print(f"\n⚠️  Found {n_duplicates} duplicate rows.")
    df = df.drop_duplicates()
    print(f"   Duplicate rows removed.")
    print(f"   Row count after cleaning: {len(df):,}")


# =============================================================================
# 5. CHECK DATA TYPES
# =============================================================================

print("\n" + "=" * 55)
print("CHECK DATA TYPES")
print("=" * 55)

print("\n--- Data Type per Column ---")
print(df.dtypes)


# =============================================================================
# 6. COLUMN NAME STANDARDIZATION
# =============================================================================

print("\n" + "=" * 55)
print("COLUMN NAME STANDARDIZATION")
print("=" * 55)

df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('-', '_'))

print("\n✅ Column names standardized successfully:")
print(df.columns.tolist())

# strip hidden whitespace from all string columns
string_cols = df.select_dtypes(include='object').columns
for col in string_cols:
    df[col] = df[col].str.strip()

print(f"\n✅ Whitespace stripped from {len(string_cols)} string columns.")


# =============================================================================
# 7. DATA TYPE CONVERSION
# =============================================================================

print("\n" + "=" * 55)
print("DATA TYPE CONVERSION")
print("=" * 55)

# date columns → datetime (only if the column exists)
for col_date, fmt in [('order_date', '%m/%d/%Y'), ('ship_date', '%m/%d/%Y')]:
    if col_date in df.columns:
        df[col_date] = pd.to_datetime(df[col_date], format=fmt)
        print(f"   ✅ {col_date} → datetime64")
    else:
        print(f"   ⏭️  {col_date} not found — skipped")

# postal code & row_id → string (they are identifiers, not numbers to compute)
for col_str in ['postal_code', 'row_id']:
    if col_str in df.columns:
        df[col_str] = df[col_str].astype(str)
        print(f"   ✅ {col_str} → string")
    else:
        print(f"   ⏭️  {col_str} not found — skipped")

print("\n✅ Data type conversion complete:")
print(df.dtypes)


# =============================================================================
# 8. OUTLIER DETECTION (IQR method)
# =============================================================================

print("\n" + "=" * 55)
print("OUTLIER DETECTION")
print("=" * 55)

numeric_cols     = ['sales', 'profit', 'discount', 'quantity']
outlier_summary  = []

print()
for col in numeric_cols:
    Q1      = df[col].quantile(0.25)
    Q3      = df[col].quantile(0.75)
    IQR     = Q3 - Q1
    lower   = Q1 - 1.5 * IQR
    upper   = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]

    outlier_summary.append({
        'Column'        : col,
        'Lower Bound'   : round(lower, 2),
        'Upper Bound'   : round(upper, 2),
        'Outlier Count' : len(outliers),
        'Outlier %'     : round(len(outliers) / len(df) * 100, 1)
    })

    print(f"{col:12} | Outliers: {len(outliers):>4} ({len(outliers)/len(df)*100:.1f}%)"
          f" | Valid range: [{lower:.2f}, {upper:.2f}]")

print("""
📌 DECISION: Outliers are RETAINED because:
   1. They represent legitimate business transactions
   2. They are actually the core insight of this analysis
      (extreme discounts → losses)
   3. They are not the result of data entry errors or corruption
""")


# =============================================================================
# 9. FEATURE ENGINEERING
# =============================================================================

print("=" * 55)
print("FEATURE ENGINEERING")
print("=" * 55)

# --- discount bucket column ---
def discount_bucket(d):
    """Groups a discount value into a labeled range category."""
    if d == 0:       return "0%"
    elif d <= 0.10:  return "1-10%"
    elif d <= 0.20:  return "11-20%"
    elif d <= 0.30:  return "21-30%"
    elif d <= 0.50:  return "31-50%"
    else:            return "51-80%"

df['discount_bucket'] = df['discount'].apply(discount_bucket)

# --- loss indicator column ---
df['is_loss'] = df['profit'] < 0

print("\n✅ New columns created:")
print("   - discount_bucket : groups discount values into labeled ranges")
print("   - is_loss         : True if the transaction generated a loss")

print("\n--- Discount Bucket Distribution ---")
print(df['discount_bucket'].value_counts().sort_index())

verify_cols = [c for c in ['sales', 'discount', 'discount_bucket', 'profit', 'is_loss']
               if c in df.columns]
print("\n--- Verification — First 5 Rows ---")
print(df[verify_cols].head())


# =============================================================================
# 10. CLEANING SUMMARY
# =============================================================================

print("\n" + "=" * 55)
print("CLEANING SUMMARY")
print("=" * 55)

print(f"""
  Original dataset : {df_original.shape[0]:,} rows, {df_original.shape[1]} columns
  Clean dataset    : {df.shape[0]:,} rows, {df.shape[1]} columns

  Changes applied:
  ✅ Column names standardized (lowercase + underscores)
  ✅ Whitespace stripped from all string columns
  ✅ order_date & ship_date → datetime64
  ✅ postal_code & row_id   → string
  ✅ Outliers investigated & retained (valid transactions)
  ✅ New columns added: discount_bucket, is_loss
""")


# =============================================================================
# 11. EXPORT CLEAN DATA
# =============================================================================

output_file = 'Superstore_Clean.xlsx'
df.to_excel(output_file, index=False, sheet_name='Superstore')

print(f"✅ Clean data saved to '{output_file}'")
print("   File is ready for visualization in Tableau.\n")
