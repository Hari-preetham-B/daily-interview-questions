#!/usr/bin/env python3
"""
Daily Interview Question Generator
-----------------------------------
Calls the Groq API (free tier, Llama models) to generate ONE new interview
question per run, rotating across categories (AIML, CSE Core, DSA,
Behavioral), avoiding repeats of anything already asked, and updates:
  - data/questions.json   (full history, structured)
  - questions/YYYY-MM-DD-<slot>-<category>.md   (dated question file with answer/hints)
  - README.md             (today's AM/PM questions + stats + index)

Runs twice daily via GitHub Actions (AM and PM slots, based on UTC hour of the
run). Each slot gets a different category so the two runs on the same day
never collide. If a slot's question already exists for today (e.g. a manual
re-run), the script skips calling the API entirely to avoid wasting quota.

Requires env var GROQ_API_KEY. Get a free key at:
https://console.groq.com/keys
"""

import json
import os
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "questions.json"
QUESTIONS_DIR = ROOT / "questions"
README_FILE = ROOT / "README.md"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
# Try these in order; if one is down/deprecated, fall through to the next.
MODELS_TO_TRY = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

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


def determine_slot() -> str:
    hour = datetime.now(timezone.utc).hour
    return "AM" if hour < 12 else "PM"


def pick_category(slot: str) -> str:
    day_index = date.today().timetuple().tm_yday
    offset = 0 if slot == "AM" else 2
    return CATEGORIES[(day_index + offset) % len(CATEGORIES)]


def already_generated(history: dict, today: str, slot: str) -> bool:
    return any(q["date"] == today and q.get("slot") == slot for q in history["questions"])


def question_filename(entry: dict) -> str:
    slug = entry["category"].lower().replace(" ", "-")
    slot = entry.get("slot")
    if slot:
        return f"questions/{entry['date']}-{slot.lower()}-{slug}.md"
    return f"questions/{entry['date']}-{slug}.md"


def recent_questions_text(history: dict, category: str, limit: int = 25) -> str:
    same_cat = [q["question"] for q in history["questions"] if q["category"] == category]
    recent = same_cat[-limit:]
    if not recent:
        return "(none yet)"
    return "\n".join(f"- {q}" for q in recent)


def call_groq(category: str, history: dict) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY not set", file=sys.stderr)
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

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = None
    for model in MODELS_TO_TRY:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.9,
            "max_tokens": 1024,
            "response_format": {"type": "json_object"},
        }

        attempts = 3
        for attempt in range(1, attempts + 1):
            resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                print(f"Used model: {model}")
                break
            if resp.status_code in (429, 503) and attempt < attempts:
                wait = attempt * 10
                print(
                    f"{model} returned {resp.status_code} (attempt {attempt}/{attempts}), "
                    f"retrying in {wait}s...",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            print(f"{model} failed with {resp.status_code}: {resp.text}", file=sys.stderr)
            break
        if resp is not None and resp.status_code == 200:
            break

    if resp is None or resp.status_code != 200:
        print("ERROR: all models failed.", file=sys.stderr)
        resp.raise_for_status()

    data = resp.json()

    try:
        raw = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        print(f"ERROR: unexpected Groq response shape:\n{json.dumps(data, indent=2)}", file=sys.stderr)
        sys.exit(1)

    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        print(f"ERROR: could not parse model output as JSON:\n{raw}", file=sys.stderr)
        sys.exit(1)

    return parsed


def write_dated_file(category: str, q: dict, slot: str) -> Path:
    today = date.today().isoformat()
    slug = category.lower().replace(" ", "-")
    path = QUESTIONS_DIR / f"{today}-{slot.lower()}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# {today} {slot} — {category} ({q.get('difficulty', 'Medium')})\n\n"
        f"## Question\n{q['question']}\n\n"
        f"## Hint\n{q.get('hint', '')}\n\n"
        f"## Answer\n{q.get('answer', '')}\n"
    )
    return path


def render_question_block(entry: dict, label: str) -> str:
    return f"""### {label} — {entry['category']}

**{entry['question']}**

<details>
<summary>💡 Hint</summary>

{entry.get('hint', '')}

</details>

<details>
<summary>✅ Answer</summary>

{entry.get('answer', '')}

</details>
"""


def update_readme(history: dict) -> None:
    total = len(history["questions"])
    counts = {c: sum(1 for x in history["questions"] if x["category"] == c) for c in CATEGORIES}
    today = date.today().isoformat()

    todays = [q for q in history["questions"] if q["date"] == today]
    slot_order = {"AM": 0, "PM": 1}
    todays.sort(key=lambda e: slot_order.get(e.get("slot"), 0))

    if todays:
        today_section = "\n---\n\n".join(
            render_question_block(e, f"🌙 Evening ({today})" if e.get("slot") == "PM" else f"🌅 Morning ({today})")
            for e in todays
        )
    else:
        today_section = "_No question generated yet today._"

    recent = history["questions"][-15:][::-1]
    index_lines = []
    for entry in recent:
        fname = question_filename(entry)
        slot_tag = f" [{entry['slot']}]" if entry.get("slot") else ""
        index_lines.append(
            f"- **{entry['date']}{slot_tag}** [{entry['category']}]({fname}): {entry['question']}"
        )

    content = f"""# 🧠 Daily Interview Question Bot

Autonomous interview-prep log, generated by the Groq API (Llama models). Two
new questions every day (morning and evening), rotating across **DSA**,
**AI/ML**, **CSE Core**, and **Behavioral** topics — no repeats, no manual effort.

## 📅 Today's Questions — {today}

{today_section}

---

## 📊 Stats

- Total questions logged: **{total}**
- DSA: {counts['DSA']} · AI/ML: {counts['AIML']} · CSE Core: {counts['CSE Core']} · Behavioral: {counts['Behavioral']}

## 🗂️ Recent Questions

{chr(10).join(index_lines)}

Full history in [`data/questions.json`](data/questions.json). All past questions live in [`questions/`](questions/).

---
*Auto-generated twice daily via GitHub Actions + the Groq API. See `scripts/generate_question.py`.*
"""
    README_FILE.write_text(content)


def main() -> None:
    today = date.today().isoformat()
    slot = determine_slot()
    history = load_history()

    if already_generated(history, today, slot):
        print(
            f"A {slot} question for {today} already exists — skipping to avoid "
            "wasting API quota on a duplicate run."
        )
        return

    category = pick_category(slot)
    q = call_groq(category, history)

    entry = {
        "date": today,
        "slot": slot,
        "category": category,
        "question": q["question"],
        "difficulty": q.get("difficulty", "Medium"),
        "hint": q.get("hint", ""),
        "answer": q.get("answer", ""),
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    history["questions"].append(entry)

    save_history(history)
    write_dated_file(category, q, slot)
    update_readme(history)

    print(f"Generated {slot} {category} question for {today}: {q['question'][:80]}...")


if __name__ == "__main__":
    main()
