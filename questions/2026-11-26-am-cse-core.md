# 2026-11-26 AM — CSE Core (Medium)

## Question
Explain how the Linux kernel’s slab allocator manages memory for frequently allocated and freed small objects. What advantages does it provide over the generic kmalloc allocator, and how does it help reduce fragmentation?

## Hint
Think about how the kernel keeps pre‑built chunks of memory ready for use, and how that affects allocation speed and memory layout.

## Answer
The slab allocator maintains a set of caches, each cache holding a number of pre‑allocated objects called slabs. When a request for a small object arrives, the allocator simply hands out a free object from the appropriate cache, avoiding the overhead of allocating a whole page. On free, the object is returned to its cache instead of being returned to the page allocator, which keeps the object in place for future reuse. This reduces fragmentation, improves cache locality, and speeds up both allocation and deallocation compared to the generic kmalloc path.
