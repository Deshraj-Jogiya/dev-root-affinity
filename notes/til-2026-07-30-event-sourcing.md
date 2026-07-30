# Event Sourcing

Event Sourcing is an architectural pattern where all changes to application state are stored as a sequence of immutable events. Instead of updating a database record directly, we append new events that describe the state change. This provides a complete, auditable history of all actions, enabling powerful features like time-travel debugging, easier state reconstruction, and event replay for disaster recovery or analytics.

## Key Takeaways
- State is derived by replaying events, not by direct mutation.
- Events are immutable facts about what happened in the system.
- Provides a robust audit trail and enables sophisticated recovery/analytical scenarios.

## Code Example
```python
from collections import defaultdict
import json

class OrderEvent:
    def __init__(self, event_type, data):
        self.event_type = event_type
        self.data = data

class Order:
    def __init__(self):
        self.state = {
            "items": defaultdict(int),
            "total_price": 0.0,
            "status": "NEW"
        }
        self.version = 0

    def apply_event(self, event):
        if event.event_type == "ITEM_ADDED":
            item_name = event.data["item_name"]
            quantity = event.data["quantity"]
            price = event.data["price"]
            self.state["items"][item_name] += quantity
            self.state["total_price"] += quantity * price
        elif event.event_type == "ITEM_REMOVED":
            item_name = event.data["item_name"]
            quantity = event.data["quantity"]
            price = event.data["price"]
            if self.state["items"][item_name] >= quantity:
                self.state["items"][item_name] -= quantity
                self.state["total_price"] -= quantity * price
            if self.state["items"][item_name] == 0:
                del self.state["items"][item_name]
        elif event.event_type == "ORDER_CHECKED_OUT":
            self.state["status"] = "CHECKED_OUT"
        self.version += 1

    def get_state(self):
        return self.state

class EventStore:
    def __init__(self):
        self.events = []

    def append(self, event):
        self.events.append(event)

    def get_all_events(self):
        return self.events

# --- Usage ---
event_store = EventStore()
order = Order()

# Simulate actions and record events
event1 = OrderEvent("ITEM_ADDED", {"item_name": "Laptop", "quantity": 1, "price": 1200.00})
event_store.append(event1)
order.apply_event(event1)

event2 = OrderEvent("ITEM_ADDED", {"item_name": "Mouse", "quantity": 2, "price": 25.00})
event_store.append(event2)
order.apply_event(event2)

event3 = OrderEvent("ORDER_CHECKED_OUT", {})
event_store.append(event3)
order.apply_event(event3)

print("Current Order State:", order.get_state())

# Reconstruct state from events (e.g., after a crash or for a new instance)
new_order = Order()
for event in event_store.get_all_events():
    new_order.apply_event(event)

print("Reconstructed Order State:", new_order.get_state())
```

---
*Logged on 2023-10-27 10:30:00 UTC*
