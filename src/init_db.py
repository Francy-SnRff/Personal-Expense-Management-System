import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "demo" / "expenses.db"
sql_path = BASE_DIR / "sql" / "schema.sql"

print("DB:", db_path)
print("SQL:", sql_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

with open(sql_path, "r", encoding="utf-8") as f:
    script = f.read()

print(script)

cur.executescript(script)

conn.commit()
conn.close()

print("Database creato.")