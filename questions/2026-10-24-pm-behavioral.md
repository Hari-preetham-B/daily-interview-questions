# 2026-10-24 PM — Behavioral (Medium)

## Question
Describe a situation where you identified a potential ethical issue or security concern in a codebase or project you were working on. How did you address it with your team or stakeholders, and what was the outcome?

## Hint
Think about a scenario where something you discovered could affect user data or company reputation, and how you communicated it.

## Answer
During a mid‑term sprint for a web app, I noticed that the password reset endpoint accepted any email address without validation, potentially exposing user data to attackers. I first documented the flaw with screenshots and a risk assessment, then scheduled a brief meeting with the product owner and lead engineer. We discussed the severity, proposed adding proper email verification and rate‑limiting, and agreed on a quick patch. I wrote the fix, ran unit and integration tests, and pushed it to staging. The patch was deployed within a day, and the team added a new security review step to the CI pipeline to prevent similar issues.
