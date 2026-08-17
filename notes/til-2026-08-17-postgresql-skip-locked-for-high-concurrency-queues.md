# PostgreSQL SKIP LOCKED for High-Concurrency Queues

Traditional queue systems often rely on external brokers like Redis or RabbitMQ, which introduces architectural complexity, deployment overhead, and challenges with distributed transactions. By using PostgreSQL's `SELECT ... FOR UPDATE SKIP LOCKED` clause, you can build a highly concurrent, reliable, and transactional queue directly inside your relational database without encountering lock contention. This ensures that concurrent worker processes can fetch and lock distinct pending jobs instantly without blocking each other or processing duplicate records.

## Key Takeaways
- `SKIP LOCKED` allows transactions to bypass rows that are already locked by other active transactions, completely eliminating lock waiting and blocking among parallel workers.
- Combining `FOR UPDATE SKIP LOCKED` with an `UPDATE ... RETURNING` statement inside a single transaction guarantees atomic "fetch-and-lock" operations with exactly-once processing semantics.
- This pattern is highly resilient; if a worker process crashes mid-job, the database transaction rolls back, releasing the row lock and making the job immediately available to other workers without manual dead-letter queue routing.

## Code Example

```sql
-- 1. Create a queue table with an index on the status and ordering column
CREATE TABLE job_queue (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    locked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_job_queue_pending_fetch 
ON job_queue (created_at ASC) 
WHERE status = 'pending';

-- 2. Atomically fetch, lock, and mark the next available job for processing.
-- This query can run concurrently across dozens of worker threads safely.
UPDATE job_queue
SET 
    status = 'processing',
    locked_at = CLOCK_TIMESTAMP()
WHERE id = (
    SELECT id
    FROM job_queue
    WHERE status = 'pending'
    ORDER BY created_at ASC
    FOR UPDATE SKIP LOCKED
    LIMIT 1
)
RETURNING id, payload;
```

---
*Logged on 2024-05-17 18:42:00 (UTC)*
