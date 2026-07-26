# PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED` for Lock-Free Task Queues

When building distributed task queues directly in PostgreSQL, concurrent workers can easily cause row contention and lock serialization if using standard transaction locks. By leveraging the `SKIP LOCKED` clause in a `SELECT ... FOR UPDATE` query, worker processes can safely fetch and lock the next available task without blocking other workers. This allows for highly concurrent, low-latency queueing systems directly on top of an existing relational database without needing dedicated brokers like RabbitMQ or Redis.

## Key Takeaways
- **Eliminates Worker Blocking:** `SKIP LOCKED` bypasses rows that are already locked by other transactions, preventing worker processes from waiting on each other and maximizing parallel throughput.
- **Ensures Reliable Task Ownership:** Combining `FOR UPDATE` with an explicit transaction guarantees that if a worker crashes before committing, the lock is automatically released and the task becomes visible to other workers again.
- **Reduces Operational Overhead:** It allows small-to-medium-scale applications to implement robust queuing mechanisms using their existing relational database, deferring the infrastructure complexity of a dedicated message broker.

## Code Example

The following SQL query demonstrates how to atomically pop the next available task from a queue table using a Common Table Expression (CTE). This pattern ensures that a task is retrieved, locked, and marked as "processing" in a single round-trip:

```sql
-- Assume a table schema: tasks (id SERIAL, payload JSONB, status VARCHAR, locked_at TIMESTAMP)

BEGIN;

WITH next_task AS (
    SELECT id
    FROM tasks
    WHERE status = 'pending'
    ORDER BY created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
UPDATE tasks
SET 
    status = 'processing', 
    locked_at = NOW()
FROM next_task
WHERE tasks.id = next_task.id
RETURNING tasks.id, tasks.payload;

-- Process the payload in your application code, then commit the transaction
COMMIT;
```

---
*Logged on 2026-03-30 14:15:22 (UTC)*
