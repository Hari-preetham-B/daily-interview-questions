# 2026-09-11 AM — CSE Core (Medium)

## Question
Why are B+ Trees generally preferred over standard B-Trees for database indexing in relational database management systems (RDBMS)?

## Hint
Consider where data pointers are stored in the tree structure and how leaf nodes are connected for sequential access.

## Answer
B+ Trees store data records (or data pointers) exclusively at the leaf nodes, whereas internal nodes only contain key values and child pointers used for routing. In contrast, B-Trees store data pointers in both internal and leaf nodes, which reduces node capacity (fan-out) and increases tree height, leading to higher disk I/O overhead. Furthermore, in a B+ Tree, all leaf nodes are linked together in a sequential doubly-linked list, allowing fast range queries and full index scans without re-traversing parent nodes. This combination of higher fan-out and efficient range-scanning capability makes B+ Trees ideal for disk-based database indexing.
