# ContextVars for Async-Safe State Management

In asynchronous Python programming, traditional thread-local storage (`threading.local`) fails because multiple coroutines interleave their execution on a single OS thread. The `contextvars` module solves this by providing "context-local" storage, allowing developers to maintain isolated state (such as request IDs, transaction tokens, or user sessions) across concurrent asynchronous task boundaries. This is highly critical for implementing reliable structured logging, distributed tracing, and dependency injection in modern ASGI frameworks like FastAPI.

## Key Takeaways
- Unlike thread-local storage, `contextvars.ContextVar` is natively aware of both thread boundaries and `asyncio.Task` execution contexts, preventing concurrent tasks from leaking state into one another.
- When a new asynchronous task is spawned (e.g., via `asyncio.create_task`), it automatically inherits a shallow copy of the creator's context, ensuring seamless propagation of context downstream.
- Modifying a `ContextVar` yields a `Token` that must be used to reset the variable to its previous state, preventing pollution of the shared execution context when returning to the event loop pool.

## Code Example
```python
import asyncio
import contextvars
import uuid

# Declare a context variable to hold a unique request correlation ID
correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id")

async def log_with_context(message: str) -> None:
    # Retrieve the context-specific value safely, falling back if not set
    corr_id = correlation_id_ctx.get("NO-CONTEXT")
    print(f"[{corr_id}] {message}")

async def handle_request(request_name: str, delay: float) -> None:
    # Set the context-local state for this specific concurrent execution path
    token = correlation_id_ctx.set(f"req-{uuid.uuid4().hex[:6]}")
    try:
        await log_with_context(f"Starting processing for {request_name}")
        # Simulate I/O context switch. The event loop yields, but context remains isolated.
        await asyncio.sleep(delay)
        await log_with_context(f"Finished processing for {request_name}")
    finally:
        # Reset the context variable to its previous state to prevent context bleeding
        correlation_id_ctx.reset(token)

async def main() -> None:
    # Run concurrent tasks to demonstrate strict context isolation
    await asyncio.gather(
        handle_request("GetUsers", 0.2),
        handle_request("UpdateProduct", 0.1),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2024-06-03 18:25:00 (UTC)*
