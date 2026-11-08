# 2026-11-08 PM — CSE Core (Medium)

## Question
What is the difference between TCP's slow start and congestion avoidance phases, and how do they affect throughput after a packet loss?

## Hint
Consider how the congestion window grows during each phase and what happens when a loss is detected.

## Answer
In TCP slow start, the congestion window starts small and grows exponentially, doubling each RTT until it reaches a predefined threshold. After that, congestion avoidance uses additive increase, adding roughly one maximum segment size per RTT. When a packet loss occurs, TCP assumes congestion and performs multiplicative decrease, reducing the congestion window to a fraction (typically half). This drop leads to a sudden decrease in throughput; slow start then re‑increases the window, producing a sawtooth pattern in throughput over time.
