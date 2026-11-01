# 2026-11-01 PM — Behavioral (Medium)

## Question
Describe a situation where you had to mediate a disagreement between a senior engineer and a junior developer over the choice of algorithm for a performance‑critical component, and how you facilitated a resolution.

## Hint
Think about balancing technical merit with team harmony and how you gathered input from both sides.

## Answer
During a sprint I noticed a senior engineer and a junior developer were at odds about whether to use a binary search tree or a hash map for a lookup feature that would be used millions of times a day. I called a short stand‑up, asked each to explain their reasoning and the trade‑offs in terms of time complexity, memory usage, and maintainability. I then suggested we benchmark a small prototype with realistic data to see the actual performance difference. The prototype showed the hash map was faster in practice, but the tree was easier to maintain with future updates. We agreed to use the hash map for the current release and keep the tree implementation in the codebase for future extensions, ensuring both parties felt heard and the decision was data‑driven. The feature shipped on time, performance met expectations, and the team gained confidence in collaborative decision‑making. 
