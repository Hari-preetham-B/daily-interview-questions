# 2026-10-23 PM — CSE Core (Medium)

## Question
What is a race condition in multithreaded programming, and what mechanisms (such as mutexes, atomic operations, or memory barriers) can be used to prevent it?

## Hint
Consider how unsynchronized access to shared mutable data can lead to nondeterministic results, and recall the primitives that enforce ordering or exclusive access.

## Answer
A race condition occurs when two or more threads access and modify shared data concurrently without proper synchronization, leading to unpredictable results depending on the execution order. It typically arises from unsynchronized reads/writes to mutable variables. To prevent race conditions, programmers can use mutexes or other lock primitives to ensure exclusive access, employ atomic operations that guarantee indivisible read-modify-write semantics, or insert memory barriers/fences that enforce ordering constraints on CPU and compiler optimizations. These mechanisms serialize access or establish a happens‑before relationship, making the program's behavior deterministic.
