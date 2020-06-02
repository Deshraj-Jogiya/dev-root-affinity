# Pandas DataFrame Filtering & Boolean Indexing

Data analysis often requires extracting subset rows from a DataFrame that satisfy specific logical conditions. In Python, Pandas provides high-performance filtering features using Boolean Indexing and the `.loc` accessor.

## Core Filtering Techniques

1. **Boolean Indexing**: Passing a boolean Series (obtained by comparing columns to values) to the DataFrame indexer `df[...]`.
   ```python
   # Filters rows where CPU_Usage_Pct is greater than 80
   high_cpu = df[df['CPU_Usage_Pct'] > 80.0]
   ```

2. **Logical Operators**: Combining multiple conditions.
   - Use `&` for element-wise AND (both conditions must be True).
   - Use `|` for element-wise OR (at least one condition must be True).
   - Use `~` for element-wise NOT.
   - *Note*: Always wrap individual conditions in parentheses due to operator precedence rules in Python.

3. **Column Selection with `.loc`**: Combining row filtering and specific column selection in a single operation.
   ```python
   # Retrieves Server_ID and Status for high usage alerts
   alerts = df.loc[df['CPU_Usage_Pct'] > 70.0, ['Server_ID', 'Status']]
   ```

## Practical Example
The complete executable script demonstrating these filtering methods on server performance logs can be found in [pandas_filtering.py](file:///G:/dev-root-affinity/src/2020/pandas_filtering.py).

---
*Logged on 2020-01-06 17:12:00 (UTC)*
