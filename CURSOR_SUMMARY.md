# Cursor session summary — Daily Mileage Calculation App

## Old files removed

- **`C:\University Course\DSA 502\Week 12\Minimal App\daily-mileage-app\`** — entire folder removed (previous minimal Flask project and its `.git` history).
- **`C:\University Course\DSA 502\Week 12\Minimal App\minimal-docker-app\`** — **not removed**: Windows reported *“The process cannot access the file … because it is being used by another process.”* Close Docker Desktop, VS Code, or Explorer windows using that path, then delete the folder manually if it is still present.

## Old Docker containers / images removed

Stopped and removed containers:

- `flask_notes_app-web-1`
- `flask_notes_app-db-1`

Removed images (no longer referenced by running containers):

- `flask_notes_app-web:latest`
- `daily-mileage-app:latest` (previous build)
- `minimal-docker-app:latest`

**Not removed:** generic `postgres:16-alpine` (may still be useful for other projects).

## New files created

Project root: **`C:\University Course\DSA 502\Week 12\Daily Mileage calculation App`**

| Path | Role |
|------|------|
| `app.py` | Flask app: `/`, `POST /calculate`, `POST /delete/<id>`, `GET /health`, SQLite init |
| `requirements.txt` | Flask + Gunicorn |
| `Dockerfile` | Python 3.12-slim, Gunicorn on port 5000 |
| `docker-compose.yml` | Compose project `daily-mileage-app`, service `web`, container `daily-mileage-app`, `5050:5000`, volume for `instance/` |
| `.dockerignore` / `.gitignore` | Build and Git hygiene |
| `README.md` | Setup, Docker, usage, structure |
| `database/schema.sql` | Reference schema (tables also created in code) |
| `instance/.gitkeep` | Keeps `instance/` in Git; DB file is gitignored |
| `templates/base.html`, `templates/index.html` | Dark glass UI, calculator, summary, history |
| `static/style.css`, `static/script.js` | Styling and small UX helper |

## App features

- Trip form: date, miles, MPG, $/gal with validation (`> 0` for numeric fields).
- Calculations: gallons, total cost, cost per mile; values rounded for display (2 decimals).
- SQLite persistence with automatic DB creation.
- History table + per-row delete.
- Summary: total miles, total spend, weighted average $/mile, entry count.
- `GET /health` → `{"status":"ok","app":"daily-mileage-app"}`.

## Local run commands

```powershell
cd "C:\University Course\DSA 502\Week 12\Daily Mileage calculation App"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** — health: **http://127.0.0.1:5000/health**

## Docker commands

```powershell
cd "C:\University Course\DSA 502\Week 12\Daily Mileage calculation App"
docker compose up --build -d
```

- App: **http://localhost:5050**
- Health: **http://localhost:5050/health**

Stop:

```powershell
docker compose down
```

## Docker Desktop naming

- **Compose project name:** `daily-mileage-app` (from top-level `name:` in `docker-compose.yml`).
- **Container name:** `daily-mileage-app`
- **Ports:** `0.0.0.0:5050->5000/tcp` (host **5050** → container **5000**)
- **Image:** `daily-mileage-app:latest`

## Git commands used

```powershell
cd "C:\University Course\DSA 502\Week 12\Daily Mileage calculation App"
git init
git add -A
git commit -m "Initial Daily Mileage Calculation App: Flask, SQLite, Docker"
git branch -M main
git remote add origin https://github.com/Rasy84/daily-mileage-app.git
git fetch origin
git push -u origin main --force
git add CURSOR_SUMMARY.md
git commit -m "Add CURSOR_SUMMARY.md for session documentation"
git push origin main
```

The remote **main** branch was **force-updated** so the old minimal app history on GitHub was replaced by this repository state. The GitHub repository was **not** deleted and recreated; overwriting via `git push --force` was sufficient.

## GitHub push result

- **Succeeded:** `main` pushed to `https://github.com/Rasy84/daily-mileage-app.git` (forced update replacing prior `main`, plus follow-up commits including `CURSOR_SUMMARY.md`).

## Issues / blockers

1. **`Minimal App\minimal-docker-app`** could not be deleted while locked; remove manually after closing the locking program.

## Verification notes (session)

- Flask test client: `GET /health` returned JSON with `application/json`.
- Docker: `Invoke-WebRequest http://localhost:5050/health` returned `{"app":"daily-mileage-app","status":"ok"}`; `GET /` returned HTTP 200.
