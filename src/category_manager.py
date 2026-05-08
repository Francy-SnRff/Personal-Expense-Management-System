import sqlite3
from pathlib import Path


# Creo il percorso dinamico del database
# __file__ indica il file corrent
# .parent.parent risale di due cartelle fino alla root del progetto.


DB_PATH = Path(__file__).resolve().parent.parent / "demo" / "expenses.db"


def manage_categories():

    # Ciclo continuo: il menu resta aperto finché l'utente non sceglie di uscire
    while True:

        print()
        print("===================================")
        print(" GESTIONE CATEGORIE")
        print("===================================")
        print("1. Inserisci Nuova Categoria")
        print("2. Visualizza Categorie")
        print("3. Torna al Menu Principale")
        print("===================================")

        # Leggo la scelta utente da tastiera  # strip() rimuove eventuali spazi digitati per errore.
        choice = input("Seleziona un'opzione: ").strip()

        # match/case è uno switch 
        match choice:

            case "1":
                add_category()

            case "2":
                list_categories()

            case "3":
                # Esco dal ciclo e torno al menu principale.
                break

            case _:
                # Caso default: input non valido.
                print("Scelta non valida.")


def add_category():

    # Chiedo il nome categoria.
    # strip() elimina spazi inutili.
    # title() mette iniziale maiuscola ad ogni parola.
    # Esempio: "alimentari" -> "Alimentari"
    category_name = input("Inserisci nome categoria: ").strip().title()

    # Controllo se utente ha lasciato campo vuoto
    if category_name == "":
        print("Il nome categoria non può essere vuoto.")
        return

    # Impedisco nomi composti solo da numeri
    if category_name.isdigit():
        print("Il nome categoria non può essere composto da soli numeri.")
        return

    # Apro connessione al database SQLite
    conn = sqlite3.connect(DB_PATH)

    # Creo il cursore per eseguire query 
    cur = conn.cursor()

    # Verifico se la categoria esiste già.
    # LOWER rende il confronto case insensitive:
    # Alimentari = alimentari = ALIMENTARI


    cur.execute(
        """
        SELECT category_id
        FROM expense_category
        WHERE LOWER(category_name) = LOWER(?)
        """,
        (category_name,)
    )

    # fetchone() prende una sola riga del risultato.
    # Se trova record restituisce i dati, altrimenti restituisce None.

    existing_category = cur.fetchone()

    # Se categoria già presente blocco inserimento
    if existing_category is not None:
        print("La categoria esiste già.")
        conn.close()
        return

    # Inserisco nuova categoria.
    

    cur.execute(
        """
        INSERT INTO expense_category (category_name)
        VALUES (?)
        """,
        (category_name,)
    )

    # Salvo 
    conn.commit()

    # Chiudo connessione
    conn.close()

    print("Categoria inserita correttamente.")


def list_categories():

    # Apro connessione database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Recupero tutte le categorie attive, ordina per ID crescente
    cur.execute(
        """
        SELECT category_id, category_name
        FROM expense_category
        WHERE category_status = 'ACTIVE'
        ORDER BY category_id
        """
    )

    # fetchall() prende tutti i risultati e li salva in una lista di tuple,es:
    #
    # [
    #   (1, 'Alimentari'),
    #   (2, 'Trasporti')
    # ]
    categories = cur.fetchall()

    conn.close()

    print()
    print("ID   Descrizione")
    print("-----------------------------------")

    # Se lista vuota equivale a len(...) == 0
    if not categories:
        print("Nessuna categoria presente.")
        return []

    # Scorro la lista una riga alla volta, ogni record contiene una tupla: (id, nome) quindi   
        # category[0] = id
        # category[1] = nome

    for category in categories:

        print(f"{category[0]:<4}{category[1]}")

    # Restituisco la lista perchè mi serve in altri moduli

    return categories