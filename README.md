# Project Description
- This project uses either a binary search tree or an AVL tree to store information about software vulnerabilities, where the tree is sorted according to the severity of the vulnerabilities. This tree is used to filter the data such that only information about vulnerabilities in a specific severity range will be displayed.
- The amount of time taken to create the tree and perform the range search is printed in the terminal.
- The user can then plot information about software vulnerabilities within that severity range.
- There are three plots that can be displayed for a given severity range:
    - Number of vulnerabilities by CWE for the top 25 most common CWEs
    - Average severity by CWE for the top 25 most common CWEs 
    - Number of vulnerabilities added to database by month

# How to Run Project
- "make test"
    - Runs all unit tests for the project
- "make" or "make run"
    - Runs the program so that the user is prompted to input information through the terminal
- "make demo"
    - Runs the program with the sample input found in demo_input.txt
    - Uses the large dataset, an AVL tree, and a severity range of 5-10
    - Instead of choosing which plot to display, it will display the 3 plots in order (exiting a plot will cause the next plot to open)

# Analysis of AVL vs. BST Performance
- For the small and medium datasets, a BST processes the data more quickly than an AVL tree despite the AVL's guaranteed O(log N) time complexity due to the added overhead of rebalancing operations.
- However, for the large dataset, an AVL tree performs much faster than a BST. This indicates that the BST becomes unbalanced due to the order of insertions from the dataset. This makes the rebalancing of the AVL tree very important, and the benefits of the guaranteed O(log N) time complexity outweigh the overhead of rebalancing operations.