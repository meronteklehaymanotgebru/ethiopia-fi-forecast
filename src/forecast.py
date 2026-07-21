"""Forecasting functions for Ethiopia financial inclusion."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import statsmodels.api as sm

REPORTS_DIR = Path("reports/figures")

def forecast_trend_with_events(series: pd.Series, event_dummies: pd.DataFrame,
                               forecast_years: list) -> pd.DataFrame:
    """
    Fit a trend + event dummy regression on the given time series.
    Returns a DataFrame with historical fit and forecast.
    """
    # Create a time index (years)
    years = series.index.year.values
    df = pd.DataFrame({'year': years, 'value': series.values})
    df = df.join(event_dummies, how='left').fillna(0)
    
    X = sm.add_constant(df[['year'] + list(event_dummies.columns)])
    model = sm.OLS(df['value'], X, missing='drop').fit()
    
    # Generate forecast
    future_years = np.array(forecast_years)
    future_X = pd.DataFrame({
        'year': future_years,
        **{col: 1 for col in event_dummies.columns}  # assume events remain active
    })
    future_X = sm.add_constant(future_X, has_constant='add')
    forecasts = model.get_prediction(future_X).summary_frame(alpha=0.05)
    
    result = pd.DataFrame({
        'year': future_years,
        'forecast': forecasts['mean'],
        'lower': forecasts['obs_ci_lower'],
        'upper': forecasts['obs_ci_upper']
    })
    return result, model

def plot_forecast(historical: pd.Series, forecast_df: pd.DataFrame,
                  title: str = 'Forecast') -> str:
    """Plot historical data with forecast and confidence intervals."""
    plt.figure(figsize=(8,5))
    plt.plot(historical.index, historical.values, 'o-', label='Historical')
    plt.plot(forecast_df['year'], forecast_df['forecast'], 's--', label='Forecast')
    plt.fill_between(forecast_df['year'], forecast_df['lower'], forecast_df['upper'],
                     alpha=0.2, label='95% CI')
    plt.title(title)
    plt.legend()
    path = REPORTS_DIR / f"{title.replace(' ','_').lower()}.png"
    plt.savefig(path, dpi=150)
    plt.show()
    return str(path)