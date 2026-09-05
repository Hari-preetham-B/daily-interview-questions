# 2026-09-05 PM — CSE Core (Medium)

## Question
What is Priority Inversion in real-time operating systems, and how does the Priority Inheritance Protocol resolve this issue?

## Hint
Consider a scenario where a medium-priority process preempts a low-priority process that currently holds a mutex needed by a high-priority process.

## Answer
Priority Inversion is a scenario in operating systems where a high-priority process is indirectly delayed by a lower-priority process. This occurs when a low-priority process holds a shared resource (via a lock) required by the high-priority process, and a medium-priority process—which does not need the resource—preempts the low-priority process, causing the high-priority process to wait indefinitely. The Priority Inheritance Protocol resolves this by temporarily boosting the priority of the low-priority process holding the lock to match that of the waiting high-priority process. Once the low-priority process releases the shared resource, its priority reverts to its original level, allowing the high-priority process to immediately acquire the lock and execute without being blocked by medium-priority tasks.
