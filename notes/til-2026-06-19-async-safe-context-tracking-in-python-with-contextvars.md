# Async-Safe Context Tracking in Python with contextvars

Today I looked into how state gets isolated when writing async Python code. 

If you have ever used `threading.local` in multi-threaded code to store request-specific info (like a correlation ID or database session), you'll quickly run into bugs in async environments. Since `asyncio` multiplexes many concurrent tasks on a single OS thread, thread-local state will leak across tasks when they yield control.

Python's `contextvars` module solves this. It gives you context-local variables that are bound to the active async task flow instead of the physical OS thread.

## How it works (My Takeaways)

* **Async Isolation**: It gives you isolated variables for async tasks. Running two requests at the same time means their variables are completely separate.
* **Inheritance & Copy-on-Write**: Spawning a new task (like `asyncio.create_task()`) copies the current context. The new task gets a snapshot of the parent's data. If the child changes a value, it doesn't affect the parent.
* **Proper Cleanup**: Calling `ContextVar.set()` returns a token. You need to reset the variable back to its previous state using `ContextVar.reset(token)` in a `finally` block so that recycled threads or tasks in a pool don't leak state.

## Practical Code Example

Here is a simple example of tracking a request correlation ID across database queries:

```python
import asyncio
import contextvars
import uuid

# Define the context variable with a default value
correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default="no-request-id"
)

async def run_db_query(query_text: str):
    # This automatically reads the ID set in the task's active context
    req_id = correlation_id.get()
    print(f"[{req_id}] Running query: {query_text}")
    await asyncio.sleep(0.05)
    print(f"[{req_id}] Done.")

async def handle_incoming_request(path: str):
    # Set a unique ID for this execution flow
    unique_id = f"req-{uuid.uuid4().hex[:6]}"
    token = correlation_id.set(unique_id)
    
    try:
        print(f"[{unique_id}] Received request for /{path}")
        # The correlation ID is implicitly passed to any downstream async functions
        await run_db_query(f"SELECT * FROM {path} LIMIT 10")
    finally:
        # Reset the context variable to avoid leaking it to subsequent tasks
        correlation_id.reset(token)

async def main():
    # Run three mock requests concurrently on the event loop
    await asyncio.gather(
        handle_incoming_request("profile"),
        handle_incoming_request("dashboard"),
        handle_incoming_request("settings")
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2024-10-24 15:30:00 (UTC)*
