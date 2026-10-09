# 2026-10-09 AM — CSE Core (Medium)

## Question
Explain the difference between composition and inheritance in object-oriented design and give an example of a scenario where composition is preferred over inheritance.

## Hint
Consider the "has‑a" versus "is‑a" relationship and think about flexibility and encapsulation.

## Answer
Composition is a "has‑a" relationship where a class contains an instance of another class, enabling it to delegate responsibilities and change behavior at runtime. Inheritance is an "is‑a" relationship where a subclass extends a parent class and inherits its implementation, often leading to tighter coupling. Composition is preferred when you need to vary behavior dynamically, promote encapsulation, or avoid fragile base class problems. For example, a Car class can have a Engine object (composition) rather than inherit from an Engine class, allowing the car to swap engines or modify engine behavior without altering the Car hierarchy.
