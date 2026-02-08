# Local 10FastFingers-style Typing Test (Flask)

A simple Flask web app inspired by 10FastFingers.

- Login with **username only** (no password)
- Choose test duration (1/2/5/10 minutes)
- Type a stream of random words (from a fixed wordlist)
- Live feedback: correct words **green**, wrong words **red**
- Shows **current word + next 20 words**
- End-of-test stats: correct, wrong, total, WPM, accuracy
- Saves results to a local **SQLite** database
- History page with a **progress graph** (WPM + Accuracy)

## Project Structure

```
local_10_fast_fingers/
├─ app.py
├─ requirements.txt
└─ templates/
   ├─ login.html
   ├─ dashboard.html
   ├─ test.html
   └─ history.html
```

When you run the app for the first time, Flask/SQLAlchemy will create a local SQLite database at:

- `instance/typing_test.db`

## Requirements

- Python 3.9+ recommended
- Linux / WSL / macOS / Windows (WSL works well)

Python dependencies are listed in `requirements.txt`.

## Setup (venv)

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open:

- http://localhost:5000

## How to Use

1. Open the app and enter a username.
2. Choose a duration (1, 2, 5, or 10 minutes).
3. Start typing.
   - Press **Space** after each word to submit it.
   - The current word is highlighted.
   - Correct words turn green; wrong words turn red.
4. When time ends, results are shown and saved automatically.
5. Visit **History** to see your progress chart + all test results.

## Stats Explained

- **Correct words**: number of words typed exactly matching the expected word.
- **Wrong words**: submitted words that do not match.
- **Total words**: correct + wrong.
- **WPM (Words Per Minute)**:

  $$\text{WPM} = \frac{\text{correct\_words}}{\text{duration\_minutes}}$$

- **Accuracy (%)**:

  $$\text{Accuracy} = \frac{\text{correct\_words}}{\text{total\_words}} \times 100$$

## Database (SQLite)

This app uses **SQLite** via **Flask-SQLAlchemy**.

### Tables

- `user`
  - `id` (PK)
  - `username` (unique)
  - `created_at`

- `test_result`
  - `id` (PK)
  - `user_id` (FK → `user.id`)
  - `duration` (seconds)
  - `correct_words`
  - `wrong_words`
  - `total_words`
  - `wpm`
  - `accuracy`
  - `created_at`

### Inspect the DB (optional)

If you have `sqlite3` installed:

```bash
sqlite3 instance/typing_test.db
```

Inside the SQLite prompt:

```sql
.tables
.schema user
.schema test_result
SELECT * FROM user;
SELECT * FROM test_result ORDER BY created_at DESC LIMIT 10;
.quit
```

## Git / Version Control

Do **not** commit the virtual environment or local database.

Create a `.gitignore` like this:

```gitignore
.venv/
__pycache__/
*.pyc
instance/
*.db
```

Commit these instead:

- `app.py`
- `requirements.txt`
- `templates/`
- `README.md`
- `.gitignore`

## Notes / Limitations

- Username-only login is for local practice only (no passwords, no security hardening).
- The word stream is randomly generated per test.
- The test currently generates 200 words per session; you can increase this in `/get_words` if needed.

## Troubleshooting

### Port already in use

If you get an “Address already in use” error, run on another port:

```bash
FLASK_RUN_PORT=5001 python app.py
```

(or edit `app.run(...)` in `app.py`).

### WSL / Browser access

Usually you can open from Windows using:

- http://localhost:5000

If not, copy the exact URL shown in the terminal output.
