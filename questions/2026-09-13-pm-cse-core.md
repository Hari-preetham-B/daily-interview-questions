# 2026-09-13 PM — CSE Core (Medium)

## Question
What is the Liskov Substitution Principle (LSP) in SOLID design, and how does violating it compromise program correctness?

## Hint
Consider the classic example where a Square class inherits from a Rectangle class and overrides width and height setters.

## Answer
The Liskov Substitution Principle (LSP) states that objects of a subclass should be able to substitute objects of a superclass without affecting the correctness or expected behavior of the program. Violating LSP occurs when a derived class alters the behavioral contract of the base class—such as throwing unexpected exceptions, relaxing preconditions, or strengthening postconditions (e.g., a Square class inheriting from Rectangle where changing the width unexpectedly modifies the height). Such violations force client code to introduce runtime type checks (`instanceof`) or special conditional logic for specific subclasses, tightly coupling the code and breaking the Open/Closed Principle.
