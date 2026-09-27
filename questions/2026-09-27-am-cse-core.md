# 2026-09-27 AM — CSE Core (Medium)

## Question
Explain the Write-Ahead Logging (WAL) protocol used in relational database systems and how it guarantees atomicity and durability during crash recovery. What are the main steps involved in the redo and undo phases of the recovery process?

## Hint
Consider the ordering requirement of log entries relative to physical data changes, and how the recovery algorithm scans the log before and after the crash point.

## Answer
Write‑Ahead Logging (WAL) requires that every modification to database pages be recorded in a persistent log before the actual data page is updated on disk, ensuring that the log contains a complete, recoverable history of all changes. During recovery, the system first performs a redo phase: it scans the log forward from the last checkpoint, applying every logged update to the database pages to guarantee that all committed transactions are reflected on disk. Next, it performs an undo phase by scanning the log backward from the checkpoint, rolling back any uncommitted transactions by applying the inverse of their logged updates. This two‑pass process guarantees atomicity (uncommitted changes are undone) and durability (committed changes survive crashes).
