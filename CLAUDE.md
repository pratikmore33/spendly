# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**Spendly** is a Flask-based personal expense tracker built as a step-by-step teaching project. Students implement features incrementally across numbered steps; placeholder routes and stub files mark what is not yet built.

## Commands

```bash
# Activate the virtual environment (always required)
source venv/bin/activate

# Run the dev server (port 5001)
python app.py

# Run tests
pytest

# Run a single test file
pytest tests/test_db.py

# Initialize the database (once db.py is implemented)
python -c "from database.db import init_db; init_db()"

# Seed sample data
python -c "from database.db import init_db, seed_db; init_db(); seed_db()"
```

## Architecture

The app is a plain Flask app with no ORM — all database access goes through raw SQLite via `database/db.py`.

```
app.py              — Flask app, all routes
database/
  db.py             — get_db(), init_db(), seed_db()
templates/          — Jinja2 templates; all extend base.html
static/
  css/style.css     — all app styles (CSS variables + component blocks)
  css/landing.css   — landing-page-only styles
  js/main.js        — client-side JS (mostly empty; added per step)
spendly.db          — SQLite file created at runtime (not in git)
```

**Database schema** (implemented in Step 1):
- `users(id, name, email, password_hash, created_at)`
- `expenses(id, user_id, title, amount, category, date, created_at)` — `user_id` FK → `users.id` with `ON DELETE CASCADE`

**`get_db()`** returns a plain `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`. Routes call it directly, open a connection, and close it when done.

## Step map

The codebase is intentionally incomplete. Routes in `app.py` that return placeholder strings correspond to future steps:

| Placeholder string | Step |
|---|---|
| `"Logout — coming in Step 3"` | Step 3 — Auth |
| `"Profile page — coming in Step 4"` | Step 4 — Profile |
| `"Add expense — coming in Step 7"` | Step 7 — Create expense |
| `"Edit expense — coming in Step 8"` | Step 8 — Edit expense |
| `"Delete expense — coming in Step 9"` | Step 9 — Delete expense |

## Styling conventions

All CSS lives in `static/css/style.css` as themed CSS variables (`--ink`, `--paper`, `--accent` = dark green `#1a472a`, `--accent-2` = amber). New pages should use these variables and follow the existing component patterns (`.auth-card`, `.btn-primary`, `.btn-ghost`, etc.). Landing-specific styles go in `landing.css`.
