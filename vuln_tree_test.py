#!/usr/bin/env python3

import unittest
import pandas as pd

from vuln_tree import (
    load_vuln_data,
    make_vuln_bst,
    make_vuln_avl,
    filter_vuln_df_by_severity,
)


class TestVulnTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small_path = "vuln_data_small.csv"
        cls.medium_path = "vuln_data_medium.csv"
        cls.large_path = "vuln_data_large.csv"

    def test_load_vuln_data(self):
        # Test small dataset
        small_df = load_vuln_data(self.small_path)
        self.assertIn("Date", small_df.columns)
        self.assertIn("CWE", small_df.columns)
        self.assertIn("Severity", small_df.columns)
        self.assertEqual(len(small_df), 100)
        # Test medium dataset
        medium_df = load_vuln_data(self.medium_path)
        self.assertIn("Date", medium_df.columns)
        self.assertIn("CWE", medium_df.columns)
        self.assertIn("Severity", medium_df.columns)
        self.assertEqual(len(medium_df), 2000)
        # Test large dataset
        large_df = load_vuln_data(self.large_path)
        self.assertIn("Date", large_df.columns)
        self.assertIn("CWE", large_df.columns)
        self.assertIn("Severity", large_df.columns)
        self.assertEqual(len(large_df), 35283)
    
    def test_make_vuln_bst(self):
        # Load small dataset
        df = load_vuln_data(self.small_path)
        
        # Build BST
        bst = make_vuln_bst(df)
        bst_keys = bst.inorder()
        
        # Ensure BST is not empty
        self.assertGreater(len(bst_keys), 0)
        
        # Collect all severities from the DataFrame (skip NaN)
        severities_in_df = [s for s in df["Severity"].tolist() if pd.notna(s)]
        
        # Check that all severities are in the BST
        for sev in severities_in_df:
            self.assertIn(sev, bst_keys)
        
        # Check that severities are ordered properly in BST
        self.assertEqual(bst_keys, sorted(bst_keys))

        # Check BST size matches number of non-NaN severities
        self.assertEqual(len(bst_keys), len(severities_in_df))
    
    def test_make_vuln_avl(self):
        # Load small dataset
        df = load_vuln_data(self.small_path)
        
        # Build AVL tree
        avl = make_vuln_avl(df)
        avl_keys = avl.inorder()
        
        # Ensure AVL tree is not empty
        self.assertGreater(len(avl_keys), 0)
        
        # Collect all severities from the DataFrame (skip NaN)
        severities_in_df = [s for s in df["Severity"].tolist() if pd.notna(s)]
        
        # Check that all severities are in the AVL tree
        for sev in severities_in_df:
            self.assertIn(sev, avl_keys)
        
        # Check that severities are ordered properly in AVL tree
        self.assertEqual(avl_keys, sorted(avl_keys))

        # Check AVL tree size matches number of non-NaN severities
        self.assertEqual(len(avl_keys), len(severities_in_df))
    
    def test_filter_vuln_df_by_severity(self):
        # Load small dataset
        df = load_vuln_data(self.small_path)

        # Filter vulnerabilities with severity between 6.0 and 9.5 using
        # BST and AVL
        filtered_df_bst = filter_vuln_df_by_severity(df, tree_type="BST", min_sev=6.0, max_sev=9.5)
        filtered_df_avl = filter_vuln_df_by_severity(df, tree_type="AVL", min_sev=6.0, max_sev=9.5)

        # Check that all remaining severities are within the specified range
        for sev in filtered_df_bst["Severity"]:
            self.assertGreaterEqual(sev, 6.0)
            self.assertLessEqual(sev, 9.5)
        for sev in filtered_df_avl["Severity"]:
            self.assertGreaterEqual(sev, 6.0)
            self.assertLessEqual(sev, 9.5)


if __name__ == "__main__":
    unittest.main()
