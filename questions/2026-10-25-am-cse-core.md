# 2026-10-25 AM — CSE Core (Medium)

## Question
What is a Wait-For Graph in the context of deadlock detection, how does the operating system use it to detect deadlocks, and what are common recovery strategies once a deadlock is detected?

## Hint
Think about representing processes and their waiting relationships as a directed graph and look for cycles; then consider how to break such cycles.

## Answer
A Wait‑For Graph (WFG) is a directed graph where each node represents a process and an edge from Pi to Pj indicates that Pi is waiting for a resource currently held by Pj. The OS constructs or updates the WFG from the resource‑allocation table and periodically runs a cycle‑detection algorithm (e.g., depth‑first search); a cycle means a set of processes are deadlocked. After detection, typical recovery actions include terminating one or more victim processes in the cycle, preempting resources from selected processes and rolling them back, or aborting and restarting affected transactions. Victim selection is usually based on criteria such as minimal cost, priority, or the number of resources held.
