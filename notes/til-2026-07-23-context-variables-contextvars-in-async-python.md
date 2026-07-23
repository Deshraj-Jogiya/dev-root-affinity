# Context Variables (`contextvars`) in Async Python

In concurrent programming, traditional Thread-Local Storage (`threading.local`) fails in asynchronous environments because a single OS thread multiplexes multiple independent coroutines. Python's `contextvars` module solves this by introducing context-local state that is bound to the execution flow of an `asyncio.Task` rather than the physical thread. This enables robust, implicit propagation of request-scoped metadata—such as correlation IDs, tenant contexts, or database sessions—across deeply nested asynchronous call stacks without polluting function signatures.

## Key Takeaways
- **Async-Safe Isolation:** Unlike thread-local storage, `contextvars.ContextVar` correctly isolates state across distinct `asyncio.Task` boundaries, ensuring concurrent coroutines on the same thread do not leak state to one another.
- **Automatic Task Propagation:** When a new asynchronous task is spawned (e.g., via `asyncio.create_task`), it automatically inherits a shallow copy of the current execution context, allowing seamless downstream access to context variables.
- **Token-Based Resetting:** Modifying a `ContextVar` returns a `Token` that must be used to reset the variable to its prior state, preventing context pollution in long-lived connection pools or reused execution threads.

## Code Example

```python
import asyncio
import contextvars
import uuid

# Define a context variable to hold the request-specific correlation ID
correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id")

async def log_with_context(message: str) -> None:
    # Retrieve the context variable's value for the current async task
    try:
        corr_id = correlation_id_ctx.get()
    except LookupError:
        corr_id = "NO-CONTEXT"
    print(f"[{corr_id}] {message}")

async def process_request(request_name: str) -> None:
    # Set the context variable and store the reset token
    token = correlation_id_ctx.set(str(uuid.uuid4())[:8])
    try:
        await log_with_context(f"Starting processing for {request_name}")
        await asyncio.sleep(0.1)  # Simulate asynchronous I/O bound work
        await log_with_context(f"Finished processing for {request_name}")
    finally:
        # Reset the context variable to its previous state to prevent context leakage
        correlation_id_ctx.reset(token)

async def main() -> None:
    # Run multiple requests concurrently; contexts remain completely isolated
    await asyncio.gather(
        process_request("Request-A"),
        process_request("Request-B"),
        process_request("Request-C")
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2024-06-03 15:45:00 (UTC)*
