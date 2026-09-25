# 2026-09-25 PM — CSE Core (Medium)

## Question
Explain the difference between a process and a thread in terms of resource allocation, scheduling, and isolation. How do these differences impact the design of concurrent applications?

## Hint
Consider how each entity shares memory, how the OS schedules them, and what happens when one fails.

## Answer
A process is an independent execution unit with its own virtual address space, code, data, and system resources; it is scheduled by the OS as a single entity and has high isolation, meaning errors or crashes in one process do not directly affect others. A thread, however, is a lightweight subunit of a process that shares the process’s memory space, file descriptors, and other resources, but has its own stack and registers; threads are scheduled by the OS or by a user‑level library, and because they share memory, a fault in one thread can corrupt shared data affecting the entire process. These differences influence concurrent design: processes provide stronger fault isolation and security at the cost of higher overhead for context switches and inter‑process communication (IPC), while threads enable fine‑grained concurrency with lower overhead but require careful synchronization to avoid race conditions and deadlocks. Choosing between processes and threads depends on the required level of isolation, performance, and complexity of the application. 
