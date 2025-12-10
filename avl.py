from tree_print import pretty_tree

class Node:
    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.height = 0

class AVLTree:
    # Constructor
    # Optionally, you can initialize the tree with a root node
    # and specify whether the tree should be balanced
    def __init__(self, root=None, do_balance=True):
        self.root = root
        self.do_balance = do_balance
    
    # Clear the tree
    def clear(self):
        self.root = None

    # Helper function to get the height of a node for AVL balancing
    # Note: The height of a null node is -1
    def _get_height(self, root):
        if not root:
            return -1
        return root.height
    
    # Helper function to update the height of a node
    def _update_height(self, node):
        # TODO
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

    # Helper function to get the balance factor of a node
    # Note: The balance factor of a null node is 0
    def _balance_factor(self, root):
        if not root:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)
    
    # Helper functions to rotate left for AVL balancing
    def _rotate_left(self, z):
        """
        Example:
            Given the following tree:
            z
           / \
          T1  y
             / \
            T2  T3

            After _left_rotate(z), the tree becomes:
              y
             / \
            z   T3
           / \
          T1  T2
        """
        # TODO
        # Do the rotation
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        # Update the heights
        self._update_height(z)
        self._update_height(y)

        # Return the new root
        return y

    # Helper functions to rotate right for AVL balancing
    def _rotate_right(self, z):
        """
        Example:
            Given the following tree:
              z
             / \
            y  T3
           / \
          T1  T2

            After _right_rotate(z), the tree becomes:
              y
             / \
            T1  z
               / \
              T2  T3
        """
        # Do the rotation
        y = z.left
        T2 = y.right

        y.right = z
        z.left = T2

        # Update the heights
        self._update_height(z)
        self._update_height(y)

        # Return the new root
        return y

    # Helper function to rebalance the tree after insertion or removal
    def _balance(self, node):
        # TODO
        # update height
        self._update_height(node)

        # left heavy
        if self._balance_factor(node) > 1:
            # left child is right heavy
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # right heavy
        if self._balance_factor(node) < -1:
            # right child is left heavy
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # Insert a Node with a given key and value into the tree
    def insert(self, key, value=None):
        self.root = self._insert(self.root, key, value)

    # Helper function for insert
    def _insert(self, root, key, value=None):
        # Regular BST insertion
        if root is None:
            return Node(key, value)
        
        if key < root.key:
            root.left = self._insert(root.left, key, value)
        else:
            root.right = self._insert(root.right, key, value)

        if self.do_balance:
            # Rebalance the tree
            return self._balance(root)
        else:
            return root
    
    # Remove a Node with a given key and value from the tree  
    def remove(self, key, value=None):
        self.root = self._remove(self.root, key, value)
    
    # Helper function for remove
    def _remove(self, root, key, value=None):
        # Regular BST removal
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

        if self.do_balance:
            # Rebalance the tree
            return self._balance(root)
        else:
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
    
    # Magic method: string representation of the tree
    # Support for the print() function
    def __str__(self):
        return pretty_tree(self)
