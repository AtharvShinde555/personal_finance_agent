import pandas as pd

# Rule-based categorization mapping
CATEGORY_MAPPING = {
    "swiggy": "Food & Dining",
    "zomato": "Food & Dining",
    "uber": "Transportation",
    "ola": "Transportation",
    "netflix": "Subscriptions",
    "spotify": "Subscriptions",
    "electricity bill": "Utilities",
    "water bill": "Utilities",
    "amazon shopping": "Shopping",
    "flipkart": "Shopping",
    "salary credit": "Income"
}

def categorize_transaction(merchant_name):
    """Maps merchant name to financial category."""
    merchant_lower = str(merchant_name).lower().strip()
    for key, category in CATEGORY_MAPPING.items():
        if key in merchant_lower:
            return category
    return "Miscellaneous"

def categorize_dataframe(df):
    """Adds category column to bank statement DataFrame."""
    df_copy = df.copy()
    df_copy['category'] = df_copy['merchant'].apply(categorize_transaction)
    return df_copy