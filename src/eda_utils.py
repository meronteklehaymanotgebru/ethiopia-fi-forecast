"""Reusable EDA plotting and analysis functions."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports" / "figures"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def plot_account_ownership(obs: pd.DataFrame) -> str:
    """Plot and save account ownership trend. Returns the file path."""
    acc = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].sort_values("observation_date")
    if acc.empty:
        print("No ACC_OWNERSHIP data found.")
        return ""

    plt.figure(figsize=(8, 4))
    plt.plot(acc["observation_date"], acc["value_numeric"], marker="o", linewidth=2)
    plt.title("Account Ownership Rate in Ethiopia (2011-2024)")
    plt.ylabel("Share of adults (%)")
    plt.xlabel("Year")
    plt.grid(True)
    path = REPORTS_DIR / "account_ownership.png"
    plt.savefig(path, dpi=150)
    plt.show()
    print(f"Saved {path}")
    return str(path)


def plot_digital_usage(obs: pd.DataFrame) -> str:
    """Plot mobile money & digital payment usage. Returns the file path."""
    mm = obs[obs["indicator_code"] == "ACC_MM_ACCOUNT"]
    digital = obs[obs["indicator_code"] == "USG_DIGITAL_PAYMENT"]
    if mm.empty and digital.empty:
        print("No digital usage data found.")
        return ""

    plt.figure(figsize=(8, 4))
    if not mm.empty:
        plt.plot(mm["observation_date"], mm["value_numeric"], marker="s", label="Mobile Money Account")
    if not digital.empty:
        plt.plot(digital["observation_date"], digital["value_numeric"], marker="^", label="Made/Received Digital Payment")
    plt.legend()
    plt.title("Digital Financial Usage")
    plt.ylabel("Share of adults (%)")
    path = REPORTS_DIR / "digital_usage.png"
    plt.savefig(path, dpi=150)
    plt.show()
    print(f"Saved {path}")
    return str(path)


def plot_event_timeline(obs: pd.DataFrame, df_enriched: pd.DataFrame) -> str:
    """Overlay events on the account ownership chart. Returns the file path."""
    acc = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].sort_values("observation_date")
    events = df_enriched[df_enriched["record_type"] == "event"].copy()
    events["event_date"] = pd.to_datetime(events["observation_date"])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(acc["observation_date"], acc["value_numeric"], marker="o", label="Account Ownership")
    for _, ev in events.iterrows():
        ax.axvline(ev["event_date"], color="gray", linestyle="--", alpha=0.7)
        label = str(ev.get("event_name", ev.get("indicator", f"Event {ev['record_id']}")))[:25]
        ax.text(ev["event_date"], ax.get_ylim()[1] * 0.95, label, rotation=90, fontsize=8)
    ax.set_title("Account Ownership with Key Events")
    ax.legend()
    plt.tight_layout()
    path = REPORTS_DIR / "events_timeline.png"
    plt.savefig(path, dpi=150)
    plt.show()
    print(f"Saved {path}")
    return str(path)


def plot_correlation_heatmap(obs: pd.DataFrame) -> str:
    """Plot a correlation heatmap of numeric indicators. Returns the file path."""
    wide = obs.pivot_table(index="observation_date", columns="indicator_code", values="value_numeric")
    if wide.shape[1] < 2:
        print("Not enough indicators for correlation heatmap.")
        return ""
    corr = wide.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
    plt.title("Indicator Correlations")
    path = REPORTS_DIR / "correlation_heatmap.png"
    plt.savefig(path, dpi=150)
    plt.show()
    print(f"Saved {path}")
    return str(path)