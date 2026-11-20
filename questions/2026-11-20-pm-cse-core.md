# 2026-11-20 PM — CSE Core (Medium)

## Question
Describe how a Linux page fault handler decides whether to bring a page from disk into RAM or to kill a process, and explain the role of the 'swappiness' setting in this decision.

## Hint
Consider the current memory pressure and how the kernel uses the swap file or swap partition when a fault occurs.

## Answer
When a page fault occurs, the kernel first checks if the faulting page is a valid page that was previously swapped out. If it is, the kernel brings the page back into RAM by reading it from the swap area, then updates the page table. If the faulting address is invalid (e.g., points to unmapped memory), the kernel will terminate the process with a segmentation fault. When memory pressure is high, the kernel may decide to evict other pages to free up space before bringing in the faulting page. The 'swappiness' sysctl value (0–100) controls how aggressively the kernel swaps memory pages: a higher value makes the kernel favor swapping out pages, which can reduce page faults but increase disk I/O; a lower value keeps more pages in RAM, reducing swap activity but risking out‑of‑memory (OOM) kills if memory runs low.
