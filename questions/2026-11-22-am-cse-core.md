# 2026-11-22 AM — CSE Core (Medium)

## Question
Describe the process a DNS resolver follows to translate a hostname into an IP address. Include the role of recursive and iterative queries, root servers, TLD servers, and authoritative servers. Explain how DNS caching improves lookup speed and reduces load on servers.

## Hint
Think about the chain of servers the resolver contacts, and how cached records can skip some steps.

## Answer
When a client wants to resolve "www.example.com", the local resolver first checks its cache; if the record is not found, it sends a recursive query to a root server. The root server returns the address of the TLD (.com) server. The resolver then queries the TLD server, which returns the authoritative server for "example.com". Finally, the resolver contacts the authoritative server, which returns the A record. The resolver caches this record for a period defined by its TTL, so future queries for the same name can be answered immediately, reducing latency and load on the hierarchy of DNS servers.
