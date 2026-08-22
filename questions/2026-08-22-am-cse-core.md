# 2026-08-22 AM — CSE Core (Medium)

## Question
What is the key difference between a Clustered Index and a Non-Clustered Index in a Relational Database Management System (RDBMS), and how do they impact data retrieval performance?

## Hint
Think about how data rows are physically stored on disk relative to the index structure, and how many of each index type can exist on a single table.

## Answer
A Clustered Index determines the physical order of data rows in a table, which means a table can have only one Clustered Index. In contrast, a Non-Clustered Index creates a separate structure that stores index keys along with pointers (such as primary keys or row IDs) to the actual data, allowing multiple non-clustered indexes per table. Clustered indexes provide faster retrieval for range queries because the data is stored sequentially on disk. Non-Clustered indexes are ideal for quick point lookups on specific non-primary columns, though retrieving non-indexed attributes requires an additional lookup step to the base table.
