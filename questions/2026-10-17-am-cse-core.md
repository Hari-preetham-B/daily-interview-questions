# 2026-10-17 AM — CSE Core (Medium)

## Question
What is Multiversion Concurrency Control (MVCC) in relational databases, and how does it enable concurrent reads and writes without locking conflicts?

## Hint
Think about how readers can see a consistent snapshot while writers create new versions of data rows. Consider the role of timestamps or transaction IDs in determining visibility.

## Answer
Multiversion Concurrency Control keeps multiple historical versions of each row, each tagged with transaction start and end timestamps. Read transactions obtain a snapshot timestamp and see only rows whose start timestamp is before the snapshot and whose end timestamp is after it, so they never block writers. Writers create a new version of a row with a new start timestamp; if two writers modify the same row, the database detects a conflict and aborts one of the transactions. This allows reads to proceed without acquiring locks, while write‑write conflicts are still detected and resolved at commit time. PostgreSQL, Oracle, and many NoSQL stores implement MVCC for high concurrency.
