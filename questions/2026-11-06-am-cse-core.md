# 2026-11-06 AM — CSE Core (Medium)

## Question
Explain the TCP three‑way handshake process used to establish a reliable connection, including the purpose of each segment and how sequence numbers are initialized and acknowledged.

## Hint
Consider the SYN, SYN‑ACK, and ACK packets and how each side picks an initial sequence number.

## Answer
The TCP three‑way handshake starts with the client sending a SYN segment containing its initial sequence number (ISN). The server replies with a SYN‑ACK segment that acknowledges the client’s ISN (ACK = client ISN + 1) and includes its own ISN. Finally, the client sends an ACK segment acknowledging the server’s ISN (ACK = server ISN + 1). This exchange synchronizes both ends' sequence numbers, confirming that both parties are ready to transmit data and establishing the parameters for reliable, ordered delivery.
