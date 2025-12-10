#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import time
from bst import Node
from bst import BSTree
from avl import AVLTree
from typing import Optional

def _process_cwe(cwe_str):
	"""Convert CWE strings to lists, remove 'NVD-CWE-noinfo', handle 'N/A'"""
	if pd.isna(cwe_str) or cwe_str == "N/A":
		return []
	cwe_list = [c.strip() for c in cwe_str.split(";") if c.strip() != "NVD-CWE-noinfo"]
	return cwe_list

def load_vuln_data(path: str) -> pd.DataFrame:
	"""Load vulnerability data from a local path into a DataFrame."""
	# Parse the first column as datetime and set it as the index so callers
	# can rely on a datetime index and station columns only.
	# Use index_col=0 to avoid keeping the datetime as a regular column.
	vuln_data = pd.read_csv(path, parse_dates=["Date"], index_col="CVE")

	# Change severities to floats, and CWEs to lists (remove NVD-CWE-noinfo from list)

	# Convert Severity to float, N/A -> NaN
	vuln_data["Severity"] = pd.to_numeric(vuln_data["Severity"], errors="coerce")

	# Process CWEs to put them into proper format
	vuln_data["CWE"] = vuln_data["CWE"].apply(_process_cwe)
	
	return vuln_data


def make_vuln_bst(vuln_data: pd.DataFrame) -> BSTree:
	"""Load vulnerability data from a DataFrame into a binary search tree 
	sorted by severity."""
	bst = BSTree()
	# Iterate through vulnerabilities in vuln_data, inserting them such that
	# the key is the severity, and the value is the rest of the data as a dict
	for index, vuln in vuln_data.iterrows():
		# skip NaN severities
		if pd.isna(vuln["Severity"]):
			continue
		bst.insert(vuln["Severity"], {"CVE": index, 
				   "Date": vuln["Date"], "CWE": vuln["CWE"]})
	return bst
	

def make_vuln_avl(vuln_data: pd.DataFrame) -> AVLTree:
	"""Load vulnerability data from a DataFrame into an AVL tree sorted
	by severity."""
	avl = AVLTree()
	# Iterate through vulnerabilities in vuln_data, inserting them such that
	# the key is the severity, and the value is the rest of the data as a dict
	for index, vuln in vuln_data.iterrows():
		# skip NaN severities
		if pd.isna(vuln["Severity"]):
			continue
		avl.insert(vuln["Severity"], {"CVE": index, 
				   "Date": vuln["Date"], "CWE": vuln["CWE"]})
	return avl

def severity_range_query(node: Node, min_sev: float, max_sev: float):
	"""Return a list of vulnerability dicts whose severity is in [min_sev, max_sev]."""
	if node is None:
		return []

	results = []

	# Left subtree may contain values >= min_sev
	if node.key >= min_sev:
		results.extend(severity_range_query(node.left, min_sev, max_sev))

	# This node is inside the range
	if min_sev <= node.key <= max_sev:
		results.append(node.value)

	# Right subtree may contain values <= max_sev
	if node.key <= max_sev:
		results.extend(severity_range_query(node.right, min_sev, max_sev))

	return results

def filter_vuln_df_by_severity(df: pd.DataFrame, tree_type: str, min_sev: float, max_sev: float) -> pd.DataFrame:
	"""
	Build a vulnerability tree (BST or AVL) from df, 
	range-search by severity, and return a new DataFrame 
	with only vulnerabilities in [min_sev, max_sev].
	"""
	# Build the tree
	if tree_type == "BST":
		tree = make_vuln_bst(df)
	elif tree_type == "AVL":
		tree = make_vuln_avl(df)
	else:
		raise ValueError("tree_type must be 'BST' or 'AVL'")

	# Range search
	in_range = severity_range_query(tree.root, min_sev, max_sev)

	# Extract the CVEs from the returned dicts
	cve_keys = [v["CVE"] for v in in_range]

	# Return a filtered DataFrame using the CVEs as index
	return df.loc[cve_keys].copy()


def plot_sev_by_CWE(df: pd.DataFrame) -> plt.Axes:
	"""
	Make bar graph of average severity for top
	25 most common CWEs
	"""
	# Explode function allows a vulnerability to counted
	# once for each CWE in its list
	df = df.explode("CWE")

	# Count CWEs
	cwe_counts = df["CWE"].value_counts()
	top_cwes = cwe_counts.head(25).index  # top 25 most common

	# Filter for only those top CWEs
	df = df[df["CWE"].isin(top_cwes)]

	# Get average severity for each CWE
	avg_sev = df.groupby("CWE")["Severity"].mean()

	# Make bar graph
	fig, ax = plt.subplots()
	ax.bar(avg_sev.index, avg_sev.values)
	ax.set_xlabel("CWE")
	ax.set_ylabel("Average Severity")
	ax.set_title("Average Severity by CWE")
	plt.setp(ax.get_xticklabels(), rotation=90, ha="center", va="top")
	plt.tight_layout()

	return ax

