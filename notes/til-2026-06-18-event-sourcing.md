# Event Sourcing

Event Sourcing is an architectural pattern where all changes to application state are stored as a sequence of immutable events. Instead of updating a database record directly, we append a new event that describes what happened, which is then used to reconstruct the current state. This approach provides a full audit log, simplifies debugging, and enables powerful features like temporal queries and command-query responsibility segregation (CQRS).

## Key Takeaways
- All state changes are recorded as a sequence of immutable events.
- The current state is derived by replaying these events.
- Provides a complete, chronological audit trail of all operations.

## Code Example
```python
from collections import defaultdict

class TransactionEvent:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount

class Account:
    def __init__(self, account_id):
        self.account_id = account_id
        self.balance = 0
        self.events = []

    def deposit(self, amount):
        event = TransactionEvent("DEPOSIT", amount)
        self.events.append(event)
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            event = TransactionEvent("WITHDRAWAL", amount)
            self.events.append(event)
            self.balance -= amount
        else:
            print("Insufficient funds")

    def replay_events(self, events_to_replay):
        self.balance = 0 # Reset state before replaying
        for event in events_to_replay:
            if event.type == "DEPOSIT":
                self.balance += event.amount
            elif event.type == "WITHDRAWAL":
                self.balance -= event.amount

# Simulate storing and replaying events
account_id = "acc_123"
initial_events = [
    TransactionEvent("DEPOSIT", 100),
    TransactionEvent("WITHDRAWAL", 20)
]

account = Account(account_id)
account.replay_events(initial_events)
print(f"Initial balance from events: {account.balance}")

account.deposit(50)
account.withdraw(10)
print(f"Current balance after new transactions: {account.balance}")

# To get the state at a specific point in time, you'd replay a subset of events.
```

---
*Logged on 2023-10-27 10:30:00 UTC*
