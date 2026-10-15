# 2026-10-15 PM — CSE Core (Medium)

## Question
Explain the phenomenon known as "write‑skew" that can occur under Snapshot Isolation in a relational database. How can this anomaly lead to integrity constraint violations, and what techniques can be used to prevent it?

## Hint
Consider two concurrent transactions that read the same rows but update different rows; think about a uniqueness or sum constraint that could be broken.

## Answer
Write‑skew is an anomaly where two concurrent transactions, each reading a set of rows and then updating disjoint rows, commit under Snapshot Isolation without seeing each other's updates. Because each transaction bases its decision on a snapshot that does not include the other’s write, a global integrity constraint (e.g., only one row may have a certain flag set) can be violated after both commit. Snapshot Isolation prevents only write‑write conflicts on the same row, not logical conflicts across rows. To avoid write‑skew, one can use a stronger isolation level such as serializable, employ predicate locking, add explicit checks that enforce the constraint, or introduce a dummy row that all transactions lock to create a write‑write conflict.
