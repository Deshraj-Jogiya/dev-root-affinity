# PostgreSQL FOR UPDATE SKIP LOCKED for High-Concurrency Task Queues

Building a lightweight distributed task queue directly inside a relational database often introduces severe concurrency bottlenecks due to row-level locking. By default, when multiple worker processes attempt to select and lock the same "pending" task row, they block and wait for the lock to release, drastically reducing system throughput. Using PostgreSQL's `FOR UPDATE SKIP LOCKED` clause allows workers to instantly bypass already-locked rows and claim the next available task, enabling highly concurrent, lock-free queue processing without the operational overhead of an external message broker.

## Key Takeaways
- **Eliminates Thread Blocking:** `SKIP LOCKED` instructs PostgreSQL to silently ignore rows that are currently locked by other transactions, preventing workers from waiting on each other.
- **Ensures Atomic State Transitions:** Combining `FOR UPDATE SKIP LOCKED` within a subquery inside an `UPDATE` statement guarantees that a task is claimed by exactly one worker.
- **Simplifies Infrastructure:** It allows teams to defer adopting dedicated queuing systems (like RabbitMQ or Redis) by leveraging existing ACID-compliant database infrastructure for background processing.

## Code Example
```sql
-- Assume a task queue table defined as:
-- CREATE TABLE task_queue (
--     id BIGSERIAL PRIMARY KEY,
--     payload JSONB NOT NULL,
--     status VARCHAR(20) DEFAULT 'pending',
--     claimed_at TIMESTAMP WITH TIME ZONE,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Atomically claim the next available pending task for a worker
UPDATE task_queue
SET 
    status = 'processing',
    claimed_at = CLOCK_TIMESTAMP()
WHERE id = (
    SELECT id
    FROM task_queue
    WHERE status = 'pending'
    ORDER BY created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
RETURNING id, payload;
```

---
*Logged on 2026-03-01 16:00:00 (UTC)*
