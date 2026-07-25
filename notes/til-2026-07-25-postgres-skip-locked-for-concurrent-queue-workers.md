# Postgres SKIP LOCKED for Concurrent Queue Workers

Using a relational database as a task queue often leads to lock contention and serialization bottlenecks when multiple workers attempt to poll the same table. PostgreSQL's `SELECT ... FOR UPDATE SKIP LOCKED` clause solves this by allowing concurrent transactions to lock and process distinct rows simultaneously, bypassing already-locked rows instead of blocking. This enables the construction of high-throughput, ACID-compliant message queues directly within an existing database without the operational overhead of dedicated brokers like RabbitMQ or SQS.

## Key Takeaways
- **Eliminates Head-of-Line Blocking:** Workers immediately skip rows currently being processed by other active transactions, preventing idle worker threads and maximizing processing throughput.
- **ACID-Compliant Queueing:** By wrapping the poll and update operations in a single transaction, tasks are guaranteed to be processed exactly-once (or at-least-once with retries) without risking race conditions.
- **Operational Simplicity:** Eliminates the need to deploy, monitor, and pay for external queueing infrastructure for moderate-to-high-volume workloads up to thousands of tasks per second.

## Code Example
```sql
-- Assume a task queue table structured as follows:
-- CREATE TABLE task_queue (
--     id BIGSERIAL PRIMARY KEY,
--     payload JSONB NOT NULL,
--     status VARCHAR(20) DEFAULT 'pending',
--     locked_at TIMESTAMP WITH TIME ZONE
-- );

-- An atomic worker query to fetch, lock, and transition the next available task
BEGIN;

UPDATE task_queue
SET 
    status = 'processing',
    locked_at = clock_timestamp()
WHERE id = (
    SELECT id 
    FROM task_queue
    WHERE status = 'pending'
    ORDER BY id ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
RETURNING id, payload;

-- The worker processes the payload in application code, then commits the transaction:
COMMIT;
```

---
*Logged on 2026-03-30 08:20:00 (UTC)*
