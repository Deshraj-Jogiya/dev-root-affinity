# PostgreSQL SKIP LOCKED for High-Throughput Concurrent Queues

Using a relational database as a task queue is a common pattern that often suffers from severe performance bottlenecks due to lock contention. PostgreSQL solves this elegantly using the `SELECT ... FOR UPDATE SKIP LOCKED` syntax, which allows concurrent worker processes to safely poll a task table and lock distinct rows without blocking one another. This feature transforms Postgres into a highly reliable, transactional message broker capable of handling significant throughput with strict ACID guarantees.

## Key Takeaways
- **Eliminates Lock Contention:** Unlike standard locking mechanisms that force concurrent transactions to wait for a locked row to be released, `SKIP LOCKED` instructs Postgres to silently bypass already-locked rows and find the next available one.
- **Transactional Safety:** Because the lock is tied to the lifecycle of the database transaction, if a worker crashes mid-task, the transaction rolls back, the lock is automatically released, and the task instantly becomes available to other workers.
- **Strict Ordering with Limits:** Combining `ORDER BY` and `LIMIT 1` with `FOR UPDATE SKIP LOCKED` ensures that workers process tasks in the exact intended priority or chronological order without stepping on each other's toes.

## Code Example

The following SQL demonstrates how to atomically claim the next available "pending" task in a highly concurrent environment using a single, non-blocking transaction:

```sql
-- Assume a task queue table structured as follows:
-- CREATE TABLE task_queue (
--     id BIGSERIAL PRIMARY KEY,
--     payload JSONB NOT NULL,
--     status VARCHAR(20) DEFAULT 'pending',
--     claimed_at TIMESTAMP WITH TIME ZONE
-- );

BEGIN;

-- Atomically claim and lock the oldest pending task
UPDATE task_queue
SET 
    status = 'processing',
    claimed_at = CLOCK_TIMESTAMP()
WHERE id = (
    SELECT id 
    FROM task_queue
    WHERE status = 'pending'
    ORDER BY id ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
RETURNING id, payload;

-- If a row is returned, process the payload in your application code, 
-- then execute COMMIT to release the lock and finalize the state change.
COMMIT;
```

---
*Logged on 2025-02-15 08:32:14 (UTC)*
