"""Daily Mileage Calculation App — Flask + SQLite."""

from __future__ import annotations

import os
import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "mileage.db"


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-change-me-in-production"
    )

    @app.get("/")
    def index():
        entries = fetch_entries()
        summary = compute_summary(entries)
        return render_template(
            "index.html",
            entries=entries,
            summary=summary,
            today_iso=date.today().isoformat(),
        )

    @app.post("/calculate")
    def calculate():
        raw_date = (request.form.get("entry_date") or "").strip()
        miles_s = (request.form.get("miles_driven") or "").strip()
        mpg_s = (request.form.get("mpg") or "").strip()
        price_s = (request.form.get("gas_price") or "").strip()

        errors: list[str] = []
        entry_date: date | None = None
        try:
            entry_date = date.fromisoformat(raw_date)
        except ValueError:
            errors.append("Please enter a valid date.")

        miles = _parse_positive_float(miles_s, "Miles driven", errors)
        mpg = _parse_positive_float(mpg_s, "Vehicle MPG", errors)
        gas_price = _parse_positive_float(price_s, "Gas price per gallon", errors)

        if errors:
            for e in errors:
                flash(e, "error")
            return redirect(url_for("index"))

        assert entry_date is not None
        assert miles is not None and mpg is not None and gas_price is not None

        gallons_used = miles / mpg
        total_cost = gallons_used * gas_price
        cost_per_mile = total_cost / miles

        conn = get_db()
        conn.execute(
            """
            INSERT INTO mileage_entries (
                entry_date, miles_driven, mpg, gas_price,
                gallons_used, total_cost, cost_per_mile
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry_date.isoformat(),
                miles,
                mpg,
                gas_price,
                gallons_used,
                total_cost,
                cost_per_mile,
            ),
        )
        conn.commit()
        conn.close()

        flash("Trip saved. Your calculation is in the history below.", "success")
        return redirect(url_for("index"))

    @app.post("/delete/<int:entry_id>")
    def delete_entry(entry_id: int):
        conn = get_db()
        cur = conn.execute("DELETE FROM mileage_entries WHERE id = ?", (entry_id,))
        conn.commit()
        deleted = cur.rowcount
        conn.close()
        if deleted:
            flash("Entry removed from history.", "success")
        else:
            flash("That entry was not found.", "error")
        return redirect(url_for("index"))

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "app": "daily-mileage-app",
        }

    with app.app_context():
        init_db()

    return app


def _parse_positive_float(
    raw: str, label: str, errors: list[str]
) -> float | None:
    try:
        value = float(raw.replace(",", ""))
    except ValueError:
        errors.append(f"{label} must be a number.")
        return None
    if value <= 0:
        errors.append(f"{label} must be greater than zero.")
        return None
    return value


def get_db() -> sqlite3.Connection:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS mileage_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            miles_driven REAL NOT NULL,
            mpg REAL NOT NULL,
            gas_price REAL NOT NULL,
            gallons_used REAL NOT NULL,
            total_cost REAL NOT NULL,
            cost_per_mile REAL NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


def fetch_entries() -> list[sqlite3.Row]:
    conn = get_db()
    rows = conn.execute(
        """
        SELECT id, entry_date, miles_driven, mpg, gas_price,
               gallons_used, total_cost, cost_per_mile, created_at
        FROM mileage_entries
        ORDER BY entry_date DESC, id DESC
        """
    ).fetchall()
    conn.close()
    return rows


def compute_summary(rows: list[sqlite3.Row]) -> dict:
    if not rows:
        return {
            "total_miles": 0.0,
            "total_spend": 0.0,
            "avg_cost_per_mile": 0.0,
            "entry_count": 0,
        }
    total_miles = sum(float(r["miles_driven"]) for r in rows)
    total_spend = sum(float(r["total_cost"]) for r in rows)
    weighted_cpm = total_spend / total_miles if total_miles > 0 else 0.0
    return {
        "total_miles": total_miles,
        "total_spend": total_spend,
        "avg_cost_per_mile": weighted_cpm,
        "entry_count": len(rows),
    }


app = create_app()

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