def plot_num_by_CWE(df: pd.DataFrame) -> plt.Axes:
	"""
	Make bar graph of number of vulnerabilites for 
	top 25 most common CWEs
	"""
	# Get count for each CWE
	# Explode function allows a vulnerability to counted
	# once for each CWE in its list
	cwe_counts = df["CWE"].explode().value_counts()
	
	# Keep only top 25 CWEs
	cwe_counts = cwe_counts.head(25)

	# Make bar graph
	fig, ax = plt.subplots()
	ax.bar(cwe_counts.index, cwe_counts.values)
	ax.set_xlabel("CWE")
	ax.set_ylabel("Number of Vulnerabilities")
	ax.set_title("Vulnerabilities by CWE")
	plt.setp(ax.get_xticklabels(), rotation=90, ha="center", va="top")
	plt.tight_layout()

	return ax

def plot_num_by_month(df: pd.DataFrame) -> plt.Axes:
	"""Make connected scatter plot of number of vulnerabilites by month"""

	# Set Date as index for resampling
	df = df.set_index("Date")

	# Resample by month and count vulnerabilities
	monthly_counts = df["Severity"].resample("MS").count()

	fig, ax = plt.subplots()
	ax.plot(monthly_counts.index, monthly_counts.values, marker='o')

	ax.set_xlabel("Month")
	ax.set_ylabel("Number of Vulnerabilities")
	ax.set_title("Vulnerabilities Per Month")

	# Major ticks: every month
	ax.xaxis.set_major_locator(mdates.MonthLocator())
	ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))

	plt.setp(ax.get_xticklabels(), rotation=90, ha="center", va="top")

	plt.tight_layout()
	return ax

def main():
	sys.setrecursionlimit(5000)
	print("=== Vulnerability Tree Demo ===")

	df = None
	while True:
		try:
			path = input("Enter CSV path for vulnerability data (e.g., vuln_data_small.csv):\n").strip()
			# Load the CSV
			df = load_vuln_data(path)
			break
		except FileNotFoundError:
			print("File not found. Please enter a valid path.")
	print(f"Loaded {len(df)} vulnerabilities.")

	# Ask which tree to use
	tree_choice = ""
	while True:
		tree_choice = input("Filter using which tree? (BST/AVL):\n").strip().upper()
		if tree_choice in ("BST", "AVL"):
			break
		else:
			print("Invalid input, please try again.")

	filtered_df = None
	# Ask for a severity range to filter
	while True:
		try:
			min_sev = float(input("Enter minimum severity for filtering (0.0-10.0):\n"))
			max_sev = float(input("Enter maximum severity for filtering (0.0-10.0):\n"))
			if (not (0.0 <= min_sev <= 10.0) or not (0.0 <= max_sev <= 10.0)
				or not min_sev <= max_sev):
				print("Invalid range, please try again.")
				continue
			# Filter the tree and time it
			start_time = time.time()
			filtered_df = filter_vuln_df_by_severity(df, tree_choice, min_sev, max_sev)
			if len(filtered_df) == 0:
				print("No vulnerabilities found in range, please try again.")
				continue
			elapsed = time.time() - start_time
			print(f"Found {len(filtered_df)} vulnerabilities in severity range [{min_sev}, {max_sev}].")
			print(f"Filtered in {elapsed:.4f} seconds")
			break
		except ValueError:
			print("Invalid input, please try again.")


	# Plot options
	while True:
		print("\nPlotting options for this severity range:")
		print("1 - Number of vulnerabilities by CWE (top 25 most common CWEs)")
		print("2 - Average severity by CWE (top 25 most common CWEs)")
		print("3 - Number of vulnerabilities added to database by month")
		print("0 - Exit plotting")
		choice = input("Enter your choice: \n").strip()

		if choice == "1":
			print("Please see desktop for plot.")
			ax = plot_num_by_CWE(filtered_df)
			plt.show()
		elif choice == "2":
			print("Please see desktop for plot.")
			ax = plot_sev_by_CWE(filtered_df)
			plt.show()
		elif choice == "3":
			print("Please see desktop for plot.")
			ax = plot_num_by_month(filtered_df)
			plt.show()
		elif choice == "0":
			break
		else:
			print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()