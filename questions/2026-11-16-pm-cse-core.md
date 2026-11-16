# 2026-11-16 PM — CSE Core (Medium)

## Question
Explain how the priority inheritance protocol (PIP) works in a real‑time operating system to prevent priority inversion. What are the key steps involved when a high‑priority task is blocked by a lower‑priority task holding a shared resource?

## Hint
Consider what happens to the priority of the task that holds the lock when another task of higher priority is waiting for it.

## Answer
In priority inheritance, when a high‑priority task becomes blocked waiting for a lock held by a lower‑priority task, the lower‑priority task temporarily inherits the higher priority. This allows the lock holder to finish quickly and release the resource, reducing the blocking time for the high‑priority task. Once the lock is released, the holder reverts to its original priority. The protocol also propagates the highest waiting priority up nested lock chains, thereby preventing priority inversion and guaranteeing bounded waiting for high‑priority tasks.
