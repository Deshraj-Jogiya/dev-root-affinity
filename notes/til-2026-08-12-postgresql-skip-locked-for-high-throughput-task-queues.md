# PostgreSQL SKIP LOCKED for High-Throughput Task Queues

When building message queues directly in PostgreSQL, traditional locking mechanisms (`FOR UPDATE`) cause concurrent workers to block each other while waiting for the same row lock, severely limiting throughput. Using `SELECT ... FOR UPDATE SKIP LOCKED` allows workers to instantly bypass locked rows and fetch the next available task in a single atomic operation. This enables highly concurrent, lock-free queue consumers without the overhead of external message brokers like Redis or RabbitMQ.

## Key Takeaways
- **Eliminates Head-of-Line Blocking:** Workers don't wait for locked rows; they skip them immediately to find the next free task, ensuring horizontal scalability.
- **Atomic State Transitions:** Combining `SKIP LOCKED` within a Common Table Expression (CTE) allows a worker to claim, lock, and update a task's status in a single, safe round-trip.
- **Transactional Safety (ACID):** It allows queuing operations to reside in the same database as business data, meaning a task is only queued if the parent business transaction successfully commits.

## Code Example
```sql
-- Atomically fetch, lock, and claim the next available task for a specific worker
WITH next_task AS (
    SELECT id
    FROM task_queue
    WHERE status = 'pending'
      AND (scheduled_at IS NULL OR scheduled_at <= NOW())
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
UPDATE task_queue
SET status = 'processing',
    locked_by = 'worker_node_01a',
    locked_at = NOW()
FROM next_task
WHERE task_queue.id = next_task.id
RETURNING task_queue.id, task_queue.payload;
```

---
*Logged on 2026-03-31 10:15:00 (UTC)*
