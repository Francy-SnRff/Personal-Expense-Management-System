
from category_manager import manage_categories
from expense_manager import add_expense
from budget_manager import manage_budget
from report_manager import manage_reports


def show_menu():
    print()
    print("==============================")
    print("   SISTEMA SPESE PERSONALI")
    print("==============================")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("==============================")


def show_message(message):
    print()
    print(message)


def main():

    running = True
    while running:
        show_menu()
        choice = input("Inserisci la tua scelta: ").strip()
 
        match choice:
            case "1":
                manage_categories()

            case "2":
                add_expense()

            case "3":
                manage_budget()

            case "4":
                manage_reports()

            case "5":
                show_message("Chiusura applicazione...")
                running = False

            case _:
                show_message("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()