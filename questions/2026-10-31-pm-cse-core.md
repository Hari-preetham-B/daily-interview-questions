# 2026-10-31 PM — CSE Core (Medium)

## Question
In relational database design, what is the difference between the First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF), and how do these normal forms prevent data anomalies?

## Hint
Think about the structure of tuples, functional dependencies, and the role of primary keys in eliminating redundancy.

## Answer
First Normal Form requires that every attribute of a relation be atomic—no repeating groups or arrays—and that each column contain a single value. Second Normal Form builds on 1NF by ensuring that every non‑key attribute is fully functionally dependent on the entire primary key (no partial dependencies on a composite key). Third Normal Form adds that all non‑key attributes must be non‑transitively dependent on the primary key; that is, no non‑key attribute should depend on another non‑key attribute. These constraints eliminate update, insertion, and deletion anomalies by reducing redundancy and ensuring that each piece of information is stored in exactly one place.
