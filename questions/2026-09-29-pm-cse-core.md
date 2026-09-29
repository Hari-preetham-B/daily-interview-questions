# 2026-09-29 PM — CSE Core (Medium)

## Question
What is the Interface Segregation Principle (ISP) in SOLID design, and how does adhering to it improve system maintainability and flexibility?

## Hint
Consider the problems caused by a single large interface that forces clients to depend on methods they never use, and how splitting it into smaller, client‑specific interfaces helps.

## Answer
The Interface Segregation Principle states that no client should be forced to depend on methods it does not use; therefore, interfaces should be fine‑grained and specific to the needs of each client. By breaking a "fat" interface into several smaller ones, each implementing class only needs to provide the behavior that its consumers require, reducing unnecessary coupling. This leads to easier code evolution because changes to one interface affect only the clients that actually use it, minimizing the risk of unintended side effects. It also enhances testability, as mock implementations can target only the relevant subset of functionality, and improves readability by clarifying the contract each client expects.
