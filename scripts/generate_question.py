#!/usr/bin/env python3
"""
Daily Interview Question Generator
-----------------------------------
Calls the Google Gemini API (free tier) to generate ONE new interview question
per run, rotating across categories (AIML, CSE Core, DSA, Behavioral), avoiding
repeats of anything already asked, and updates:
  - data/questions.json   (full history, structured)
  - questions/YYYY-MM-DD-<slot>-<category>.md   (dated question file with answer/hints)
  - README.md             (today's AM/PM questions + stats + index)

Runs twice daily via GitHub Actions (AM and PM slots, based on UTC hour of the
run). Each slot gets a different category so the two runs on the same day never
collide. If a slot's question already exists for today (e.g. a manual re-run),
the script skips calling the API entirely to avoid wasting quota.

Requires env var GEMINI_API_KEY. Get a free key at:
https://aistudio.google.com/app/apikey
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

# Gemini free-tier model. Google deprecates/renames Flash models every few months
# (this script was bumped from gemini-2.0-flash after Google shut it down in June 2026).
# If this model 404s in the future, check https://ai.google.dev/gemini-api/docs/models
# for the current stable Flash model name and update MODEL below.
MODEL = "gemini-3.6-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

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
    """AM if this run landed in the UTC morning window (covers 2:30 UTC / 8am IST),
    PM if it landed in the UTC afternoon/evening window (covers 14:30 UTC / 8pm IST).
    Using the UTC hour rather than a fixed label keeps this correct even if the
    cron times in the workflow are ever tweaked slightly."""
    hour = datetime.utcnow().hour
    return "AM" if hour < 12 else "PM"


def pick_category(slot: str) -> str:
    """Pick a category for this slot. Offsetting the PM slot by 2 (out of 4
    categories) guarantees AM and PM always land on different categories on
    the same day, while still rotating predictably day to day."""
    day_index = date.today().timetuple().tm_yday
    offset = 0 if slot == "AM" else 2
    return CATEGORIES[(day_index + offset) % len(CATEGORIES)]


def already_generated(history: dict, today: str, slot: str) -> bool:
    return any(q["date"] == today and q.get("slot") == slot for q in history["questions"])


def question_filename(entry: dict) -> str:
    """Build the questions/ filename for a history entry. Entries generated
    before slots existed won't have a 'slot' key, so we fall back to the old
    naming for those so existing links in README history keep working."""
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


def call_gemini(category: str, history: dict) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
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
        params={"key": api_key},
        headers={"content-type": "application/json"},
        json={
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 2048,
                "responseMimeType": "application/json",
            },
        },
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"API error {resp.status_code}: {resp.text}", file=sys.stderr)
    resp.raise_for_status()
    data = resp.json()

    try:
        candidates = data["candidates"]
        finish_reason = candidates[0].get("finishReason")
        parts = candidates[0]["content"]["parts"]
        raw = "".join(p.get("text", "") for p in parts).strip()
    except (KeyError, IndexError):
        print(f"ERROR: unexpected Gemini response shape:\n{json.dumps(data, indent=2)}", file=sys.stderr)
        sys.exit(1)

    if finish_reason == "MAX_TOKENS":
        print(
            "ERROR: Gemini response was cut off (hit maxOutputTokens). "
            "Increase generationConfig.maxOutputTokens in the script.",
            file=sys.stderr,
        )
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

    # Today's entries, AM first then PM
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

    # Index of last 15 entries, newest first
    recent = history["questions"][-15:][::-1]
    index_lines = []
    for entry in recent:
        fname = question_filename(entry)
        slot_tag = f" [{entry['slot']}]" if entry.get("slot") else ""
        index_lines.append(
            f"- **{entry['date']}{slot_tag}** [{entry['category']}]({fname}): {entry['question']}"
        )

    content = f"""# 🧠 Daily Interview Question Bot

Autonomous interview-prep log, generated by the Gemini API. Two new questions
every day (morning and evening), rotating across **DSA**, **AI/ML**, **CSE Core**,
and **Behavioral** topics — no repeats, no manual effort.

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
*Auto-generated twice daily via GitHub Actions + the Gemini API. See `scripts/generate_question.py`.*
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
    q = call_gemini(category, history)

    entry = {
        "date": today,
        "slot": slot,
        "category": category,
        "question": q["question"],
        "difficulty": q.get("difficulty", "Medium"),
        "hint": q.get("hint", ""),
        "answer": q.get("answer", ""),
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    history["questions"].append(entry)

    save_history(history)
    write_dated_file(category, q, slot)
    update_readme(history)

    print(f"Generated {slot} {category} question for {today}: {q['question'][:80]}...")


if __name__ == "__main__":
    main()
