# 2026-11-02 AM — CSE Core (Medium)

## Question
Explain the concept of copy‑on‑write in virtual memory, and describe how it improves memory efficiency when a process forks a child.

## Hint
Consider how the operating system handles page tables after a fork and what happens when either process modifies a page.

## Answer
Copy‑on‑write (COW) is a memory‑optimization technique used when a process forks. Initially, the child and parent share the same physical pages with read‑only permissions; the page table entries point to the same frames. When either process attempts to write to a shared page, the OS intercepts the fault, allocates a new physical page, copies the contents, updates the faulting process’s page table to point to the new page, and marks it writable. This avoids duplicating all pages up front, saving memory and reducing fork latency, and only duplicates pages that are actually modified.
