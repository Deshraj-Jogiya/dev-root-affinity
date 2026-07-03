# Thread-Safe and Async-Safe Context Propagation with Python's contextvars

In concurrent programming, sharing contextual data (like request IDs or transaction states) across nested function calls without parameter drilling is a common pattern. While thread-local storage (`threading.local`) solves this for multi-threaded applications, it fails in asynchronous programs where multiple cooperative tasks interleave on a single thread. Python's `contextvars` module solves this by providing context-local storage that is natively isolated at the `asyncio.Task` level, preventing data leakage across concurrent operations.

## Key Takeaways
- `threading.local` is unsafe for `asyncio` because multiple concurrent tasks run on the same thread, causing data to leak between requests.
- `contextvars.ContextVar` maintains separate, isolated states for each concurrent `asyncio.Task`, automatically managing context propagation when tasks are scheduled and context-switched.
- This pattern is essential for implementing production-grade logging, distributed tracing, and multi-tenant tenant-ID isolation in modern asynchronous Python web frameworks like FastAPI and Sanic.

## Code Example
```python
import asyncio
import contextvars
import random

# Define a context variable to hold the request ID
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

async def perform_db_query(query_name: str) -> None:
    # Retrieve the context-bound request ID without passing it as an argument
    req_id = request_id_ctx.get()
    print(f"[{req_id}] Executing query: {query_name}")
    await asyncio.sleep(random.uniform(0.1, 0.5))
    print(f"[{req_id}] Query finished: {query_name}")

async def handle_request(req_id: str, query: str) -> None:
    # Set the context variable for the current task context
    token = request_id_ctx.set(req_id)
    try:
        print(f"[{req_id}] Started handling request")
        await perform_db_query(query)
    finally:
        # Reset the context variable to its previous state (best practice)
        request_id_ctx.reset(token)

async def main() -> None:
    # Run multiple requests concurrently to demonstrate context isolation
    await asyncio.gather(
        handle_request("REQ-101", "SELECT * FROM users;"),
        handle_request("REQ-102", "UPDATE orders SET status = 'shipped';"),
        handle_request("REQ-103", "DELETE FROM cache;"),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2024-10-24 17:30:00 (UTC)*
