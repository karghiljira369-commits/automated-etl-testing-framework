import pandas as pd
from pathlib import Path

# Step 1: Locate the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Step 2: Locate the CSV file
file_path = BASE_DIR / "data" / "sales.csv"

# Step 3: Read the CSV
df = pd.read_csv(file_path)

print("=== ORIGINAL SALES DATA ===")
print(df)

# Step 4: Identify valid and invalid records
valid_sales = df[df["amount"] > 0]
invalid_sales = df[df["amount"] <= 0]

# Step 5: Display invalid records
print("\n=== INVALID SALES ===")
print(invalid_sales)

# Step 6: Display summary
print("\n=== VALIDATION SUMMARY ===")
print("Total records:", len(df))
print("Valid records:", len(valid_sales))
print("Invalid records:", len(invalid_sales))
print("Total valid sales:", valid_sales["amount"].sum())\
    
    # Step 7: Create a validation report
report_path = BASE_DIR / "reports" / "validation_summary.txt"

# Make sure the reports folder exists
report_path.parent.mkdir(parents=True, exist_ok=True)

# Prepare report content
report = f"""
=== ETL VALIDATION REPORT ===
Total Records: {len(df)}
Valid Records: {len(valid_sales)}
Invalid Records: {len(invalid_sales)}
Total Valid Sales: {valid_sales['amount'].sum()}
"""

# Save the report
report_path.write_text(report, encoding="utf-8")

print("\nValidation report saved successfully!")