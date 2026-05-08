import sqlite3
from datetime import datetime
from pathlib import Path
from category_manager import list_categories


DB_PATH = Path(__file__).resolve().parent.parent / "demo" / "expenses.db"


# stessa funzione → stessa logica
def resolve_category_id(category_input, categories, cursor):

    if category_input.isdigit():

        valid_ids = [str(category[0]) for category in categories]

        if category_input not in valid_ids:
            return None

        return int(category_input)

    cursor.execute(
        """
        SELECT category_id
        FROM expense_category
        WHERE LOWER(category_name) = LOWER(?)
        """,
        (category_input,)
    )

    result = cursor.fetchone()

    if result is None:
        return None

    return result[0]


def manage_budget():

    while True:

        print()
        print("===================================")
        print(" GESTIONE BUDGET")
        print("===================================")
        print("1. Definisci Budget Mensile")
        print("2. Torna al Menu Principale")
        print("===================================")

        choice = input("Seleziona un'opzione: ").strip()

        match choice:

            case "1":
                set_budget()

            case "2":
                break

            case _:
                print("Scelta non valida")


def set_budget():

    print()
    print("===================================")
    print(" DEFINISCI BUDGET")
    print("===================================")



    budget_period = input("Periodo (YYYY-MM): ").strip()

    # controllo lunghezza
    if len(budget_period) != 7:
        print("Formato periodo non valido (YYYY-MM)")
        return

    try:
        datetime.strptime(budget_period, "%Y-%m")
    except ValueError:
        print("Formato periodo non valido (YYYY-MM)")
        return


    categories = list_categories()

    if not categories:
        return

    print("-----------------------------------")

    category_input = input("Categoria (ID o Descrizione): ").strip()
    budget_amount = input("Importo Budget: ").strip().replace(",", ".")

    # validazione importo
    try:
        amount = float(budget_amount)

        if amount <= 0:
            print("L'importo deve essere maggiore di zero")
            return

    except ValueError:
        print("Importo non valido")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # uso funzione unica
    category_id = resolve_category_id(category_input, categories, cur)

    if category_id is None:
        print("Categoria non valida")
        conn.close()
        return

    # controllo esistenza budget
    cur.execute(
        """
        SELECT budget_amount
        FROM monthly_budget
        WHERE budget_period = ?
        AND category_id = ?
        """,
        (budget_period, category_id)
    )

    existing_budget = cur.fetchone()

    # update
    if existing_budget is not None:

        old_amount = existing_budget[0]

        cur.execute(
            """
            UPDATE monthly_budget
            SET budget_amount = ?
            WHERE budget_period = ?
            AND category_id = ?
            """,
            (amount, budget_period, category_id)
        )

        conn.commit()
        conn.close()

        print(f"Budget aggiornato (precedente: {old_amount} → nuovo: {amount})")
        return

    # insert
    cur.execute(
        """
        INSERT INTO monthly_budget (
            budget_period,
            category_id,
            budget_amount
        )
        VALUES (?, ?, ?)
        """,
        (budget_period, category_id, amount)
    )

    conn.commit()
    conn.close()

    print("Budget inserito correttamente")