import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "demo" / "expenses.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
INSERT INTO expense_category (category_name)
VALUES
('Alimentari'),
('Trasporti'),
('Bollette'),
('Ristoranti e Pizzerie'),
('Salute e Farmacia'),
('Tempo Libero'),
('Casa e Manutenzione');
""")

conn.commit()
conn.close()

print("Categorie dimostrative inserite correttamente.")