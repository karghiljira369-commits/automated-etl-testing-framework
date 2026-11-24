from pathlib import Path
import pandas as pd

from src.validation import validate_sales

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data" / "sales_day2.csv")

valid, invalid, summary = validate_sales(df)

print(summary)