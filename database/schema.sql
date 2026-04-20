-- SQLite schema for Daily Mileage Calculation App (reference; app also auto-creates tables)
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
);
