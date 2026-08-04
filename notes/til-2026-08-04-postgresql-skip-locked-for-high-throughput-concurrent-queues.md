# PostgreSQL `SKIP LOCKED` for High-Throughput Concurrent Queues

PostgreSQL allows developers to build robust, concurrent task queues directly inside the database using the `SELECT ... FOR UPDATE SKIP LOCKED` clause. This mechanism enables multiple worker processes to safely poll the same queue table and lock unique rows without blocking each other or causing deadlocks. By bypassing locked rows instead of waiting for them, it eliminates database contention and allows for high-throughput message processing without the operational overhead of a dedicated message broker like RabbitMQ or SQS.

## Key Takeaways
- **Non-Blocking Concurrency:** The `SKIP LOCKED` modifier instructs PostgreSQL to completely ignore rows that are already locked by other active transactions, allowing workers to find and lock the next available task instantly.
- **Atomic State Transitions:** Combining `FOR UPDATE SKIP LOCKED` with an `UPDATE ... RETURNING` statement allows a worker to fetch, lock, and transition a task's state in a single, atomic database round-trip.
- **Simplified Architecture:** This pattern provides robust "exactly-once" delivery semantics (within the scope of the database transaction) and automatic fault tolerance—if a worker crashes, its transaction rolls back, and the task immediately becomes visible to other workers.

## Code Example

```sql
-- 1. Define a robust queue table schema
CREATE TABLE task_queue (
    id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed')),
    locked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index to optimize queue polling performance
CREATE INDEX idx_task_queue_poll 
ON task_queue (id ASC) 
WHERE status = 'queued';

-- 2. Atomic worker query to safely claim and lock the next available task
UPDATE task_queue
SET 
    status = 'processing', 
    locked_at = NOW()
WHERE id = (
    SELECT id
    FROM task_queue
    WHERE status = 'queued'
    ORDER BY id ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
RETURNING id, payload;
```

---
*Logged on 2026-03-31 01:12:00 (UTC)*
