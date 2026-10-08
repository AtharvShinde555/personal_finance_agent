import pandas as pd

def analyze_spending_patterns(df):
    """Calculates category-wise spending totals."""
    debits = df[df['type'].str.lower() == 'debit']
    category_totals = debits.groupby('category')['amount'].sum().reset_index()
    return category_totals

def forecast_cash_flow(df, current_balance=50000.0, forecast_days=30):
    """Forecasts daily wallet balance over the next 30 days based on net cash flow."""
    total_income = df[df['type'].str.lower() == 'credit']['amount'].sum()
    total_expenses = df[df['type'].str.lower() == 'debit']['amount'].sum()
    net_flow = total_income - total_expenses
    
    num_days = len(df['date'].dt.date.unique()) if 'date' in df.columns else 1
    daily_net = net_flow / max(num_days, 1)
    
    daily_trend = []
    bal = current_balance
    for day in range(1, forecast_days + 1):
        bal += daily_net
        daily_trend.append({"day": f"Day {day}", "projected_balance": round(bal, 2)})
        
    return {
        "projected_savings": round(net_flow, 2),
        "ending_balance": round(bal, 2),
        "daily_trend": pd.DataFrame(daily_trend)
    }