# 2026-10-07 PM — CSE Core (Medium)

## Question
Explain the two-phase commit (2PC) protocol and how it ensures atomicity and consistency across distributed database transactions. What are the roles of the coordinator and participants, and what happens in each phase?

## Hint
Consider the prepare and commit/abort phases and the messages exchanged.

## Answer
In 2PC, a coordinator initiates a transaction and sends a prepare request to all participants. Each participant locks the necessary resources and votes either commit or abort, responding to the coordinator. In phase two, the coordinator sends a global commit if all votes were commit, or a global abort otherwise, and participants release locks accordingly. This guarantees that either all participants commit or all abort, ensuring atomicity and consistency across the distributed system.
