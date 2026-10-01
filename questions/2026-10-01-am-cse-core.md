# 2026-10-01 AM — CSE Core (Medium)

## Question
Explain how the Linux Completely Fair Scheduler (CFS) approximates fairness using virtual runtime, and describe a scenario where CFS might lead to starvation of a low‑priority task.

## Hint
Think about how CFS keeps track of each task’s execution time and how it uses a red‑black tree to select the next task.

## Answer
CFS maintains a virtual runtime (vruntime) for each task, which increases by the actual CPU time the task has consumed, but is scaled by the task’s nice value so that lower‑priority tasks accumulate vruntime faster. All runnable tasks are stored in a red‑black tree keyed by vruntime; the task with the smallest vruntime is selected next, ensuring that over time each task gets a proportional share of CPU. Because CFS always picks the task with the lowest vruntime, a very low‑priority task that has never run will have a very low vruntime and can be scheduled frequently. However, if a group of high‑priority tasks keeps consuming CPU, their vruntime grows slowly, staying ahead of the low‑priority task, which can lead to the low‑priority task being starved for extended periods, especially in systems with many active high‑priority threads or in real‑time workloads where priority inversion occurs.
