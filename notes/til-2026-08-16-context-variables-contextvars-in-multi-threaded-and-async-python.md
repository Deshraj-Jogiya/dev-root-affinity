# Context Variables (`contextvars`) in Multi-threaded and Async Python

Python's `contextvars` module provides a mechanism to manage, store, and access state that is local to a specific execution context, such as an asynchronous task or a thread. Unlike traditional `threading.local` which is bound strictly to OS threads, context variables are native to the event loop and propagate correctly across asynchronous boundaries. This is critical for tracking request-scoped data—such as trace IDs, tenant contexts, or database transactions—in modern, highly concurrent applications.

## Key Takeaways
- **Async-Safe Alternative to Thread-Local:** Traditional `threading.local` fails in asynchronous code because multiple coroutines share the same OS thread; `contextvars` correctly isolates state per asynchronous task.
- **Context Propagation:** When an async task spawns a child task (e.g., via `asyncio.create_task`), the current context is automatically copied, allowing child tasks to safely inherit the parent's context state.
- **Token-Based State Restoration:** Modifying a context variable using `.set()` returns a unique `Token`. This token must be passed to `.reset()` to safely restore the variable to its previous state, preventing context pollution in connection pools or worker loops.

## Code Example
```python
import asyncio
import contextvars
import uuid

# Define a context variable for tracking request IDs
request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

async def perform_subtask(task_name: str) -> None:
    # Child tasks inherit the context variable automatically
    current_req_id = request_id_ctx.get()
    print(f"  -> [Subtask: {task_name}] Inherited request_id: {current_req_id}")

async def handle_request(user_id: str) -> None:
    # Generate and set a unique request ID for this specific execution context
    req_id = str(uuid.uuid4())[:8]
    token = request_id_ctx.set(req_id)
    
    try:
        print(f"[{user_id}] Started. Set request_id to: {request_id_ctx.get()}")
        
        # Simulate an asynchronous I/O boundary (yielding control to the event loop)
        await asyncio.sleep(0.1)
        
        # Spawn a nested task to demonstrate context propagation
        await asyncio.create_task(perform_subtask(f"{user_id}-nested"))
        
        print(f"[{user_id}] Finished. Verified request_id is still: {request_id_ctx.get()}")
    finally:
        # Always reset the token to restore the context to its prior state
        request_id_ctx.reset(token)

async def main() -> None:
    # Run two tasks concurrently on the same thread's event loop
    await asyncio.gather(
        handle_request("Alice"),
        handle_request("Bob")
    )

if __name__ == "__main__":
    asyncio.run(main())
```

---
*Logged on 2026-03-31 08:30:00 (UTC)*
