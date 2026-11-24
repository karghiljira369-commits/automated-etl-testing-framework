import pandas as pd
import pytest
from pathlib import Path

from src.validation import validate_sales


# Test 1: Validate the complete sales dataset
def test_sales_validation():
    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "sales_day2.csv"

    df = pd.read_csv(file_path)

    valid, invalid, summary = validate_sales(df)

    assert summary["total_records"] == 14
    assert summary["valid_records"] == 8
    assert summary["invalid_records"] == 6


# Tests 2, 3, 4: Validate invalid sales amounts
@pytest.mark.parametrize("amount", [0, -500, "abc"])
def test_invalid_sales_amount(amount):
    df = pd.DataFrame({
        "transaction_id": [201],
        "customer_name": ["Arun"],
        "product": ["Laptop"],
        "amount": [amount]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["valid_records"] == 0
    assert summary["invalid_records"] == 1
    assert "Invalid amount" in invalid.iloc[0]["issues"]
    
    # Test 5: Missing customer name
def test_missing_customer():
    df = pd.DataFrame({
        "transaction_id": [202],
        "customer_name": [None],
        "product": ["Mouse"],
        "amount": [500]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["invalid_records"] == 1
    assert "Missing customer" in invalid.iloc[0]["issues"]


# Test 6: Missing product name
def test_missing_product():
    df = pd.DataFrame({
        "transaction_id": [203],
        "customer_name": ["Priya"],
        "product": [None],
        "amount": [1000]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["invalid_records"] == 1
    assert "Missing product" in invalid.iloc[0]["issues"]


# Test 7: Duplicate transaction ID
def test_duplicate_transaction_id():
    df = pd.DataFrame({
        "transaction_id": [301, 301],
        "customer_name": ["Arun", "Ravi"],
        "product": ["Laptop", "Mouse"],
        "amount": [45000, 500]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["valid_records"] == 1
    assert summary["invalid_records"] == 1
    assert "Duplicate ID" in invalid.iloc[0]["issues"]
    
    # Test 8: All records are valid
def test_all_valid_sales():
    df = pd.DataFrame({
        "transaction_id": [401, 402],
        "customer_name": ["Arun", "Priya"],
        "product": ["Pen", "Book"],
        "amount": [100, 200]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 2
    assert summary["invalid_records"] == 0
    assert summary["total_valid_sales"] == 300.0
    
    # Test 9: Original DataFrame must remain unchanged
def test_original_data_unchanged():
    df = pd.DataFrame({
        "transaction_id": [501, 502],
        "customer_name": ["Arun", "Priya"],
        "product": ["Laptop", "Mouse"],
        "amount": [45000, -500]
    })

    original_df = df.copy(deep=True)

    validate_sales(df)

    pd.testing.assert_frame_equal(df, original_df)
    
    # Test 10: Detect multiple validation errors
def test_multiple_validation_errors():
    df = pd.DataFrame({
        "transaction_id": [601, 601],
        "customer_name": ["Arun", " "],
        "product": ["Laptop", ""],
        "amount": [45000, 0]
    })

    valid, invalid, summary = validate_sales(df)

    assert summary["valid_records"] == 1
    assert summary["invalid_records"] == 1

    issues = invalid.iloc[0]["issues"]

    assert "Missing customer" in issues
    assert "Missing product" in issues
    assert "Duplicate ID" in issues
    assert "Invalid amount" in issues