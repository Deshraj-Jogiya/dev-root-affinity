# Eventual Consistency and the CAP Theorem

Eventual consistency is a consistency model where, if no new updates are made to a given data item, all accesses to that item will eventually return the last updated value. This is a crucial concept in distributed systems, as it allows for higher availability and partition tolerance, often at the cost of immediate consistency. The CAP theorem states that a distributed data store cannot simultaneously provide more than two out of the following three guarantees: Consistency, Availability, and Partition Tolerance. In practice, most distributed systems must choose between C and A when a network partition occurs.

## Key Takeaways
- Eventual consistency prioritizes availability and partition tolerance over immediate data consistency across all nodes.
- The CAP theorem highlights the fundamental trade-offs in distributed systems: you can't have perfect Consistency, Availability, and Partition Tolerance all at once.
- Systems opting for eventual consistency often use mechanisms like read repair, write repair, or version vectors to resolve conflicts and converge towards a consistent state.

## Code Example
```python
# Illustrating a simplified "eventual consistency" scenario with separate data stores
# This is a conceptual example, not a production-ready distributed system.

class UserProfile:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.version = 0

class DistributedUserProfileService:
    def __init__(self):
        self.data_store_1 = {}
        self.data_store_2 = {}

    def update_profile(self, user_id, username=None, email=None):
        # Simulate an update operation that might not reach all nodes immediately
        if user_id in self.data_store_1:
            profile = self.data_store_1[user_id]
            if username:
                profile.username = username
            if email:
                profile.email = email
            profile.version += 1
            # Simulate a delay or failure in replicating to data_store_2
            # In a real system, this would involve network calls and error handling
            if user_id not in self.data_store_2 or self.data_store_2[user_id].version < profile.version:
                self.data_store_2[user_id] = UserProfile(profile.user_id, profile.username, profile.email)
                self.data_store_2[user_id].version = profile.version
            print(f"Updated profile for {user_id} in data_store_1 (v{profile.version})")
        else:
            print(f"User {user_id} not found in data_store_1.")

    def get_profile(self, user_id):
        # In a real system, this would involve a strategy to read from multiple nodes
        # and resolve potential inconsistencies. Here, we just check both.
        profile1 = self.data_store_1.get(user_id)
        profile2 = self.data_store_2.get(user_id)

        if profile1 and profile2:
            if profile1.version >= profile2.version:
                return profile1
            else:
                return profile2
        elif profile1:
            return profile1
        elif profile2:
            return profile2
        else:
            return None

# --- Usage ---
service = DistributedUserProfileService()

# Initial creation (simplified, assuming it propagates)
service.data_store_1[1] = UserProfile(1, "alice", "alice@example.com")
service.data_store_1[1].version = 1
service.data_store_2[1] = UserProfile(1, "alice", "alice@example.com")
service.data_store_2[1].version = 1

print("Initial state:")
print(service.get_profile(1).__dict__)

# Update that might not immediately reflect everywhere
service.update_profile(1, username="alice_updated") # This update is applied to data_store_1 and then (simulated) to data_store_2

print("\nAfter update:")
# Reading from data_store_1 might show the new username, while data_store_2 might still have the old one briefly.
# Our get_profile tries to resolve this by picking the latest version.
print(service.get_profile(1).__dict__)

# Simulate a scenario where data_store_2 is lagging
del service.data_store_2[1]
service.data_store_2[1] = UserProfile(1, "alice_updated", "alice@example.com")
service.data_store_2[1].version = 1 # Incorrect version to show potential issues

print("\nSimulating data_store_2 lag with older version:")
# get_profile should still return the correct version from data_store_1
print(service.get_profile(1).__dict__)

# Now, let's say data_store_2 gets updated correctly
service.data_store_2[1] = UserProfile(1, "alice_updated", "alice@example.com")
service.data_store_2[1].version = 2

print("\nAfter data_store_2 is correctly updated:")
print(service.get_profile(1).__dict__)
```

---
*Logged on 2023-10-27 14:30:00 (UTC)*
