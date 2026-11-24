# 2026-11-24 PM — CSE Core (Medium)

## Question
How does HTTP/2 achieve multiplexing of multiple request/response streams over a single TCP connection, and what mechanisms does it use to avoid head‑of‑line blocking? Explain the role of stream identifiers, frames, and stream priority.

## Hint
Think about how data is broken into smaller units that carry a stream ID and how the protocol can interleave those units on one TCP flow.

## Answer
HTTP/2 splits each request/response into a sequence of frames, each prefixed with a 9‑byte header that includes a 31‑bit stream identifier. Because frames from different streams can be interleaved arbitrarily on the same TCP stream, the client and server can transmit multiple concurrent conversations over a single connection. To avoid head‑of‑line blocking, HTTP/2 uses flow‑control windows per stream and per connection, so a slow stream does not stall others. Additionally, each stream can be assigned a priority (weight and parent stream) so that the receiver can decide which streams to transmit first. These mechanisms together allow concurrent, independent streams while keeping the underlying TCP connection free of per‑stream stalls.
