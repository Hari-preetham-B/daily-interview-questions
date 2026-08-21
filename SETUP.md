# One-time setup

## 1. Create the repo
Create a new GitHub repo (e.g. `daily-interview-questions`) and push this folder's
contents to it.

```bash
cd daily-interview-questions
git init
git add .
git commit -m "init: daily interview question bot"
git branch -M main
git remote add origin https://github.com/hari-preetham/daily-interview-questions.git
git push -u origin main
```

## 2. Create a Personal Access Token (PAT)
This is required so commits count on your contribution graph (the default
Actions token commits as `github-actions[bot]`, which does NOT count).

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Generate new token
   - Repository access: only this repo (`daily-interview-questions`)
   - Permissions: **Contents → Read and write**
3. Copy the token (starts with `github_pat_...`)

## 3. Get an Anthropic API key
1. Go to console.anthropic.com → API Keys → Create Key
2. Copy it (starts with `sk-ant-...`)
3. Note: this uses your API credits, not your Claude.ai subscription. One
   question a day is very cheap (a few thousand tokens/day with Haiku).

## 4. Add both as repo secrets
Repo → Settings → Secrets and variables → Actions → New repository secret

- `PAT_TOKEN` → paste the PAT from step 2
- `ANTHROPIC_API_KEY` → paste the API key from step 3

## 5. Confirm your git email matches your GitHub account
The workflow commits as:
```
user.name  = "Hari Preetham"
user.email = "haripreetham.1111@gmail.com"
```
This email MUST be a verified email on your GitHub account (Settings → Emails),
or the commit won't be linked to your profile and won't count on your graph.
If you use a different email on GitHub, edit the `git config user.email` line
in `.github/workflows/daily-question.yml` to match.

## 6. Test it manually
Repo → Actions tab → "Daily Interview Question" → Run workflow (top right).
Check that:
- The workflow completes green
- `README.md`, `data/questions.json`, and a new file in `questions/` were updated
- The commit shows your GitHub avatar (not the bot icon) — this confirms it'll count

## 7. Done
It now runs automatically every day at 8:00 AM IST (edit the cron line in the
workflow file to change the time). Even if you never open GitHub, this repo
will get 1 commit/day. If you want 2-4/day, see the note below.

---

## Want more than 1 contribution/day?
Add more schedule triggers to the same workflow, or duplicate the job for
other repos from your earlier automation (LeetCode tracker, profile README
refresh). A simple option: change the cron to run twice — e.g. once for a new
question, once for a "review yesterday's answer" reminder commit that
appends to a `reviewed.log` file. I can wire that up too if you want.
