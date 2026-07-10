# Event Sourcing

Event Sourcing is a software design pattern where all changes to application state are stored as a sequence of immutable events. Instead of updating a record directly, we append a new event that describes the change. This approach provides a complete audit trail, simplifies debugging, and enables powerful features like time-travel debugging and rebuilding state from scratch.

## Key Takeaways
- State is derived from a sequence of immutable events, not by directly modifying a current state representation.
- Provides a full, immutable history of all changes, which is invaluable for auditing, debugging, and compliance.
- Enables rebuilding application state at any point in time, facilitating complex scenarios like "time travel" debugging.

## Code Example
```python
class OrderCreated:
    def __init__(self, order_id, customer_id, items):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items

class ItemAdded:
    def __init__(self, order_id, item_id, quantity):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity = quantity

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.customer_id = None
        self.items = {}
        self.events = []

    def apply(self, event):
        if isinstance(event, OrderCreated):
            self.customer_id = event.customer_id
            self.items = {item['id']: item for item in event.items}
        elif isinstance(event, ItemAdded):
            if event.item_id in self.items:
                self.items[event.item_id]['quantity'] += event.quantity
            else:
                self.items[event.item_id] = {'id': event.item_id, 'quantity': event.quantity}
        # ... handle other event types

    def record(self, event):
        self.events.append(event)
        self.apply(event)

def replay_events(order_id, event_stream):
    order = Order(order_id)
    for event in event_stream:
        order.apply(event)
    return order

# Example Usage
order_id = "ORD123"
initial_items = [{"id": "ITEM001", "quantity": 2}]
events = [
    OrderCreated(order_id, "CUST456", initial_items),
    ItemAdded(order_id, "ITEM001", 1),
    ItemAdded(order_id, "ITEM002", 3)
]

reconstructed_order = replay_events(order_id, events)

print(f"Order ID: {reconstructed_order.order_id}")
print(f"Customer ID: {reconstructed_order.customer_id}")
print(f"Items: {reconstructed_order.items}")
```

---
*Logged on 2023-10-27 10:30:00 UTC*
