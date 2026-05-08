import sqlite3
from datetime import date, datetime
from pathlib import Path
from category_manager import list_categories


DB_PATH = Path(__file__).resolve().parent.parent / "demo" / "expenses.db"


# funzione unica per gestire categoria (ID o nome)
def resolve_category_id(category_input, categories, cursor):

    # caso ID
    if category_input.isdigit():

        valid_ids = [str(category[0]) for category in categories]

        if category_input not in valid_ids:
            return None

        return int(category_input)

    # caso nome
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


def add_expense():

    print()
    print("===================================")
    print(" INSERISCI SPESA")
    print("===================================")



    print("-----------------------------------")
    transaction_date = input("Data spesa (YYYY-MM-DD) [Invio = oggi]: ").strip()

    transaction_amount = input("Importo: ").strip().replace(",", ".")

    # mostro categorie
    categories = list_categories()

    if not categories:
        return

    category_input = input("Inserisci ID oppure nome categoria (es: 1 oppure Alimentari) ): ").strip()
    expense_description = input("Descrizione (facoltativa): ").strip().title()

    # se vuota → uso oggi
    if transaction_date == "":
        transaction_date = date.today().isoformat()
        print(f"Data impostata automaticamente a oggi: {transaction_date}")
    else:
    # controllo formato
        try:
            datetime.strptime(transaction_date, "%Y-%m-%d")
        except ValueError:
            print("Formato data non valido (YYYY-MM-DD)")
            return

    # validazione importo
    try:
        amount = float(transaction_amount)

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

    # inserimento
    cur.execute(
        """
        INSERT INTO expense_transaction (
            transaction_date,
            transaction_amount,
            category_id,
            expense_description
        )
        VALUES (?, ?, ?, ?)
        """,
        (transaction_date, amount, category_id, expense_description)
    )

    conn.commit()
    conn.close()

    print("Spesa registrata correttamente")


