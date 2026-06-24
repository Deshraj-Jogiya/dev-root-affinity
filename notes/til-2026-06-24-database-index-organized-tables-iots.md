# Database Index-Organized Tables (IOTs)

An Index-Organized Table (IOT) is a database structure where the table data itself is stored within the B-tree index structure rather than in a separate heap file. By co-locating the row data with the primary key, IOTs eliminate the need for an extra lookup step (a "rowid" fetch) when accessing data by the primary key, significantly reducing I/O overhead for point queries.

## Key Takeaways
- **Reduced I/O:** Since the primary key and the row data reside in the same leaf block, a single index traversal retrieves the entire record.
- **Cache Efficiency:** IOTs improve buffer cache hit ratios because they eliminate the need to maintain separate data pages and index pages for the same logical record.
- **Trade-offs:** While excellent for primary key-based lookups, IOTs can incur a performance penalty for secondary index lookups, as secondary indexes must store a logical row identifier (a primary key) rather than a physical rowid.

## Code Example

In Oracle SQL, you define an IOT by using the `ORGANIZATION INDEX` clause during table creation. This ensures the table data is physically stored in the B-tree structure.

```sql
-- Creating an Index-Organized Table for high-performance key-based lookups
CREATE TABLE user_sessions (
    session_id VARCHAR2(64) PRIMARY KEY,
    user_id    NUMBER,
    data       BLOB,
    created_at TIMESTAMP
) 
ORGANIZATION INDEX
PCTTHRESHOLD 20 -- Move columns exceeding 20% of block size to an overflow segment
INCLUDING user_id;
```

---
*Logged on 2024-05-22 14:35:12 (UTC)*
