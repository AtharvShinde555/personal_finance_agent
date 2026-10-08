import os
import json
from openai import OpenAI

def generate_advice(df, health_score):
    """Generates proactive financial coaching advice using Groq API with fallback rules."""
    api_key = os.getenv("GROQ_API_KEY")
    
    income = df[df['type'].str.lower() == 'credit']['amount'].sum()
    expenses = df[df['type'].str.lower() == 'debit']['amount'].sum()
    top_category = df[df['type'].str.lower() == 'debit'].groupby('category')['amount'].sum().idxmax() if not df.empty else "Miscellaneous"
    
    prompt = (
        f"You are an AI Personal CFO and Financial Wellness Coach. "
        f"The user has a Financial Health Score of {health_score}/100. "
        f"Total Income: ₹{income}, Total Expenses: ₹{expenses}. "
        f"Their highest spending category is '{top_category}'. "
        f"Provide 3 concise, highly actionable savings recommendations to improve their financial health."
    )

    if api_key and api_key != "your_groq_api_key_here":
        try:
            client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a top-tier financial advisor. Be concise, direct, and actionable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception:
            pass  # Fall back to rule-based engine if API key is invalid or fails

    # Rule-Based Advisor Fallback
    advice_points = [
        f"💡 **Optimize Highest Expense Category:** Your primary expense driver is **{top_category}**. Reducing this by 15% will increase your annual savings.",
        f"🎯 **Boost Emergency Fund:** Maintain at least 3 to 6 months of expenses (₹{expenses * 3:,.2f}) in a high-yield liquid account.",
        "📊 **Automated Wealth Building:** Set up an automated recurring SIP on salary credit days to ensure you save before discretionary spending."
    ]
    return "\n\n".join(advice_points)

def simulate_life_event(event_cost, cash_flow_forecast):
    """Simulates the impact of major purchase or life event on cash flow."""
    current_savings = cash_flow_forecast.get("projected_savings", 0)
    ending_balance = cash_flow_forecast.get("ending_balance", 50000)
    
    post_purchase_balance = ending_balance - event_cost
    
    if post_purchase_balance >= 20000:
        status = "✅ **Safe Investment:** Your financial buffer remains healthy post-purchase."
    elif post_purchase_balance >= 0:
        status = "⚠️ **Tight Liquidity Alert:** This purchase leaves a minimal cash buffer. Consider financing or deferring."
    else:
        status = "🚨 **High Deficit Risk:** This purchase exceeds your available liquid balance and will create debt."
        
    return {
        "event_cost": event_cost,
        "post_purchase_balance": round(post_purchase_balance, 2),
        "status_message": status
    }
