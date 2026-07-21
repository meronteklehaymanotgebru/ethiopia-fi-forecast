"""Event impact modeling utilities for Ethiopia FI forecasting."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

REPORTS_DIR = Path("reports/figures")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Extract and validate impact_link records."""
    links = df[df['record_type'] == 'impact_link'].copy()
    if links.empty:
        print("Warning: No impact_link records found.")
    return links

def build_association_matrix(links: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create an event-indicator matrix with numeric impact values.
    Maps 'high'→3, 'medium'→2, 'low'→1.
    """
    # Map text to numeric
    mapping = {'high': 3, 'medium': 2, 'low': 1}
    links['impact_magnitude'] = links['impact_magnitude'].replace(mapping)
    # If still string, coerce to float
    links['impact_magnitude'] = pd.to_numeric(links['impact_magnitude'], errors='coerce').fillna(0)

    event_label_col = 'event_name' if 'event_name' in events_df.columns else 'indicator'
    event_cols = ['record_id', event_label_col]
    available_cols = [col for col in event_cols if col in events_df.columns]

    merged = links.merge(events_df[available_cols],
                         left_on='parent_id', right_on='record_id',
                         how='left', suffixes=('', '_event'))
    if merged.empty:
        print("No links could be joined with events.")
        return pd.DataFrame()

    merged['event_name'] = merged[event_label_col]
    pivot = merged.pivot_table(
        index='event_name',
        columns='related_indicator',
        values='impact_magnitude',
        aggfunc='first'
    )
    return pivot.fillna(0)
def plot_association_heatmap(matrix: pd.DataFrame) -> str:
    """Save and display a heatmap of the association matrix."""
    if matrix.empty:
        print("Association matrix is empty; cannot plot heatmap.")
        return ""
    plt.figure(figsize=(10, 6))
    sns.heatmap(matrix, annot=True, cmap='coolwarm', center=0, fmt='.1f')
    plt.title('Event-Indicator Association Matrix')
    plt.tight_layout()
    path = REPORTS_DIR / 'association_matrix.png'
    plt.savefig(path, dpi=150)
    plt.show()
    return str(path)

def create_event_dummies(df_obs: pd.DataFrame, events_df: pd.DataFrame,
                         indicator: str, lag_months: int = 0) -> pd.DataFrame:
    """
    For a given indicator, create dummy variables that turn on after each event date.
    Returns a DataFrame with the original indicator time series and event dummies.
    """
    series = df_obs[df_obs['indicator_code'] == indicator].copy()
    if series.empty:
        print(f"No observations for indicator {indicator}")
        return pd.DataFrame()
    series = series.sort_values('observation_date').set_index('observation_date')
    # Add event dummies
    events_df = events_df.copy()
    events_df['event_date'] = pd.to_datetime(events_df['observation_date'])
    for _, ev in events_df.iterrows():
        col_name = ev.get('event_name', f"event_{ev['record_id']}")[:30]
        # create a boolean column that is 1 after the event date (shifted by lag_months)
        after_date = ev['event_date'] + pd.DateOffset(months=lag_months)
        series[col_name] = (series.index >= after_date).astype(int)
    return series