import pandas as pd

# Creating a mock dataset representing student logs or server metrics
data = {
    'Timestamp': pd.date_range(start='2020-09-01 08:00', periods=6, freq='h'),
    'Server_ID': ['SRV-01', 'SRV-02', 'SRV-01', 'SRV-03', 'SRV-02', 'SRV-01'],
    'CPU_Usage_Pct': [45.2, 88.7, 50.1, 95.4, 72.3, 91.0],
    'Memory_Usage_Pct': [60.5, 78.2, 63.4, 91.2, 70.1, 85.6],
    'Status': ['OK', 'WARNING', 'OK', 'CRITICAL', 'WARNING', 'CRITICAL']
}

def run_filters():
    df = pd.DataFrame(data)
    
    print("=== Complete System Metrics ===")
    print(df)
    
    # 1. Boolean Indexing: Filter for critical state or high CPU usage
    print("\n--- High Alert Servers (CPU > 80% or Status == CRITICAL) ---")
    high_alert = df[(df['CPU_Usage_Pct'] > 80.0) | (df['Status'] == 'CRITICAL')]
    print(high_alert)
    
    # 2. Filtering by specific server
    print("\n--- History of SRV-01 ---")
    srv_01 = df[df['Server_ID'] == 'SRV-01']
    print(srv_01)
    
    # 3. Using .loc to filter and select specific columns
    print("\n--- Alert Server Performance Columns ---")
    alert_metrics = df.loc[df['CPU_Usage_Pct'] > 70.0, ['Server_ID', 'CPU_Usage_Pct', 'Status']]
    print(alert_metrics)

if __name__ == "__main__":
    run_filters()
