# Contextvars for Async-Safe Context Propagation in Python

In concurrent programming, sharing request-scoped metadata (like trace IDs, user sessions, or database transactions) across deeply nested function calls is a common challenge. While `threading.local` works perfectly for synchronous multi-threaded applications, it fails in asynchronous Python because multiple coroutines run concurrently on the same thread's event loop. Python's `contextvars` module solves this by providing "Context Variables" that are natively managed by the event loop, ensuring strict context isolation per asynchronous task.

## Key Takeaways
- **Async-Aware Isolation:** Unlike `threading.local`, which isolates data per OS thread, `contextvars` isolates data per asynchronous task (`asyncio.Task`), preventing data leakage between concurrent coroutines running on the same thread.
- **Automatic Context Copying:** When a new asynchronous task is spawned, it inherits a copy of the parent task's context, allowing read access while keeping modifications isolated to the child scope.
- **Zero-Propagator Pattern:** Using `contextvars` eliminates the need to pass context objects (like `request` or `trace_id`) as arguments through every intermediate function in your call stack, keeping APIs clean.

## Code Example
```python
import asyncio
import contextvars
import uuid

# Define a context variable with a default value of "N/A"
correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default="N/A"
)

async def mock_db_query(query: str) -> None:
    # Access the context variable without passing it as an argument
    curr_id = correlation_id_ctx.get()
    print(f"[{curr_id}] Executing DB query: {query}")
    await asyncio.sleep(0.1)

async def handle_request(request_path: str) -> None:
    # Set a unique correlation ID for this specific execution context
    token = correlation_id_ctx.set(str(uuid.uuid4())[:8])
    try:
        print(f"[{correlation_id_ctx.get()}] Received request for {request_path}")
        await mock_db_query("SELECT * FROM users;")
    finally:
        # Reset the context variable to prevent memory leaks or context pollution
        correlation_id_ctx.reset(token)

async def main() -> None:
    # Run multiple concurrent requests to demonstrate isolation
    await asyncio.gather(
        handle_request("/api/v1/users"),
        handle_request("/api/v1/status"),
        handle_request("/api/v1/billing"),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2024-10-24 16:00:00 (UTC)*
