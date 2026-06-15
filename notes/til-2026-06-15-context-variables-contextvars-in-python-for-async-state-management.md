# Context Variables (`contextvars`) in Python for Async State Management

In multi-threaded programming, thread-local storage (`threading.local`) is the standard way to isolate state to a specific thread of execution. However, in asynchronous programming with `asyncio`, multiple tasks/coroutines are multiplexed onto a single OS thread, meaning thread-local storage will leak state across interleaved tasks. Python's `contextvars` module solves this by providing context-local storage, allowing developer-defined state to be isolated to the execution context of individual asynchronous tasks.

## Key Takeaways
- `contextvars` prevents race conditions and state leakage across concurrent tasks running on the same event loop thread.
- Asynchronous frameworks (like FastAPI) use context variables under the hood to manage request-scoped data, such as database sessions or correlation IDs.
- When spawning new tasks using `asyncio.create_task()`, the current context is automatically copied, ensuring child tasks inherit the parent's context state without mutating it.

## Code Example
```python
import asyncio
import contextvars
import uuid

# Define a context variable with a default value
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="no-request-id"
)

async def handle_request(client_name: str, delay: float):
    # Set the unique context variable for this specific execution context
    req_id = f"req-{uuid.uuid4().hex[:6]}"
    token = request_id_ctx.set(req_id)
    
    try:
        print(f"[{client_name}] Started. Context Request ID: {request_id_ctx.get()}")
        
        # Yield control to the event loop. In thread-local storage, 
        # another task running now would overwrite our state.
        await asyncio.sleep(delay)
        
        # The context remains perfectly isolated when we resume
        print(f"[{client_name}] Completed. Context Request ID: {request_id_ctx.get()}")
    finally:
        # Reset the context variable to its previous state (good practice)
        request_id_ctx.reset(token)

async def main():
    # Run two concurrent tasks to demonstrate isolation
    await asyncio.gather(
        handle_request("Client-A", 0.2),
        handle_request("Client-B", 0.1)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2023-10-27 19:15:30 (UTC)*
