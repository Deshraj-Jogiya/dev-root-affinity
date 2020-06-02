import pandas as pd
import io

# Simulated raw CSV data representing remote study metrics during 2020 lockdown
csv_data = """Date,Subject,HoursStudied,SessionsCompleted,FocusScore
2020-04-01,Python Programming,4.5,3,85
2020-04-01,Algorithms,2.0,1,78
2020-04-02,Database Systems,3.5,2,80
2020-04-02,Python Programming,5.0,4,90
2020-04-03,Algorithms,3.0,2,82
2020-04-03,Web Development,4.0,3,88
2020-04-04,Python Programming,6.0,5,92
2020-04-04,Database Systems,2.5,1,75
"""

def analyze_lockdown_study():
    # Load raw data
    df = pd.read_csv(io.StringIO(csv_data))
    
    # Calculate total and average metrics
    print("=== Raw Study Data ===")
    print(df)
    print("\n=== Summary Stats ===")
    print(f"Total hours studied during this period: {df['HoursStudied'].sum()} hours")
    print(f"Average focus score: {df['FocusScore'].mean():.2f}")
    
    # Filter for high-focus sessions
    print("\n=== High Focus Sessions (Score >= 85) ===")
    high_focus = df[df['FocusScore'] >= 85]
    print(high_focus)
    
    # Group by subject
    print("\n=== Total Study Hours by Subject ===")
    grouped = df.groupby('Subject')['HoursStudied'].sum().reset_index()
    print(grouped)

if __name__ == "__main__":
    analyze_lockdown_study()
