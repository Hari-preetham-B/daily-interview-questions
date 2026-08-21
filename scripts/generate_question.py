#!/usr/bin/env python3
"""
Daily Interview Question Generator
-----------------------------------
Calls the Anthropic API to generate ONE new interview question per run,
rotating across categories (AIML, CSE Core, DSA, Behavioral), avoiding
repeats of anything already asked, and updates:
  - data/questions.json   (full history, structured)
  - questions/YYYY-MM-DD-<category>.md   (dated question file with answer/hints)
  - README.md             (rotating "today's question" + stats + index)

Run daily via GitHub Actions. Requires env var ANTHROPIC_API_KEY.
"""

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "questions.json"
QUESTIONS_DIR = ROOT / "questions"
README_FILE = ROOT / "README.md"

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"  # fast + cheap, fine for this task. Bump to "claude-sonnet-5" for higher-effort questions.

# Rotate categories by day-of-year so you get an even, predictable spread
CATEGORIES = ["DSA", "AIML", "CSE Core", "Behavioral"]

CATEGORY_PROMPTS = {
    "DSA": (
        "a Data Structures & Algorithms interview question suitable for placement/internship "
        "interviews (arrays, linked lists, trees, graphs, DP, recursion, sorting/searching, "
        "time/space complexity). Prefer questions that could realistically appear at a product "
        "or service-based company interview."
    ),
    "AIML": (
        "an Artificial Intelligence / Machine Learning interview question suitable for an "
        "AI/ML engineering or research internship interview (ML fundamentals, deep learning, "
        "NLP, CV, model evaluation, classic algorithms like linear/logistic regression, "
        "decision trees, neural nets, overfitting, bias-variance, etc.)."
    ),
    "CSE Core": (
        "a core Computer Science Engineering interview question from OS, DBMS, Computer "
        "Networks, or OOP concepts (e.g. deadlocks, normalization, TCP/IP, indexing, "
        "process scheduling, virtual memory, SOLID principles)."
    ),
    "Behavioral": (
        "a behavioral / HR interview question commonly asked in software or tech internship "
        "interviews (teamwork, conflict resolution, failure, leadership, time management, "
        "why-this-company style questions)."
    ),
}


def load_history() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"questions": []}


def save_history(history: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(history, indent=2))


def pick_category(history: dict) -> str:
    day_index = date.today().timetuple().tm_yday
    return CATEGORIES[day_index % len(CATEGORIES)]


def recent_questions_text(history: dict, category: str, limit: int = 25) -> str:
    same_cat = [q["question"] for q in history["questions"] if q["category"] == category]
    recent = same_cat[-limit:]
    if not recent:
        return "(none yet)"
    return "\n".join(f"- {q}" for q in recent)


def call_claude(category: str, history: dict) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    avoid_list = recent_questions_text(history, category)

    system_prompt = (
        "You generate ONE new interview question at a time for a computer science / AI-ML "
        "student preparing for internship and placement interviews. "
        "Return ONLY valid JSON, no markdown fences, no preamble, in exactly this shape:\n"
        '{"question": "...", "difficulty": "Easy|Medium|Hard", "hint": "...", '
        '"answer": "..."}\n'
        "The 'answer' should be a concise but complete model answer (3-8 sentences, or "
        "well-commented code for DSA questions). The 'hint' should nudge without giving "
        "the answer away. Never repeat or closely rephrase a question already listed as "
        "asked below."
    )

    user_prompt = (
        f"Generate {CATEGORY_PROMPTS[category]}\n\n"
        f"Questions already asked in this category (do NOT repeat or closely rephrase any "
        f"of these):\n{avoid_list}\n\n"
        "Respond with ONLY the JSON object."
    )

    resp = requests.post(
        API_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 800,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        },
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"API error {resp.status_code}: {resp.text}", file=sys.stderr)
    resp.raise_for_status()
    data = resp.json()

    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    raw = "".join(text_blocks).strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print(f"ERROR: could not parse model output as JSON:\n{raw}", file=sys.stderr)
        sys.exit(1)

    return parsed


def write_dated_file(category: str, q: dict) -> Path:
    today = date.today().isoformat()
    slug = category.lower().replace(" ", "-")
    path = QUESTIONS_DIR / f"{today}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {today} — {category} ({q.get('difficulty', 'Medium')})\n\n"
        f"## Question\n{q['question']}\n\n"
        f"## Hint\n{q.get('hint', '')}\n\n"
        f"## Answer\n{q.get('answer', '')}\n"
    )
    return path


def update_readme(history: dict, category: str, q: dict) -> None:
    total = len(history["questions"])
    counts = {c: sum(1 for x in history["questions"] if x["category"] == c) for c in CATEGORIES}
    today = date.today().isoformat()

    # Index of last 15 entries, newest first
    recent = history["questions"][-15:][::-1]
    index_lines = []
    for entry in recent:
        slug = entry["category"].lower().replace(" ", "-")
        fname = f"questions/{entry['date']}-{slug}.md"
        index_lines.append(f"- **{entry['date']}** [{entry['category']}]({fname}): {entry['question']}")

    content = f"""# 🧠 Daily Interview Question Bot

Autonomous daily interview-prep log, generated by the Claude API. One new question
every day, rotating across **DSA**, **AI/ML**, **CSE Core**, and **Behavioral**
topics — no repeats, no manual effort.

## 📅 Today's Question — {today} ({category})

**{q['question']}**

<details>
<summary>💡 Hint</summary>

{q.get('hint', '')}

</details>

<details>
<summary>✅ Answer</summary>

{q.get('answer', '')}

</details>

---

## 📊 Stats

- Total questions logged: **{total}**
- DSA: {counts['DSA']} · AI/ML: {counts['AIML']} · CSE Core: {counts['CSE Core']} · Behavioral: {counts['Behavioral']}

## 🗂️ Recent Questions

{chr(10).join(index_lines)}

Full history in [`data/questions.json`](data/questions.json). All past questions live in [`questions/`](questions/).

---
*Auto-generated daily via GitHub Actions + the Claude API. See `scripts/generate_question.py`.*
"""
    README_FILE.write_text(content)


def main() -> None:
    history = load_history()
    category = pick_category(history)
    q = call_claude(category, history)

    entry = {
        "date": date.today().isoformat(),
        "category": category,
        "question": q["question"],
        "difficulty": q.get("difficulty", "Medium"),
        "hint": q.get("hint", ""),
        "answer": q.get("answer", ""),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    history["questions"].append(entry)

    save_history(history)
    write_dated_file(category, q)
    update_readme(history, category, q)

    print(f"Generated {category} question for {entry['date']}: {q['question'][:80]}...")


if __name__ == "__main__":
    main()
