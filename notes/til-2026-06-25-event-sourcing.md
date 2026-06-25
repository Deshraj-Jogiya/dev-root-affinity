# Event Sourcing

Event Sourcing is an architectural pattern where all changes to application state are stored as a sequence of immutable events. Instead of updating a database record directly, you append an event describing the change, and the current state is derived by replaying these events. This approach provides a complete audit trail, simplifies debugging, and enables powerful features like time-travel debugging and CQRS (Command Query Responsibility Segregation).

## Key Takeaways
- State is reconstructed by replaying a historical log of events, not by direct mutation.
- Each event is immutable, ensuring data integrity and a reliable audit trail.
- Enables sophisticated features like temporal querying, debugging historical states, and easily implementing read models for performance.

## Code Example
```python
from datetime import datetime

class Event:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.data = data

class OrderCreated(Event):
    def __init__(self, timestamp, order_id, customer_id, items):
        super().__init__(timestamp, {"order_id": order_id, "customer_id": customer_id, "items": items})
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items

class ItemAddedToOrder(Event):
    def __init__(self, timestamp, order_id, item):
        super().__init__(timestamp, {"order_id": order_id, "item": item})
        self.order_id = order_id
        self.item = item

class OrderState:
    def __init__(self):
        self.order_id = None
        self.customer_id = None
        self.items = {}
        self.version = 0

    def apply_event(self, event):
        self.version += 1
        if isinstance(event, OrderCreated):
            self.order_id = event.order_id
            self.customer_id = event.customer_id
            for item, quantity in event.items.items():
                self.items[item] = quantity
        elif isinstance(event, ItemAddedToOrder):
            if event.order_id == self.order_id:
                self.items[event.item] = self.items.get(event.item, 0) + 1
            else:
                # In a real system, this would likely be an error or handled differently
                print(f"Warning: ItemAddedToOrder for wrong order ID: {event.order_id}")

# Simulate event stream
event_stream = [
    OrderCreated(datetime.utcnow(), "ORD123", "CUST456", {"apple": 2, "banana": 1}),
    ItemAddedToOrder(datetime.utcnow(), "ORD123", "apple")
]

# Replay events to get current state
order_state = OrderState()
for event in event_stream:
    order_state.apply_event(event)

print(f"Current Order State: {order_state.__dict__}")
```

---
*Logged on 2023-10-27 10:30:00 (UTC)*
