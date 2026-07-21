"""
Streamlit dashboard for Ethiopia Financial Inclusion Forecasting.
Sections: Overview, Trends, Forecasts, Inclusion Projections.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '.')
from src.data_loader import load_unified_data

st.set_page_config(page_title="Ethiopia FI Forecast", layout="wide")
st.title("Ethiopia Financial Inclusion Forecasting")
st.markdown("### By Selam Analytics — July 2026")

df = load_unified_data()
obs = df[df['record_type'] == 'observation']
events = df[df['record_type'] == 'event']

# Sidebar for section navigation
section = st.sidebar.radio(
    "Navigate to:",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"]
)

# =================== OVERVIEW ===================
if section == "Overview":
    st.header("Key Metrics at a Glance")
    col1, col2, col3 = st.columns(3)
    # Latest account ownership
    acc = obs[obs['indicator_code'] == 'ACC_OWNERSHIP']
    latest_acc = acc[acc['observation_date'] == acc['observation_date'].max()]['value_numeric']
    val_acc = latest_acc.values[0] if not latest_acc.empty else 0
    col1.metric("Account Ownership (2024)", f"{val_acc}%")

    # Mobile money accounts
    mm = obs[obs['indicator_code'] == 'ACC_MM_ACCOUNT']
    latest_mm = mm[mm['observation_date'] == mm['observation_date'].max()]['value_numeric']
    val_mm = latest_mm.values[0] if not latest_mm.empty else 0
    col2.metric("Mobile Money Accounts (2024)", f"{val_mm}%")

    # Digital payment usage
    dig = obs[obs['indicator_code'] == 'USG_DIGITAL_PAYMENT']
    latest_dig = dig[dig['observation_date'] == dig['observation_date'].max()]['value_numeric']
    val_dig = latest_dig.values[0] if not latest_dig.empty else 0
    col3.metric("Digital Payment Usage (2024)", f"{val_dig}%")

    st.subheader("Recent Events")
    events_display = events[['indicator', 'observation_date']].dropna().sort_values('observation_date', ascending=False)
    st.dataframe(events_display, use_container_width=True)

# =================== TRENDS ===================
elif section == "Trends":
    st.header("Historical Trends")
    indicator = st.selectbox("Select indicator:", 
                             ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT',
                              'ACC_4G_COV', 'GEN_GAP_ACC'])
    
    ind_data = obs[obs['indicator_code'] == indicator].set_index('observation_date')['value_numeric'].sort_index()
    if not ind_data.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(ind_data.index, ind_data.values, 'o-', markersize=6)
        ax.set_title(f"{indicator} Trend")
        ax.set_ylabel("Value")
        ax.grid(True)
        st.pyplot(fig)
        st.caption(f"Data points: {len(ind_data)} | Source: Global Findex, enriched dataset")
    else:
        st.warning("No data available for this indicator.")

# =================== FORECASTS ===================
elif section == "Forecasts":
    st.header("Forecasts 2025‑2027")
    indicator = st.selectbox("Select indicator:", ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT'])
    
    ind_data = obs[obs['indicator_code'] == indicator].set_index('observation_date')['value_numeric'].sort_index()
    if not ind_data.empty:
        # Simple linear trend forecast with placeholder confidence bands
        from sklearn.linear_model import LinearRegression
        X = np.array([d.year for d in ind_data.index]).reshape(-1, 1)
        y = ind_data.values
        lr = LinearRegression().fit(X, y)
        future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
        pred = lr.predict(future_years)
        
        # Approximate confidence interval based on residual std
        residuals = y - lr.predict(X)
        std_res = np.std(residuals)
        ci = 1.96 * std_res  # 95% CI
        
        forecast_df = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Forecast': pred,
            'Lower': pred - ci,
            'Upper': pred + ci
        })
        st.dataframe(forecast_df.style.format("{:.2f}"), use_container_width=True)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(ind_data.index, y, 'o-', label='Historical')
        ax.plot([2025, 2026, 2027], pred, 's--', label='Forecast')
        ax.fill_between([2025, 2026, 2027], pred - ci, pred + ci, alpha=0.2, label='95% CI')
        ax.set_title(f"{indicator} Forecast")
        ax.set_ylabel("Value")
        ax.legend()
        st.pyplot(fig)
        st.caption("Simple trend model with ±1.96 residual std as approximate CI. Based on limited data points.")
    else:
        st.warning("Insufficient data for forecasting.")

# =================== INCLUSION PROJECTIONS ===================
else:
    st.header("Inclusion Projections")
    st.subheader("Progress toward NFIS‑II 60% target")
    # Hardcoded values from the forecast
    projections = pd.DataFrame({
        'Year': [2024, 2025, 2026, 2027],
        'Account Ownership': [49, 51.5, 53.5, 55.5],
        'Target': [60, 60, 60, 60]
    })
    st.dataframe(projections.set_index('Year'), use_container_width=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(projections['Year'], projections['Account Ownership'], 'o-', label='Projected')
    ax.plot(projections['Year'], projections['Target'], 'r--', label='NFIS‑II Target (60%)')
    ax.set_ylabel("Account Ownership (%)")
    ax.legend()
    ax.set_title("Gap to NFIS‑II 60% Target")
    st.pyplot(fig)
    st.caption("Projections are based on a linear trend model. Wide uncertainty remains.")
    
    st.subheader("Scenario Analysis")
    scenario = st.selectbox("Select scenario:", ["Baseline", "Optimistic", "Pessimistic"])
    scenario_vals = {
        'Baseline': [49, 51.5, 53.5, 55.5],
        'Optimistic': [49, 53, 57, 61],
        'Pessimistic': [49, 48, 47, 46]
    }
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot([2024, 2025, 2026, 2027], scenario_vals[scenario], 'o-')
    ax2.set_title(f"{scenario} Scenario – Account Ownership")
    ax2.set_ylabel("Account Ownership (%)")
    ax2.set_ylim(40, 65)
    st.pyplot(fig2)