import pandas as pd

def calculate_health_score(df):
    """Calculates a Financial Health Score from 0 to 100 based on savings rate."""
    income = df[df['type'].str.lower() == 'credit']['amount'].sum()
    expenses = df[df['type'].str.lower() == 'debit']['amount'].sum()
    
    if income == 0:
        return 50  # Baseline score if no income recorded
    
    savings_rate = ((income - expenses) / income) * 100
    
    if savings_rate >= 30:
        score = 88
    elif savings_rate >= 15:
        score = 75
    elif savings_rate >= 0:
        score = 62
    else:
        score = 42
        
    if (expenses / income) > 0.8:
        score -= 10
        
    return max(min(score, 100), 0)
