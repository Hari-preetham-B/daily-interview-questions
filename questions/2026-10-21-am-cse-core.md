# 2026-10-21 AM — CSE Core (Medium)

## Question
In object-oriented design, how do composition and aggregation differ, and in what scenarios would you prefer one over the other?

## Hint
Think about ownership lifetime and the strength of the relationship between the containing and contained objects.

## Answer
Composition implies a strong ownership: the container creates and destroys the contained object, and the contained object cannot exist independently. Aggregation is a weaker association; the container references an object that may outlive it and is often shared. Use composition when the contained object's lifecycle is tightly coupled to the container (e.g., a Car owns its Engine). Use aggregation when the contained object has an independent lifecycle and may be shared (e.g., a Library has Books that exist regardless of the Library).
