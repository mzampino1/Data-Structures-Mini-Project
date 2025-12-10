run: vuln_tree.py
	@echo Running with user input ...
	@chmod +x vuln_tree.py
	./vuln_tree.py
	@echo

demo: demo_input.txt vuln_tree.py
	@echo Running demo ...
	@chmod +x vuln_tree.py
	./vuln_tree.py < demo_input.txt
	@echo

test:
	@$(MAKE) -sk test_all

test_all: test_tree test_avl test_bst

test_tree: vuln_tree_test.py vuln_tree.py
	@echo Testing vuln_tree ...
	@chmod +x ./vuln_tree_test.py
	./vuln_tree_test.py -v
	@echo

test_avl: avl_test.py vuln_tree.py
	@echo Testing avl ...
	@chmod +x ./avl_test.py
	./avl_test.py -v
	@echo

test_bst: bst_test.py vuln_tree.py
	@echo Testing bst ...
	@chmod +x ./bst_test.py
	./bst_test.py -v
	@echo