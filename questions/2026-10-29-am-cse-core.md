# 2026-10-29 AM — CSE Core (Medium)

## Question
What is the Open/Closed Principle in object‑oriented design, and how can a class hierarchy be refactored to satisfy this principle when new functionality needs to be added?

## Hint
Consider using abstraction and polymorphism so that existing code remains unchanged while new behavior is introduced.

## Answer
The Open/Closed Principle (OCP) states that software entities such as classes, modules, and functions should be open for extension but closed for modification. In practice, you should be able to add new functionality by writing new code rather than altering existing, tested code. A typical refactor introduces an abstract base class or interface that defines the required operations, with concrete subclasses implementing each behavior. When a new feature is required, you add a new subclass that implements the interface, leaving the original classes untouched, and client code interacts only with the abstraction, often via dependency injection or a factory. This approach reduces regression risk and improves maintainability.
