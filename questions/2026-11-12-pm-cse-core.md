# 2026-11-12 PM — CSE Core (Medium)

## Question
Explain the structure of a B+ tree and how it differs from a B‑tree in terms of leaf node organization and data lookup efficiency. Why is a B+ tree preferred for database indexing?

## Hint
Consider where the actual records are stored and how the leaf nodes are linked.

## Answer
In a B+ tree, all keys are stored in the leaf nodes, while internal nodes only contain copy of keys used for routing. The leaf nodes are linked in a doubly‑linked list, which allows range scans to be performed efficiently. This separation means that internal nodes can hold more keys, reducing tree height compared to a B‑tree where keys and pointers to data are mixed. Consequently, B+ trees provide better cache locality and faster sequential access, making them the preferred structure for database indexes.
