# Python `contextvars` for Async-Safe Context Propagation

In concurrent programming, managing request-scoped state (such as trace IDs, user sessions, or database transactions) is critical for observability and safety. While `threading.local` works perfectly for multi-threaded applications, it fails in asynchronous code because multiple coroutines interleave on the same physical thread. Python's `contextvars` module solves this by providing context-local storage that is natively aware of both threads and asynchronous task boundaries.

## Key Takeaways
- **Async-Aware Isolation:** Unlike `threading.local`, `contextvars` isolates state at the `asyncio.Task` level, preventing data leakage between concurrent coroutines running on the single-threaded event loop.
- **Context Propagation:** State is automatically copied when spawning new tasks, allowing child tasks to inherit the context of their parent while keeping mutations isolated if desired.
- **Practical Observability:** It is the foundational mechanism used by modern tracing libraries (like OpenTelemetry) to propagate span contexts across asynchronous execution boundaries without explicitly passing variables through every function signature.

## Code Example
```python
import asyncio
import contextvars
import uuid

# Define a context variable with a default value
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="no-request-id"
)

async def process_sub_task(task_name: str):
    # The context variable is automatically propagated to this sub-task
    current_id = request_id_var.get()
    print(f"[{task_name}] Inherited Request ID: {current_id}")

async def handle_request(client_name: str):
    # Set a unique request ID for this execution context
    token = request_id_var.set(str(uuid.uuid4())[:8])
    try:
        print(f"[{client_name}] Started with ID: {request_id_var.get()}")
        # Simulate concurrent work
        await asyncio.sleep(0.1)
        await process_sub_task(client_name)
    finally:
        # Always reset the context variable to its prior state
        request_id_var.reset(token)

async def main():
    # Run two requests concurrently. Their contexts will remain completely isolated.
    await asyncio.gather(
        handle_request("Client-A"),
        handle_request("Client-B"),
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2026-03-30 08:45:00 (UTC)*
