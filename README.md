# Forecasting Financial Inclusion in Ethiopia

[![CI](https://github.com/meronteklehaymanotgebru/ethiopia-fi-forecast/actions/workflows/unittests.yml/badge.svg)](https://github.com/meronteklehaymanotgebru/ethiopia-fi-forecast/actions)

## 1. Business Context

Ethiopia is undergoing a rapid digital financial transformation. Telebirr has grown to over 54 million users since 2021, M‑Pesa entered the market in 2023, and interoperable digital transfers have surpassed ATM withdrawals. Yet only 49% of adults have a financial account (Global Findex 2024). A consortium of stakeholders has engaged Selam Analytics to forecast financial inclusion outcomes for 2025‑2027.

## 2. Project Objectives

- **Task 1** – Enrich the provided dataset with additional observations, events, and impact links.
- **Task 2** – Perform exploratory data analysis and identify key drivers of inclusion.
- **Task 3** – Model the impact of events (policy, product launch, infrastructure) on inclusion indicators.
- **Task 4** – Forecast Account Ownership (Access) and Digital Payment Usage for 2025‑2027.
- **Task 5** – Build an interactive Streamlit dashboard for stakeholders.

## 3. Repository Structure

```
ethiopia-fi-forecast/
├── .github/workflows/          # CI/CD (flake8 + pytest)
├── data/
│   ├── raw/                    # Starter datasets (Excel)
│   └── processed/              # Enriched data (CSV)
├── notebooks/
│   └── eda_and_enrichment.ipynb   # Task 1 & 2 analysis
├── src/
│   ├── data_loader.py          # Data loading & validation
│   └── eda_utils.py            # Reusable EDA plotting functions
├── dashboard/
│   └── app.py                  # Streamlit dashboard (Task 5)
├── reports/
│   ├── figures/                # Saved PNG figures
│   ├── interim_report.md
│   └── final_report.md
├── tests/
│   └── test_dummy.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 4. Setup & Installation

```bash
git clone https://github.com/meronteklehaymanotgebru/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 5. Running the Analysis

### Jupyter Notebook
```bash
jupyter notebook notebooks/eda_and_enrichment.ipynb
```
Run all cells to reproduce the EDA figures and save the enriched dataset.

### Streamlit Dashboard (Task 5)
```bash
streamlit run dashboard/app.py
```

### CI/CD
GitHub Actions runs `flake8` linting and `pytest` on every push. The workflow is defined in `.github/workflows/unittests.yml`.

## 6. Key Findings

- Account ownership growth slowed to only +3pp (46% → 49%) between 2021‑2024, despite massive mobile money expansion.
- Mobile money accounts tripled from 4.7% to 9.45% after Telebirr and M‑Pesa launches.
- Digital payment usage (~35%) lags far behind account ownership (49%), indicating a registration‑active usage gap.
- Infrastructure (4G coverage, agent density) and gender parity are critical enablers.

## 7. Data Enrichment Log

All added records are documented in `data_enrichment_log.md` with source, original text, confidence, and rationale.

## 8. References

- Global Findex Database
- GSMA State of the Industry Report
- National Bank of Ethiopia
- Ethio Telecom reports
