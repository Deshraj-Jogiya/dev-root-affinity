# PostgreSQL `SKIP LOCKED` for High-Concurrency Database Queues

Building a task queue inside a relational database often leads to severe lock contention and performance bottlenecks when multiple workers attempt to claim tasks simultaneously. By utilizing PostgreSQL's `SELECT ... FOR UPDATE SKIP LOCKED` syntax, concurrent workers can instantly skip rows that are already locked by other transactions. This allows you to build a highly performant, ACID-compliant message queue directly within your existing database, eliminating the operational complexity of running a separate Redis or RabbitMQ cluster for simple workloads.

## Key Takeaways
- **Non-Blocking Concurrency:** `SKIP LOCKED` allows transactions to bypass rows currently locked by other workers, eliminating lock wait times and maximizing throughput across highly concurrent consumer pools.
- **ACID-Backed Reliability:** Task state transitions (e.g., from `pending` to `processing`) are bound to the worker's transaction. If a worker crashes or times out, the transaction rolls back, releasing the lock and making the task instantly available to other workers.
- **Subquery Optimization:** To update a row safely, the `FOR UPDATE SKIP LOCKED` clause should be executed inside a nested subquery with a `LIMIT 1` to ensure only a single record is locked and updated, preventing table-wide scan locks.

## Code Example

The following Python code demonstrates how a worker can safely claim a single pending task in a highly concurrent environment using Postgres and `psycopg2`.

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any

def claim_next_task(worker_id: str) -> Optional[Dict[str, Any]]:
    """
    Safely claims the oldest pending task using FOR UPDATE SKIP LOCKED.
    Ensures that concurrent workers do not block each other or process duplicate tasks.
    """
    connection_string = "dbname=app_db user=postgres password=secret host=localhost"
    
    # We must manage the transaction explicitly to control the lock lifecycle
    with psycopg2.connect(connection_string) as conn:
        conn.autocommit = False
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # The subquery selects and locks exactly one pending row, skipping locked ones.
                # The outer UPDATE then changes its status so subsequent transactions won't select it.
                query = """
                    UPDATE tasks
                    SET status = 'processing',
                        locked_by = %s,
                        locked_at = NOW()
                    WHERE id = (
                        SELECT id
                        FROM tasks
                        WHERE status = 'pending'
                        ORDER BY created_at ASC
                        FOR UPDATE SKIP LOCKED
                        LIMIT 1
                    )
                    RETURNING id, payload;
                """
                cur.execute(query, (worker_id,))
                task = cur.fetchone()
                
                # Commit the transaction to release the row lock and persist the status change
                conn.commit()
                return task
                
        except Exception as e:
            conn.rollback()
            print(f"Failed to claim task: {e}")
            raise e
```

---
*Logged on 2024-10-24 14:32:10 (UTC)*
