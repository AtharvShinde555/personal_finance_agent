import pandas as pd

def detect_anomalies(df):
    """Detects duplicate charges and unusual spending spikes."""
    alerts = []
    debits = df[df['type'].str.lower() == 'debit'].copy()
    
    if debits.empty:
        return alerts
    
    # 1. Detect Duplicate Charges (same date, merchant, and amount)
    if 'date' in debits.columns:
        duplicates = debits[debits.duplicated(subset=['date', 'merchant', 'amount'], keep=False)]
        if not duplicates.empty:
            for _, row in duplicates.drop_duplicates(subset=['merchant', 'amount']).iterrows():
                alerts.append(f"⚠️ **Duplicate Charge Detected:** ₹{row['amount']} at **{row['merchant']}**.")
                
    # 2. Detect Spending Spikes (> 3x average expense)
    avg_expense = debits['amount'].mean()
    spikes = debits[debits['amount'] > (3 * avg_expense)]
    for _, row in spikes.iterrows():
        alerts.append(f"🚨 **High Spending Spike:** ₹{row['amount']} spent at **{row['merchant']}** (exceeds 3x average transaction).")
        
    return alerts

def detect_unused_subscriptions(df):
    """Flags active subscriptions and calculates potential annual savings."""
    sub_alerts = []
    subs = df[df['category'] == 'Subscriptions']
    
    if not subs.empty:
        total_sub_cost = subs['amount'].sum()
        annual_savings = total_sub_cost * 12
        sub_list = ", ".join(subs['merchant'].unique())
        sub_alerts.append(
            f"💡 **Subscription Intelligence:** Active subscriptions found ({sub_list}) totaling ₹{total_sub_cost}/month. "
            f"Canceling unused plans could save up to **₹{annual_savings:,.2f}/year**."
        )
        
    return sub_alerts
