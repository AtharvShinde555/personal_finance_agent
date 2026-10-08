import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

# Import multi-agent modules
from modules import (
    ingestion_agent,
    categorization_agent,
    analytics_agent,
    anomaly_sub_agent,
    budget_health_agent,
    advisor_agent
)

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="FinOps AI | Autonomous Personal Finance Agent",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Corporate CSS Injection
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Global Typography & Font Family */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Banner Styling */
    .header-box {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        color: #F8FAFC;
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .header-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 6px;
        font-weight: 400;
    }
    .badge-tag {
        background-color: #3B82F6;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-left: 12px;
    }
    
    /* Executive Metric KPI Card Styling */
    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .kpi-title {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        color: #F8FAFC;
        font-size: 1.75rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .kpi-sub-positive {
        color: #10B981;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 2px;
    }
    .kpi-sub-alert {
        color: #F43F5E;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 2px;
    }

    /* Clean Streamlit Tab Tweaks */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Hide Streamlit Default Footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar: Control Panel & Ingestion
# ---------------------------------------------------------
st.sidebar.markdown("### 🏛️ Financial Control Panel")
st.sidebar.caption("PS-05 Autonomous AI Finance Agent")
st.sidebar.markdown("---")

st.sidebar.subheader("📁 Statement Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Bank Statement (.CSV)", type=["csv"])

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom statement ingested successfully!")
else:
    df_raw = ingestion_agent.load_bank_statement()
    st.sidebar.info("Using default dataset (`data/sample_statement.csv`).")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ System Settings")
demo_balance = st.sidebar.number_input("Starting Account Balance (₹):", value=50000, step=5000)

# Process dataset through Multi-Agent pipeline
df_categorized = categorization_agent.categorize_dataframe(df_raw)
health_score = budget_health_agent.calculate_health_score(df_categorized)
anomalies = anomaly_sub_agent.detect_anomalies(df_categorized)
sub_insights = anomaly_sub_agent.detect_unused_subscriptions(df_categorized)
cash_flow = analytics_agent.forecast_cash_flow(df_categorized, current_balance=demo_balance)

# ---------------------------------------------------------
# Main Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div style="display: flex; align-items: center;">
        <h1 class="header-title">FinOps AI Advisor</h1>
        <span class="badge-tag">Active CFO Engine</span>
    </div>
    <p class="header-subtitle">Autonomous Financial Intelligence, Cash Flow Analytics & Anomaly Protection System</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Executive KPI Row
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Financial Health Score</div>
        <div class="kpi-value">{health_score} <span style="font-size: 1rem; color: #94A3B8;">/ 100</span></div>
        <div class="kpi-sub-positive">▲ +4 pts vs prior period</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    savings_val = cash_flow['projected_savings']
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Net Cash Flow</div>
        <div class="kpi-value">₹{savings_val:,.2f}</div>
        <div class="kpi-sub-positive">Projected Monthly Savings</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    num_alerts = len(anomalies)
    sub_class = "kpi-sub-alert" if num_alerts > 0 else "kpi-sub-positive"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Security & Anomalies</div>
        <div class="kpi-value">{num_alerts} Flagged</div>
        <div class="{sub_class}">Requires Attention</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    num_subs = len(df_categorized[df_categorized['category'] == 'Subscriptions'])
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Active Recurring Plans</div>
        <div class="kpi-value">{num_subs} Subscriptions</div>
        <div class="kpi-sub-positive">Auto-Debit Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive Agent Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Cash Flow & Analytics", 
    "🚨 Proactive Alerts & Security", 
    "💡 AI CFO Advisory", 
    "🔮 Life Event Simulator"
])

# ---------------------------------------------------------
# Tab 1: Analytics & Interactive Charts
# ---------------------------------------------------------
with tab1:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        with st.container(border=True):
            st.markdown("### 🍩 Category Expense Breakdown")
            debits = df_categorized[df_categorized['type'].str.lower() == 'debit']
            if not debits.empty:
                cat_summary = debits.groupby('category')['amount'].sum().reset_index()
                fig_pie = px.pie(
                    cat_summary, 
                    values='amount', 
                    names='category', 
                    hole=0.5,
                    color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6', '#64748B']
                )
                fig_pie.update_layout(
                    margin=dict(t=20, b=20, l=20, r=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No debit transactions recorded.")
                
    with col_right:
        with st.container(border=True):
            st.markdown("### 📉 30-Day Liquidity Forecast")
            trend_df = cash_flow['daily_trend']
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=trend_df['day'], 
                y=trend_df['projected_balance'],
                mode='lines+markers',
                name='Projected Balance',
                line=dict(color='#10B981', width=3),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            fig_line.update_layout(
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#334155')
            )
            st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Proactive Alerts & Security
# ---------------------------------------------------------
with tab2:
    with st.container(border=True):
        st.markdown("### 🛡️ Fraud Detection & Subscription Audit")
        all_alerts = anomalies + sub_insights
        if all_alerts:
            for alert in all_alerts:
                st.warning(alert)
        else:
            st.success("✅ Clean Bill of Financial Health: No duplicate charges or unusual spikes detected.")
            
    with st.container(border=True):
        st.markdown("### 📋 Categorized Transaction Audit Trail")
        st.dataframe(
            df_categorized, 
            column_config={
                "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "date": st.column_config.DateColumn("Transaction Date")
            },
            use_container_width=True,
            hide_index=True
        )

# ---------------------------------------------------------
# Tab 3: AI Financial Coach
# ---------------------------------------------------------
with tab3:
    with st.container(border=True):
        st.markdown("### 🤖 Strategic Financial Recommendations")
        st.caption("Generated by AI CFO Engine based on transaction velocity and health score.")
        
        if st.button("🔄 Refresh Advisory Engine"):
            st.rerun()
            
        advice_output = advisor_agent.generate_advice(df_categorized, health_score)
        st.info(advice_output)

# ---------------------------------------------------------
# Tab 4: Life Event Simulator
# ---------------------------------------------------------
with tab4:
    with st.container(border=True):
        st.markdown("### 🔮 Life Event Scenario Simulator")
        st.write("Test the impact of major capital expenditures (e.g. buying a laptop, car, or taking a vacation) on your liquid buffer before making a decision.")
        
        c_sim1, c_sim2 = st.columns([1, 1])
        
        with c_sim1:
            event_cost = st.slider(
                "Simulated Capital Expense (₹):", 
                min_value=5000, 
                max_value=200000, 
                value=35000, 
                step=5000
            )
            
            simulation = advisor_agent.simulate_life_event(event_cost, cash_flow)
            
        with c_sim2:
            st.markdown(f"#### Impact Analysis for ₹{event_cost:,.2f} Outflow:")
            st.markdown(simulation['status_message'])
            st.metric("Post-Expense Projected Buffer", f"₹{simulation['post_purchase_balance']:,.2f}")