# 2026-08-24 PM — CSE Core (Medium)

## Question
What is Belady's Anomaly in Operating Systems, and which page replacement algorithms are susceptible or immune to it?

## Hint
Consider the unexpected effect of increasing the number of allocated page frames on the total count of page faults.

## Answer
Belady's Anomaly is the phenomenon where increasing the number of page frames allocated to a process leads to an increase, rather than a decrease, in the number of page faults. This counter-intuitive behavior occurs in certain page replacement algorithms, most notably First-In, First-Out (FIFO). In contrast, stack-based algorithms such as Least Recently Used (LRU) and Optimal Page Replacement (OPT) are completely immune to Belady's Anomaly. This immunity exists because, for stack algorithms, the set of pages residing in memory with N frames is guaranteed to be a subset of the pages that would reside in memory with N+1 frames.
