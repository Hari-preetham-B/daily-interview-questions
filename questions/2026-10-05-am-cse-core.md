# 2026-10-05 AM — CSE Core (Medium)

## Question
In Java, what is the difference between an abstract class and an interface, and in which scenarios would you choose one over the other?

## Hint
Think about method implementation, inheritance, and the ability to provide default behavior.

## Answer
An abstract class can contain both abstract methods without implementation and concrete methods with implementation, allowing shared code and state via fields. An interface, until Java 8, could only declare abstract methods, but now can also provide default methods and static methods, yet it cannot hold instance fields. Use an abstract class when you want to share common implementation or maintain state among subclasses, especially when the classes belong to the same inheritance hierarchy. Use an interface when you need to define a contract that can be implemented by classes across unrelated hierarchies, or when you want to provide optional default behavior without forcing inheritance.
