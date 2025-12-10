from tree_print import pretty_tree
import sys

class Node:
    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

class BSTree:
    # Constructor
    # Optionally, you can initialize the tree with a root node
    def __init__(self, root=None):
        self.root = root
    
    # Clear the tree
    def clear(self):
        self.root = None

    # Insert a Node with a given key and value into the tree
    def insert(self, key, value=None):
        self.root = self._insert(self.root, key, value)

    # Helper function for insert
    def _insert(self, root, key, value=None):
        if root is None:
            return Node(key, value)
        if key < root.key:
            root.left = self._insert(root.left, key, value)
        else:
            root.right = self._insert(root.right, key, value)
        return root

    # Magic method: check if the tree contains a key
    # Support for the 'in' operator
    def __contains__(self, key):
        return self._search(self.root, key)
    
    # Helper function for contains
    def _search(self, root, key):
        if root is None:
            return False
        if root.key == key:
            return True
        if key < root.key:
            return self._search(root.left, key)
        return self._search(root.right, key)
    
    # Inorder traversal
    def inorder(self):
        return self._inorder(self.root)

    # Helper function for inorder
    def _inorder(self, root):
        if not root:
            return []
        return (
            self._inorder(root.left) +
            [root.key] +
            self._inorder(root.right) )

    # Magic method: get the length of the tree 
    # Support for the len() function 
    def __len__(self):
        return self._len(self.root)
    
    # Helper function for len
    def _len(self, root):
        if not root:
            return 0
        left_len = self._len(root.left)
        right_len = self._len(root.right)
        return 1 + left_len + right_len
    
    # Get the height of the tree
    def height(self):
        return self._height(self.root)
    
    # Helper function for height
    def _height(self, root):
        if root == None:
            return -1
        left_height = self._height(root.left)
        right_height = self._height(root.right)
        return 1 + max(left_height, right_height)

    # Remove a Node with a given key and value from the tree  
    def remove(self, key, value=None):
        self.root = self._remove(self.root, key, value)
    
    # Helper function for remove
    def _remove(self, root, key, value=None):
        if root is None:
            return root
        
        # Key is not yet found
        if key < root.key:
            root.left = self._remove(root.left, key, value)
        # Searches right subtree if key is greater or value does not match
        elif key > root.key or value != root.value:
            root.right = self._remove(root.right, key, value)

        # Matching key, value is found
        else:
            # Node with only one child or leaf node: return the non-null child
            # If the node has no children, return None
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            successor = self._min_value_node(root.right)
            root.key = successor.key
            root.value = successor.value
            # Delete the inorder successor
            root.right = self._remove(root.right, root.key, root.value)
        return root
    
    # Helper function to find the minimum value node in a tree
    def _min_value_node(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current

    # Write the BFS traversal of the tree to a list
    def write_bfs(self):
        # If the tree is empty, return an empty list
        if self.root is None:
            return []
        
        # Push the root node to the queue
        queue = [self.root]

        # List to store the BFS traversal results
        bfs = []

        # While there are nodes to process
        while queue:
            # Pop the first node from the queue
            node = queue.pop(0)

            # If the node is None (missing children), append None to the BFS list
            if node is None:
                bfs.append(None)
            
            # If the node is not None, append its key to the results and push its children to the queue
            else:
                bfs.append(node.key)
                queue.append(node.left)
                queue.append(node.right)
        
        # Remove trailing None values
        while bfs and bfs[-1] is None:
            bfs.pop()
        
        # Return the BFS traversal list
        return bfs
    
    # Magic method: string representation of the tree
    # Support for the print() function
    def __str__(self):
        return pretty_tree(self)
