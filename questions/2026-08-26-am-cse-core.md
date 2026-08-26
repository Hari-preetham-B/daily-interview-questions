# 2026-08-26 AM — CSE Core (Medium)

## Question
What is the key difference between Flow Control and Congestion Control in TCP, and what mechanism is used to implement Flow Control?

## Hint
Think about who is being protected from data overflow in each scenario: the receiving host or the intermediate network nodes.

## Answer
Flow Control prevents a fast sender from overwhelming a slow receiver, whereas Congestion Control prevents the sender from overwhelming the intermediate network infrastructure (routers and links). TCP implements Flow Control using the Sliding Window protocol, where the receiver continuously communicates its available buffer capacity to the sender via the 'Receive Window' (rwnd) field in the TCP header. In contrast, Congestion Control dynamically adjusts traffic based on network capacity using a 'Congestion Window' (cwnd) and algorithms like Slow Start, Congestion Avoidance, and Fast Retransmit.
