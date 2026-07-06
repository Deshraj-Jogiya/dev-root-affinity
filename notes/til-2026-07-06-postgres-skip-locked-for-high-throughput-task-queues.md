# Postgres SKIP LOCKED for High-Throughput Task Queues

Building task queues directly inside a relational database often leads to severe lock contention and performance degradation when multiple concurrent workers attempt to claim jobs. By utilizing PostgreSQL's `SELECT ... FOR UPDATE SKIP LOCKED` clause, workers can lock and acquire the next available task while completely bypassing rows already locked by other active workers. This pattern allows you to build a reliable, atomic, and highly concurrent queueing system directly in your database without the operational complexity of external message brokers like RabbitMQ or Redis.

## Key Takeaways
- **Eliminates Thread Contention:** Traditional `FOR UPDATE` locks force concurrent workers to block and wait for the lock to release; `SKIP LOCKED` instructs the database engine to ignore locked rows and immediately return the next free row.
- **Strict Transactional Guarantees:** Because the lock is tied to the life of the database transaction, if a worker crashes or fails mid-task, the transaction rolls back, releasing the lock and automatically returning the job to the queue.
- **Simplifies Infrastructure:** It allows small-to-medium scale applications to implement reliable "at-least-once" queue semantics using existing Postgres instances, avoiding the overhead of maintaining dedicated queueing infrastructure.

## Code Example

The following SQL demonstrates how to atomicaly claim the next available job in a thread-safe, concurrent-friendly manner:

```sql
-- 1. Create a simple queue table
CREATE TABLE job_queue (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    locked_at TIMESTAMP WITH TIME ZONE
);

-- 2. Concurrently claim a job (Run this inside a transaction block)
BEGIN;

UPDATE job_queue
SET 
    status = 'processing',
    locked_at = NOW()
WHERE id = (
    SELECT id
    FROM job_queue
    WHERE status = 'queued'
    ORDER BY created_at ASC
    FOR UPDATE SKIP LOCKED
    LIMIT 1
)
RETURNING id, payload;

COMMIT;
```

---
*Logged on 2025-05-15 14:23:10 (UTC)*
