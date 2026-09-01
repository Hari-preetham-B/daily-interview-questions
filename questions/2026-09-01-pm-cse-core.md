# 2026-09-01 PM — CSE Core (Medium)

## Question
What is the Copy-on-Write (CoW) resource management technique in Operating Systems, and how does it optimize the performance of the fork() system call?

## Hint
Consider whether a child process actually needs its own independent physical copy of all memory pages immediately upon creation.

## Answer
Copy-on-Write (CoW) is an optimization strategy where a child process created via `fork()` initially shares the parent process's physical memory pages instead of duplicating them immediately. These shared pages are marked as read-only in both the parent and child page tables. If either process attempts to write to a shared page, a page fault exception is raised by the MMU. The operating system handles this fault by allocating a new physical page, copying the data from the original page, updating the faulting process's page table entry with write permissions, and resuming execution. This prevents expensive memory allocation and copying overhead, which is especially beneficial when a `fork()` is immediately followed by an `exec()` call.
