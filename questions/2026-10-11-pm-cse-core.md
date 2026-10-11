# 2026-10-11 PM — CSE Core (Hard)

## Question
In a preemptive multitasking operating system, how does the scheduler decide which process to run next, and what role does the CPU's cache (specifically L1 cache) play during a context switch? Explain the impact on performance and how modern OSes mitigate cache thrashing.

## Hint
Consider the scheduler’s data structures and the cache state that is preserved or flushed when a process is swapped in or out. Think about cache line reuse and how TLB entries are managed across contexts.

## Answer
The scheduler picks the next process based on its policy (e.g., round‑robin, priority‑based, or multi‑level feedback queue). It maintains per‑process state such as run‑queue position, priority, and estimated CPU burst. When a context switch occurs, the CPU’s L1 data and instruction caches are still occupied with the previous process’s data. If the new process touches the same cache lines, a cache hit can happen; otherwise, the cache must be refilled, leading to a miss penalty. Modern OSes mitigate this by using cache‑friendly scheduling: they try to keep processes that share memory (or are in the same locality group) on the same core for as long as possible, use cache‑aware data structures, and employ techniques like cache prefetching or TLB shootdown minimization. Some systems also support “cache partitioning” or “cache locking” for real‑time tasks to reduce interference.

