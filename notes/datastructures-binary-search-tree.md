# Binary Search Tree (BST) Implementation

A Binary Search Tree is a hierarchical data structure where each node has at most two children, referred to as the left child and the right child.

## BST Property
For any given node $N$:
- All keys in the left subtree of $N$ are less than the key of $N$.
- All keys in the right subtree of $N$ are greater than the key of $N$.

This property allows search, insertion, and deletion operations to run in $O(\log n)$ average time complexity.

## Common Operations

1. **Insertion**: Recursively traverse the tree, placing the new key in the left subtree if it is smaller than the current node, or the right subtree if it is larger.
2. **Search**: Compare the target key with the current node key; traverse left or right accordingly until the node is found or a leaf is reached.
3. **Inorder Traversal**: Traverses the left subtree, visits the root, and then traverses the right subtree. This traversal retrieves BST keys in sorted order.

## Implementation Details
The complete implementation of this BST node, insertion, search, and inorder traversal functions can be found in [binary_search_tree.py](file:///G:/dev-root-affinity/src/2019/binary_search_tree.py).

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
    return root
```

---
*Logged on 2019-03-18 13:01:00 (UTC)*
