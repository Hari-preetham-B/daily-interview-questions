# 2026-10-03 PM — CSE Core (Medium)

## Question
What is thrashing in a virtual memory system, what causes it, and how does the working set model help prevent it?

## Hint
Consider the effect of frequent page faults on CPU utilization and the set of pages a process actively uses.

## Answer
Thrashing occurs when a system spends most of its time swapping pages in and out of memory rather than executing useful work, typically caused by a working set larger than available physical memory. As processes repeatedly reference pages not in RAM, page faults trigger excessive paging, leading to high CPU overhead and low throughput. The working set model mitigates thrashing by tracking the set of pages a process has referenced within a recent window of time; the OS can then ensure enough frames are allocated to keep this working set resident, or it may swap out entire processes whose working sets exceed the available memory, thereby reducing the paging rate.
