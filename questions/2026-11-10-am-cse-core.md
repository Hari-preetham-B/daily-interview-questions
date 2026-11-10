# 2026-11-10 AM — CSE Core (Medium)

## Question
What is Belady's anomaly in virtual memory systems, and under what conditions does it occur? Illustrate with an example where increasing the number of page frames leads to more page faults.

## Hint
Think about how different page replacement policies behave when the frame count changes, especially FIFO vs. LRU.

## Answer
Belady's anomaly refers to the counter‑intuitive situation where a paging algorithm (most commonly FIFO) results in more page faults when the number of available page frames increases. It occurs because the algorithm does not consider future page accesses; adding frames can change the order in which pages are evicted, sometimes causing a previously loaded page to be discarded prematurely. For example, consider the reference string 1,2,3,4,1,2,5,1,2,3,4,5 with 3 frames and FIFO: 9 faults. With 4 frames the same string yields 10 faults, demonstrating the anomaly. This effect does not happen with optimal or LRU policies, which are theoretically optimal or near‑optimal, respectively.
