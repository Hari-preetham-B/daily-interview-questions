# 2026-09-03 AM — CSE Core (Medium)

## Question
What is the primary purpose of the TIME_WAIT state during TCP connection teardown, and why is its duration typically set to 2 times the Maximum Segment Lifetime (2 * MSL)?

## Hint
Consider what happens to packets that are delayed in transit across the network and how a new connection reusing the same socket pair could be affected.

## Answer
The TIME_WAIT state is entered by the TCP endpoint that initiates the active close after sending the final ACK in the four-way handshake. Its primary purpose is twofold: first, to ensure the remote peer receives the final ACK (if the ACK is lost, the peer retransmits its FIN, requiring a re-sent ACK); second, to allow any delayed or duplicate packets from the closed connection to naturally expire in the network. The duration is set to 2 * MSL (Maximum Segment Lifetime) to guarantee that the maximum time a packet can exist in transit in both directions (to and from the destination) has elapsed before the same local IP/port combination can be reused for a new connection.
