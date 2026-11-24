import pandas as pd
from pathlib import Path

# 1. Locate project folders
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "sales_day2.csv"
reports_dir = BASE_DIR / "reports"

reports_dir.mkdir(parents=True, exist_ok=True)

# 2. Extract data from CSV
df = pd.read_csv(file_path)

print("=== ORIGINAL DATA ===")
print(df)

# 3. Check missing customer names
missing_customer = (
    df["customer_name"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
)

# 4. Check missing product names
missing_product = (
    df["product"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
)

# 5. Check duplicate transaction IDs
duplicate_id = df["transaction_id"].duplicated(
    keep="first"
)

# 6. Convert amount values to numbers
df["amount_numeric"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

# 7. Check invalid amounts
invalid_amount = (
    df["amount_numeric"].isna()
    | (df["amount_numeric"] <= 0)
)

# 8. Combine all validation rules
has_issue = (
    missing_customer
    | missing_product
    | duplicate_id
    | invalid_amount
)

# 9. Record reasons for failures
df["issues"] = ""

df.loc[missing_customer, "issues"] += "Missing customer; "
df.loc[missing_product, "issues"] += "Missing product; "
df.loc[duplicate_id, "issues"] += "Duplicate ID; "
df.loc[invalid_amount, "issues"] += "Invalid amount; "

# 10. Split valid and invalid records
output_df = df.drop(columns=["amount_numeric"])

valid_sales = output_df.loc[~has_issue].drop(
    columns=["issues"]
)

invalid_sales = output_df.loc[has_issue]

# 11. Calculate summary
total_records = len(df)
valid_count = len(valid_sales)
invalid_count = len(invalid_sales)

total_sales = df.loc[
    ~has_issue, "amount_numeric"
].sum()

# 12. Generate summary report
report = f"""=== DAY 2 ETL VALIDATION REPORT ===
Total records: {total_records}
Valid records: {valid_count}
Invalid records: {invalid_count}
Missing customers: {missing_customer.sum()}
Missing products: {missing_product.sum()}
Duplicate IDs: {duplicate_id.sum()}
Invalid amounts: {invalid_amount.sum()}
Total valid sales: {total_sales}
"""

# 13. Save files
(reports_dir / "day2_validation_summary.txt").write_text(
    report, encoding="utf-8"
)

valid_sales.to_csv(
    reports_dir / "valid_sales_day2.csv",
    index=False
)

invalid_sales.to_csv(
    reports_dir / "invalid_sales_day2.csv",
    index=False
)

print("\n" + report)
print("Day 2 reports generated successfully!")