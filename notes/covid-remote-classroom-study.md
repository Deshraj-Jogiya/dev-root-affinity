# COVID-19: Adapting to Remote Learning & Data Analysis

*Logged in May 2020 during the peak quarantine lockdown.*

The shift from in-person engineering lectures to fully remote online classrooms has been a major adjustment. However, the isolation has provided a unique opportunity to deep-dive into Python programming and scripting without distractions.

## Lockdown Study Configuration
To make the most of my time during quarantine, I have established a dedicated learning workflow:
- **Environment:** Transitioned from basic text editors to VS Code and Jupyter Notebooks.
- **Python Setup:** Standardized virtual environments (`venv`) to keep project packages separated.
- **Data Engineering Focus:** Studying Pandas, NumPy, and basic data transformations.

## Building a COVID-19 Case Parser
To apply my data analysis learning to real-world events, I built a lightweight Python script that parses CSV case datasets published by Johns Hopkins University and summarizes daily stats:

```python
import pandas as pd

def summarize_covid_data(csv_url):
    print(f"Fetching data from: {csv_url}")
    # Load dataset
    df = pd.read_csv(csv_url)
    
    # Filter for specific regions of interest
    us_cases = df[df["Country_Region"] == "US"]
    
    # Aggregate stats
    total_confirmed = us_cases["Confirmed"].sum()
    total_deaths = us_cases["Deaths"].sum()
    
    print("=== US DATA SUMMARY ===")
    print(f"Total Confirmed Cases: {total_confirmed:,}")
    print(f"Total Deaths: {total_deaths:,}")
    
    # Group by state
    state_totals = us_cases.groupby("Province_State")["Confirmed"].sum().sort_values(ascending=False)
    print("\nTop 5 States by Cases:")
    print(state_totals.head(5))

# Example run with JHU dataset
csv_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/05-15-2020.csv"
summarize_covid_data(csv_url)
```

## Key Learnings
1. **Vectorized Operations:** Pandas is much faster than running native Python loops because it leverages optimized C under the hood.
2. **Data Cleansing:** Handling missing values (`NaN`) using `fillna()` or `dropna()` is a crucial first step in any data pipeline.
