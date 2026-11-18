# 2026-11-18 AM — CSE Core (Medium)

## Question
What is the Liskov Substitution Principle (LSP) in object‑oriented design, and how does adhering to it affect the correctness and extensibility of class hierarchies?

## Hint
Consider what must remain true when a subclass instance is used wherever a base‑class instance is expected, especially regarding method contracts.

## Answer
The Liskov Substitution Principle states that objects of a superclass must be replaceable with objects of any subclass without affecting program correctness. This means a subclass cannot strengthen preconditions, weaken postconditions, or violate invariants defined by the base class. When LSP is respected, polymorphic code works reliably and new subclasses can be added without breaking existing functionality, improving extensibility. Violations often appear when a subclass changes the expected behavior, such as a Square subclass of Rectangle that restricts width and height independently, breaking client code that assumes independent dimension changes.
