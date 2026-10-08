import pandas as pd
import os

def load_bank_statement(file_path="data/sample_statement.csv"):
    """Loads CSV bank statement and normalizes columns."""
    if not os.path.exists(file_path):
        return get_sample_data()
    
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower().str.strip()
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
    return df

def get_sample_data():
    """Fallback sample financial data."""
    data = {
        "date": pd.to_datetime(["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-05", "2026-10-06", "2026-10-07"]),
        "merchant": ["Swiggy", "Uber", "Salary Credit", "Netflix", "Electricity Bill", "Swiggy", "Spotify", "Amazon Shopping"],
        "amount": [450.00, 280.00, 85000.00, 649.00, 2100.00, 450.00, 119.00, 4200.00],
        "type": ["debit", "debit", "credit", "debit", "debit", "debit", "debit", "debit"]
    }
    return pd.DataFrame(data)