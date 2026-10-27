# 2026-10-27 PM — CSE Core (Medium)

## Question
What is the purpose of a page replacement algorithm in virtual memory systems, and how do the Least Recently Used (LRU) and Clock (Second-Chance) algorithms differ in terms of implementation complexity and performance trade‑offs?

## Hint
Consider how each algorithm decides which page to evict when a page fault occurs, and think about the data structures they require.

## Answer
A page replacement algorithm selects a victim frame to free when a page fault occurs and no free frames are available, aiming to minimize future faults. LRU evicts the page that has not been accessed for the longest time; it provides good approximation of optimal replacement but requires tracking exact access order, often using a stack or timestamps, which adds overhead. The Clock algorithm approximates LRU by arranging frames in a circular list with a reference bit; the hand sweeps the list, giving each page a second chance (clearing the bit) before eviction, resulting in lower hardware/software overhead and comparable performance in practice, though it may evict a page that was more recently used than LRU would.
