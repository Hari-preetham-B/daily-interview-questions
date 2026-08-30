# 2026-08-30 AM — CSE Core (Medium)

## Question
Explain the four standard SQL Transaction Isolation Levels and the specific read phenomena (Dirty Read, Non-Repeatable Read, Phantom Read) each level prevents.

## Hint
Consider how locks or multi-version concurrency control (MVCC) restrict visibility of uncommitted or newly committed changes between concurrent transactions.

## Answer
SQL isolation levels define how changes made by one transaction are isolated from other concurrent transactions. 1. Read Uncommitted: Allows transactions to read uncommitted changes, making it susceptible to Dirty Reads, Non-Repeatable Reads, and Phantom Reads. 2. Read Committed: Guarantees that any data read is committed at the moment it is read, preventing Dirty Reads, but still allowing Non-Repeatable Reads and Phantom Reads. 3. Repeatable Read: Ensures that if a transaction reads a row, subsequent reads of that same row will return the same data, preventing Dirty Reads and Non-Repeatable Reads, though Phantom Reads (new rows inserted by concurrent transactions) can still occur. 4. Serializable: The highest isolation level, enforcing total isolation (often via range locks or snapshot isolation) to prevent all three phenomena: Dirty Reads, Non-Repeatable Reads, and Phantom Reads.
