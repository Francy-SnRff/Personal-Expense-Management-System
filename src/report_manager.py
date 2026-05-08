import sqlite3
from pathlib import Path


# percorso database
DB_PATH = Path(__file__).resolve().parent.parent / "demo" / "expenses.db"

print("DB:", DB_PATH.resolve())

# formatto numero in stile italiano
def format_currency(value):
    return f"{value:.2f} €".replace(".", ",")



# stampa intestazione
def print_header(headers, widths):

    parts = []

    # creo ogni colonna
    for i in range(len(headers)):
        parts.append(f"{headers[i]:<{widths[i]}}")

    # unisco con spazio fisso tra colonne
    print("  ".join(parts))

    # linea sotto
    print("-" * (sum(widths) + (len(widths) - 1) * 2))


# stampa riga dati
def print_row(values, widths, aligns):

    parts = []

    for i in range(len(values)):
        value = values[i]
        width = widths[i]
        align = aligns[i]

        # allineo testo / numeri
        if align == "right":
            formatted = f"{value:>{width}}"
        else:
            formatted = f"{value:<{width}}"

        parts.append(formatted)

    # spazio tra colonne garantito
    print("  ".join(parts))


def manage_reports():

    while True:

        print()
        print("===================================")
        print(" REPORT")
        print("===================================")
        print("1. Totale spese per categoria")
        print("2. Budget vs Speso")
        print("3. Elenco movimenti")
        print("4. Torna al Menu Principale")
        print("===================================")

        choice = input("Seleziona un'opzione: ").strip()

        match choice:

            case "1":
                report_total_by_category()

            case "2":
                report_budget_vs_spent()

            case "3":
                report_all_expenses()

            case "4":
                break

            case _:
                print("Scelta non valida")


def report_total_by_category():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # somma spese per categoria
    cur.execute("""
        SELECT c.category_name, SUM(e.transaction_amount)
        FROM expense_transaction e
        JOIN expense_category c ON e.category_id = c.category_id
        GROUP BY c.category_name
    """)

    results = cur.fetchall()
    conn.close()

    print()
    print("Totale spese per categoria")
    print("-----------------------------------")

    widths = [20, 15]
    aligns = ["left", "right"]

    print_header(["Categoria", "Totale"], widths)

    total_sum = 0

    for row in results:
        categoria = row[0]
        totale = row[1] if row[1] else 0

        total_sum += totale

        print_row(
            [categoria, format_currency(totale)],
            widths,
            aligns
        )

    print("-" * (sum(widths) + (len(widths) - 1) * 2))

    print_row(
        ["TOTALE", format_currency(total_sum)],
        widths,
        aligns
    )


def report_budget_vs_spent():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # query corretta con mese da budget
    cur.execute("""
        SELECT 
            b.budget_period AS mese,
            c.category_name,
            b.budget_amount,
            IFNULL(SUM(e.transaction_amount), 0) AS speso
        FROM monthly_budget b
        JOIN expense_category c 
            ON b.category_id = c.category_id
        LEFT JOIN expense_transaction e 
            ON e.category_id = b.category_id
            AND strftime('%Y-%m', e.transaction_date) = b.budget_period
        GROUP BY b.budget_period, c.category_name, b.budget_amount
        ORDER BY b.budget_period DESC
    """)

    results = cur.fetchall()
    conn.close()

    print()
    print("Budget vs Speso (Mensile)")
    print("-----------------------------------")

    widths = [15, 20, 15, 15, 20]
    aligns = ["left", "left", "right", "right", "left"]

    print_header(["Mese", "Categoria", "Budget", "Speso", "Stato"], widths)

    total_budget = 0
    total_speso = 0

    
    for row in results:
        mese = row[0]
        categoria = row[1]
        budget = row[2]
        speso = row[3]

        total_budget += budget
        total_speso += speso

        # niente conversioni
        mese_label = mese

        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "ENTRO BUDGET"

        print_row(
            [mese_label, categoria, format_currency(budget), format_currency(speso), stato],
            widths,
            aligns
        )

    print("-" * (sum(widths) + (len(widths) - 1) * 2))

    print_row(
        ["TOTALE", "", format_currency(total_budget), format_currency(total_speso), ""],
        widths,
        aligns
    )


def report_all_expenses():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # elenco movimenti
    cur.execute("""
        SELECT 
            e.transaction_date,
            c.category_name,
            e.transaction_amount,
            e.expense_description
        FROM expense_transaction e
        JOIN expense_category c ON e.category_id = c.category_id
        ORDER BY e.transaction_date DESC
    """)

    results = cur.fetchall()
    conn.close()

    print()
    print("Elenco movimenti")
    print("---------------------------------------------------------------------")

    widths = [12, 25, 10, 25]
    aligns = ["left", "left", "right", "left"]

    print_header(
        ["Data", "Categoria", "Importo", "Descrizione"],
        widths
    )

    total_speso = 0

    for row in results:
        data = row[0]
        categoria = row[1]
        importo = row[2]

        descrizione = row[3] if row[3] else ""

        total_speso += importo

        print_row(
            [data, categoria, format_currency(importo), descrizione],
            widths,
            aligns
        )

    print("-" * (sum(widths) + (len(widths) - 1) * 2))

    print_row(
        ["TOTALE", "", format_currency(total_speso), ""],
        widths,
        aligns
    )