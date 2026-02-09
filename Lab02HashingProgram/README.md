**Lab02HashingProgram**
This project is my solution for Lab 02 – Hashing Program for ITIS 6200.

**Overview**

This Python program demonstrates the use of cryptographic hash functions to check file integrity. The program can scan a directory, compute hash values for all files, and store them in a JSON file. It can also verify the files later by recomputing their hashes and comparing them with the stored values.

The program supports the following features:
Generate a new hash table for all files in a directory
Verify files against the saved hash table
Detect modified files (invalid hash)
Detect deleted files
Detect newly added files
Detect renamed files when the content hash is unchanged 

**Files**
hashing_python.py – Main Python program
Screenshots/ – Contains screenshots showing the program output and required test cases
README.md – This file

**How to Run**

Open Anaconda Spyder, VS Code, or a terminal.

Run the program:

python hashing_python.py

You will see a menu:
Enter 1 to generate a new hash table
Enter 2 to verify hashes
Enter 3 to exit

When prompted, enter the full directory path you want to scan.

**How It Works**
When generating a hash table, the program goes through all files in the given directory and computes a SHA-256 hash for each file. These hashes and their file paths are saved into a JSON file. When verifying, the program reads the JSON file, scans the directory again, recomputes each file’s hash, and compares the results. It reports whether each file is valid, modified, deleted, new, or renamed.

**Screenshots**

All required screenshots for the assignment, including:
Program menu
Hash table generation
Folder and JSON before changes
Hash verification results (valid, invalid, deleted, new file, rename detection)
Folder and JSON after changes

are available in the Screenshots folder.
