"""
Streamlit dashboard for Ethiopia Financial Inclusion Forecasting.
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

df = load_unified_data()
obs = df[df['record_type'] == 'observation']
events = df[df['record_type'] == 'event']

# Sidebar
indicator = st.sidebar.selectbox(
    "Select indicator:",
    ['ACC_OWNERSHIP', 'ACC_MM_ACCOUNT', 'USG_DIGITAL_PAYMENT']
)

# Filter data
ind_data = obs[obs['indicator_code'] == indicator].set_index('observation_date')['value_numeric']
ind_data = ind_data.sort_index()

# --- Historical chart ---
st.subheader(f"{indicator} – Historical Trend")
fig, ax = plt.subplots()
ax.plot(ind_data.index, ind_data.values, 'o-')
st.pyplot(fig)

# --- Simple forecast ---
st.subheader("Forecast 2025‑2027 (Trend‑Only)")
try:
    from sklearn.linear_model import LinearRegression
    X = np.array([d.year for d in ind_data.index]).reshape(-1, 1)
    y = ind_data.values
    lr = LinearRegression().fit(X, y)
    future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
    pred = lr.predict(future_years)
    forecast_df = pd.DataFrame({'Year': [2025, 2026, 2027], 'Forecast': pred})
    st.dataframe(forecast_df)
    fig2, ax2 = plt.subplots()
    ax2.plot(ind_data.index, y, 'o-')
    ax2.plot([2025, 2026, 2027], pred, 's--')
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Forecast failed: {e}")

# --- Events table ---
st.subheader("Key Events")
events_display = events[['indicator', 'observation_date']].dropna()
st.dataframe(events_display)