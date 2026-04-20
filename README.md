# Daily Mileage Calculation App

A polished, portfolio-ready **Flask** web application for estimating **fuel use**, **trip cost**, and **cost per mile** from miles driven, vehicle MPG, and price per gallon. Entries are stored in **SQLite** with a sortable history table, summary cards, and delete actions.

**GitHub:** [github.com/Rasy84/daily-mileage-app](https://github.com/Rasy84/daily-mileage-app)

## Description

You enter a trip date, distance, your car’s MPG, and the gas price. The app computes:

- **Gallons used** = miles ÷ MPG  
- **Total fuel cost** = gallons × price per gallon  
- **Cost per mile** = total cost ÷ miles  

Each saved trip appears in a **history** table. **Summary** cards show total miles driven, total gas spend, a weighted average cost per mile, and how many entries you have saved.

## Features

- Dark, modern **card-based** UI with responsive layout  
- **Validation** with clear error messages  
- **Save** each calculation to SQLite  
- **History** table (newest first) with **delete** per row  
- **Summary** metrics across all entries  
- **`/health`** JSON endpoint for monitoring or demos  
- **Docker** setup with named project and container for Docker Desktop  

## Screenshots

_Add screenshots here after running the app (dashboard with calculator, summary, and history)._

## Tech stack

- Python 3.12+  
- Flask 3  
- SQLite (file under `instance/`)  
- Jinja2 templates  
- Vanilla CSS (and minimal JS)  
- Gunicorn in Docker  
- Docker Compose  

## Local setup

1. **Python 3.12+** recommended.  
2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python app.py
   ```

5. Open **http://127.0.0.1:5000** (or **http://localhost:5000**).

The database file is created automatically at `instance/mileage.db` on first run.

## Docker setup

From the project root (where `docker-compose.yml` lives):

```bash
docker compose up --build -d
```

Then open:

- App: **http://localhost:5050**  
- Health: **http://localhost:5050/health**  

Stop and remove containers:

```bash
docker compose down
```

## Docker Desktop visibility

This Compose file sets **`name: daily-mileage-app`** so the **project** appears as **daily-mileage-app** in Docker Desktop. The service builds image **`daily-mileage-app:latest`** and runs a container named **`daily-mileage-app`** with host port **5050** mapped to container port **5000** (`5050:5000`). You should see the project, container, and port mapping in the **Containers** view.

SQLite data is persisted in the named volume **`mileage_instance`** (mounted at `/app/instance` in the container).

## Example usage

1. Set **Date** to today.  
2. Enter **Miles driven** (e.g. `32.4`).  
3. Enter **Vehicle MPG** (e.g. `29`).  
4. Enter **Gas price** per gallon (e.g. `3.49`).  
5. Click **Calculate & save**.  
6. Confirm the new row in **History** and updated **Summary** values.  
7. Use **Delete** on a row to remove one entry.  

## Folder structure

```
Daily Mileage calculation App/
  app.py                 # Flask app, routes, DB helpers
  requirements.txt
  Dockerfile
  docker-compose.yml
  .dockerignore
  .gitignore
  README.md
  CURSOR_SUMMARY.md
  instance/              # SQLite file (created at runtime; .gitkeep tracked)
  database/
    schema.sql           # Table definition (reference)
  templates/
    base.html
    index.html
  static/
    style.css
    script.js
```

## GitHub repository

- **Owner:** Rasy84  
- **Repo:** [daily-mileage-app](https://github.com/Rasy84/daily-mileage-app)  

Push updates from this folder after configuring `git remote` and authentication (HTTPS or SSH).

## Future improvements

- Export history to CSV  
- Optional vehicle profiles (name + default MPG)  
- Charts for spend and miles over time  
- Stronger production settings (secret management, HTTPS, logging)  
