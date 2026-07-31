# Event Sourcing

Event sourcing is a software architectural pattern where all changes to application state are stored as a sequence of immutable events. Instead of storing the current state directly, you store the history of events that led to that state. This allows for powerful auditing, debugging, and the ability to reconstruct past states of the application.

## Key Takeaways
- State is derived by replaying events, not stored directly, offering a complete audit trail.
- Enables easy time-travel debugging and recovery from corrupted states.
- Can be combined with CQRS (Command Query Responsibility Segregation) for enhanced scalability and flexibility.

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
        self.state = defaultdict(lambda: None)
        self.events = []

    def apply_event(self, event):
        if event.event_type == "ORDER_CREATED":
            self.state['order_id'] = event.data['order_id']
            self.state['customer_id'] = event.data['customer_id']
            self.state['status'] = 'PENDING'
        elif event.event_type == "ITEM_ADDED":
            if 'items' not in self.state:
                self.state['items'] = []
            self.state['items'].append(event.data)
        elif event.event_type == "ORDER_SHIPPED":
            self.state['status'] = 'SHIPPED'
        elif event.event_type == "ORDER_CANCELLED":
            self.state['status'] = 'CANCELLED'

    def process_command(self, command):
        if command['command_type'] == "CREATE_ORDER":
            event = OrderEvent("ORDER_CREATED", {"order_id": command['order_id'], "customer_id": command['customer_id']})
            self.events.append(event)
            self.apply_event(event)
        elif command['command_type'] == "ADD_ITEM":
            # In a real system, validation would happen here
            event = OrderEvent("ITEM_ADDED", {"product_id": command['product_id'], "quantity": command['quantity']})
            self.events.append(event)
            self.apply_event(event)
        elif command['command_type'] == "SHIP_ORDER":
            if self.state['status'] == 'PENDING':
                event = OrderEvent("ORDER_SHIPPED", {})
                self.events.append(event)
                self.apply_event(event)
        elif command['command_type'] == "CANCEL_ORDER":
            if self.state['status'] == 'PENDING':
                event = OrderEvent("ORDER_CANCELLED", {})
                self.events.append(event)
                self.apply_event(event)

# Example Usage
order = Order()
commands = [
    {"command_type": "CREATE_ORDER", "order_id": "123", "customer_id": "abc"},
    {"command_type": "ADD_ITEM", "product_id": "p1", "quantity": 2},
    {"command_type": "ADD_ITEM", "product_id": "p2", "quantity": 1},
    {"command_type": "SHIP_ORDER"}
]

for cmd in commands:
    order.process_command(cmd)

print("Current State:", dict(order.state))
# Example of replaying to get state at a specific point
past_order = Order()
past_order.apply_event(order.events[0]) # Only apply the first event
print("State after first event:", dict(past_order.state))
```

---
*Logged on 2023-10-27 10:30:00 UTC*
