# Database Sharding via Consistent Hashing

Consistent hashing is a distributed systems technique that maps data to nodes in a way that minimizes remapping when the cluster size changes. Unlike simple modulo hashing (where adding a node forces a reshuffle of nearly all keys), consistent hashing limits reorganization to only a fraction of the keys, which is critical for maintaining availability in large-scale distributed databases.

## Key Takeaways
- **Ring Topology:** Keys and nodes are mapped onto a logical circular hash space (the "hash ring") using the same hash function.
- **Minimal Disruption:** When a node is added or removed, only the keys immediately adjacent to that node on the ring need to be remapped, rather than the entire dataset.
- **Virtual Nodes:** To prevent "hotspots" and ensure uniform data distribution, each physical node is mapped to multiple points (virtual nodes) on the ring.

## Code Example
```python
import hashlib
import bisect

class ConsistentHash:
    def __init__(self, nodes=None, replicas=3):
        self.replicas = replicas
        self.ring = {}
        self._sorted_keys = []
        for node in (nodes or []):
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node):
        for i in range(self.replicas):
            h = self._hash(f"{node}:{i}")
            self.ring[h] = node
            bisect.insort(self._sorted_keys, h)

    def get_node(self, key):
        if not self.ring: return None
        h = self._hash(key)
        # Find the first node clockwise on the ring
        idx = bisect.bisect_right(self._sorted_keys, h)
        idx = idx % len(self._sorted_keys)
        return self.ring[self._sorted_keys[idx]]

# Usage
cluster = ConsistentHash(["db-node-1", "db-node-2"])
print(f"Key 'user_123' maps to: {cluster.get_node('user_123')}")
```

---
*Logged on 2025-05-14 14:32:10 (UTC)*
