# PostgreSQL `FOR UPDATE SKIP LOCKED` for High-Concurrency Queues

Building reliable background task queues directly inside a relational database often leads to lock contention and performance degradation under high concurrency. PostgreSQL's `FOR UPDATE SKIP LOCKED` clause solves this by allowing worker processes to instantly lock and acquire the next available, unlocked row without blocking each other. This enables highly concurrent, transactional queue architectures using simple SQL queries, eliminating the need for external message brokers in early-to-mid-stage systems.

## Key Takeaways
- **Non-Blocking Concurrency:** Unlike standard `FOR UPDATE` which blocks waiting transactions, `SKIP LOCKED` skips already locked rows, letting multiple workers process distinct tasks simultaneously without serialization bottlenecks.
- **Transactional Guarantees (ACID):** Because the queue resides in the database, task consumption can be bundled into the same transaction as the business logic, ensuring exactly-once processing or automatic rollback on worker failure.
- **Performance Optimization:** To prevent table bloat and index degradation from frequent queue writes/deletes, columns used for queue status should be indexed, and aggressive `VACUUM` autotuning should be applied to the queue table.

## Code Example
The following Python snippet demonstrates how a worker process can atomically claim a pending task using a nested subquery with `FOR UPDATE SKIP LOCKED` to prevent race conditions.

```python
import time
import psycopg2

def claim_and_process_job(conn_string):
    # The atomic query claims a single pending task and locks it from other workers
    claim_query = """
        UPDATE tasks
        SET status = 'processing', started_at = NOW()
        WHERE id = (
            SELECT id
            FROM tasks
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        )
        RETURNING id, payload;
    """

    with psycopg2.connect(conn_string) as conn:
        with conn.cursor() as cur:
            cur.execute(claim_query)
            job = cur.fetchone()

            if not job:
                print("No pending jobs found.")
                return None

            job_id, payload = job
            print(f"Claimed Job {job_id}: Processing {payload}...")

            try:
                # Simulate task execution
                time.sleep(1.5)
                
                # Mark job as completed within the same transaction
                cur.execute(
                    "UPDATE tasks SET status = 'completed', completed_at = NOW() WHERE id = %s",
                    (job_id,)
                )
                conn.commit()
                print(f"Successfully processed Job {job_id}")
            except Exception as e:
                # Rollback automatically releases the row lock, returning status to pending if desired
                conn.rollback()
                print(f"Failed to process Job {job_id}: {e}. Lock released.")
```

---
*Logged on 2026-03-30 18:42:15 (UTC)*
