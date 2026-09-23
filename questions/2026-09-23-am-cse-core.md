# 2026-09-23 AM — CSE Core (Medium)

## Question
Explain the difference between preemptive and cooperative multitasking in operating systems and give an example of each.

## Hint
Think about how the CPU scheduler decides when to switch tasks.

## Answer
In preemptive multitasking the OS kernel can interrupt a running task at any time and switch to another, using timers or signals; this allows fair CPU sharing but requires context switching overhead. An example is Windows or Linux preemptive scheduler. In cooperative multitasking a task voluntarily yields control, typically by calling a yield or sleep function; the OS trusts the task to give up the CPU, as in early Mac OS or classic Windows 3.x. The latter can lead to unresponsive applications if a task never yields.
