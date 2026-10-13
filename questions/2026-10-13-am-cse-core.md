# 2026-10-13 AM — CSE Core (Medium)

## Question
What is the difference between optimistic and pessimistic locking mechanisms in relational database systems, and in which scenarios would each approach be more appropriate? Provide an example transaction scenario for each.

## Hint
Consider how each method detects or prevents conflicts and when conflicts are expected to occur.

## Answer
Optimistic locking assumes that conflicts are rare. Transactions proceed without acquiring locks on data; when they finish, they check whether any data they read has been modified by another transaction (typically via a version number or timestamp). If a conflict is detected, the transaction is rolled back or retried. This approach is efficient for read‑heavy workloads with low contention, such as reporting or web applications where many users read data but few update the same rows.

Pessimistic locking, by contrast, preemptively acquires exclusive locks on data that a transaction intends to modify. The locks are held until the transaction commits or aborts, preventing other transactions from reading or writing the locked data. This is suitable for workloads with high contention or where consistency is critical, such as financial systems where concurrent updates to the same account must be serialized.

Example optimistic: A user edits a profile record. The application reads the row, shows the data, and when the user submits, the system checks that the version number hasn’t changed. If it has, the update fails and the user is notified.

Example pessimistic: A bank transfer transaction locks both the source and destination account rows before debiting and crediting, ensuring no other transfer can modify those accounts until the transaction completes.
