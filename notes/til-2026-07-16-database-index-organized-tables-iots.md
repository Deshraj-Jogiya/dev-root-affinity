# Database Index-Organized Tables (IOTs)

An Index-Organized Table (IOT) is a database structure where the table data itself is stored within the B-tree index of the primary key, rather than in a separate heap-organized structure. This architecture eliminates the need for a secondary lookup from the index to the table row, significantly reducing I/O overhead for primary key-based lookups and range scans.

## Key Takeaways
- **Reduced I/O:** By co-locating the data with the index, you eliminate the "fetch" step required in traditional heap tables, turning a two-step retrieval process into a single index traversal.
- **Improved Cache Locality:** Since the index blocks contain the actual row data, spatial locality is improved, leading to better buffer cache hit rates during primary key lookups.
- **Storage Trade-offs:** While IOTs excel at point lookups, they can lead to increased leaf block contention and potential fragmentation if the primary key is not strictly monotonic, making them best suited for static or append-heavy datasets.

## Code Example

```sql
-- Creating an Index-Organized Table in Oracle/MySQL (InnoDB via PRIMARY KEY)
-- In InnoDB, all tables are inherently IOTs because the data is clustered 
-- by the primary key by default.

CREATE TABLE sensor_readings (
    reading_id BIGINT NOT NULL,
    sensor_id INT NOT NULL,
    value DECIMAL(10, 2),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (reading_id)
) ENGINE=InnoDB;

-- The data for 'reading_id = 500' is retrieved directly from the leaf node 
-- of the primary key B-tree, requiring no additional pointer follow.
SELECT * FROM sensor_readings WHERE reading_id = 500;
```

---
*Logged on 2025-05-14 14:32:10 (UTC)*
