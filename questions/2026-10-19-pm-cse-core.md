# 2026-10-19 PM — CSE Core (Medium)

## Question
Explain the role of the 'page table walk' in translating virtual addresses to physical addresses in an x86‑64 system, and discuss how the TLB mitigates the performance impact of this process.

## Hint
Consider the hierarchical page tables and how a TLB cache can avoid repeated walks.

## Answer
In x86‑64, a virtual address is broken into a 4‑level page‑table index and an offset. The CPU walks each level (PML4, PDPT, PD, PT) by reading the corresponding page‑table entry from memory until it reaches the physical frame number, which can be expensive if done on every instruction. The Translation Lookaside Buffer (TLB) caches recently used virtual‑to‑physical translations; on a TLB hit, the walk is skipped entirely, dramatically reducing latency. When a translation is not in the TLB (a miss), the processor performs the walk and then inserts the mapping into the TLB for future use.
