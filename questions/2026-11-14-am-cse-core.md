# 2026-11-14 AM — CSE Core (Medium)

## Question
Explain how Linux implements memory overcommit and the role of the overcommit_memory sysctl setting. What are the implications for applications that allocate large amounts of memory?

## Hint
Think about the kernel’s policy for allowing more virtual memory than physical RAM and how it signals when the limit is reached.

## Answer
Linux allows applications to request more virtual memory than the system actually has in RAM using overcommit. The overcommit_memory sysctl has three modes:
1. 0 – heuristic: the kernel estimates available RAM and decides at allocation time whether to allow the request.
2. 1 – always allow: every allocation succeeds; the kernel only checks during actual physical page allocation and may kill the process if it overuses memory.
3. 2 – no overcommit: the kernel rejects any allocation that would exceed the sum of RAM, swap, and a configurable overcommit factor. Applications that allocate large buffers must handle failures from malloc/alloca, and developers may set overcommit_memory=2 or tune vm.overcommit_ratio to protect against out‑of‑memory situations.
