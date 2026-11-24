import pandas as pd


def validate_sales(df):
    # Make a copy of the original data
    data = df.copy()

    # Check missing customer names
    missing_customer = (
        data["customer_name"].fillna("").str.strip() == ""
    )

    # Check missing product names
    missing_product = (
        data["product"].fillna("").str.strip() == ""
    )

    # Check duplicate transaction IDs
    duplicate_id = data["transaction_id"].duplicated()

    # Convert amount to numeric
    amounts = pd.to_numeric(
        data["amount"],
        errors="coerce"
    )

    # Check invalid amounts
    invalid_amount = amounts.isna() | (amounts <= 0)

    # Combine validation conditions
    has_issue = (
        missing_customer
        | missing_product
        | duplicate_id
        | invalid_amount
    )

    # Create issue descriptions
    data["issues"] = ""

    data.loc[missing_customer, "issues"] += "Missing customer; "
    data.loc[missing_product, "issues"] += "Missing product; "
    data.loc[duplicate_id, "issues"] += "Duplicate ID; "
    data.loc[invalid_amount, "issues"] += "Invalid amount; "

    # Split valid and invalid records
    valid = data.loc[~has_issue].copy()
    invalid = data.loc[has_issue].copy()

    # Generate summary
    summary = {
        "total_records": len(data),
        "valid_records": len(valid),
        "invalid_records": len(invalid),
        "missing_customers": int(missing_customer.sum()),
        "missing_products": int(missing_product.sum()),
        "duplicate_ids": int(duplicate_id.sum()),
        "invalid_amounts": int(invalid_amount.sum()),
        "total_valid_sales": float(amounts.loc[~has_issue].sum())
    }

    return valid, invalid, summary