class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert(root, key):
    """Insert a new key into the BST."""
    if root is None:
        return Node(key)
    
    if key < root.val:
        root.left = insert(root.left, key)
    elif key > root.val:
        root.right = insert(root.right, key)
        
    return root


def search(root, key):
    """Search a key in the BST."""
    if root is None or root.val == key:
        return root

    if root.val < key:
        return search(root.right, key)

    return search(root.left, key)


def inorder(root, result=None):
    """Perform Inorder traversal of the BST (returns sorted values)."""
    if result is None:
        result = []
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result


if __name__ == "__main__":
    # BST Construction
    r = Node(50)
    r = insert(r, 30)
    r = insert(r, 20)
    r = insert(r, 40)
    r = insert(r, 70)
    r = insert(r, 60)
    r = insert(r, 80)

    print("Inorder traversal of BST (should be sorted):")
    print(inorder(r))

    search_key = 60
    found_node = search(r, search_key)
    if found_node:
        print(f"Key {search_key} found in BST.")
    else:
        print(f"Key {search_key} not found in BST.")
