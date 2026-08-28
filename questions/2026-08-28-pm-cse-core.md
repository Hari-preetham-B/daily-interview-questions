# 2026-08-28 PM — CSE Core (Medium)

## Question
What is Two-Phase Locking (2PL) in DBMS, and how does Strict 2PL differ from Basic 2PL to prevent cascading rollbacks?

## Hint
Consider the exact moment when exclusive locks are released relative to the transaction's commit or abort phase.

## Answer
Two-Phase Locking (2PL) is a concurrency control protocol ensuring serializability through two distinct phases: the Growing Phase (acquiring locks) and the Shrinking Phase (releasing locks). In Basic 2PL, a transaction can start releasing locks at any point during its execution once it no longer needs the data, even before committing. This can cause cascading rollbacks if another transaction reads uncommitted data from a transaction that later aborts. Strict 2PL prevents this issue by requiring all exclusive (write) locks held by a transaction to be retained until the transaction completely commits or aborts. This guarantees that no other transaction can read uncommitted dirty data, eliminating cascading rollbacks and making recovery easier.
