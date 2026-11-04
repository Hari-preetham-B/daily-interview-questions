# 2026-11-04 PM — CSE Core (Medium)

## Question
What is the purpose of a memory balloon device in a virtualized environment, and how does it help manage memory between the host and guest operating systems?

## Hint
Think about how a guest OS can signal its memory needs to the hypervisor and how the hypervisor can reclaim unused memory.

## Answer
A memory balloon device is a virtual device presented to the guest OS that lets the guest inflate or deflate a memory buffer. When the guest needs more memory, it inflates the balloon, allocating pages to the balloon driver; these pages are then reported to the hypervisor as free, allowing the host to reclaim memory for other guests. Conversely, if the host needs to free memory, the hypervisor can deflate the balloon, forcing the guest to release pages. This dynamic mechanism enables efficient sharing of physical RAM among multiple virtual machines without hard limits.
