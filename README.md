# Expense Manager

## Requisiti

L’applicazione è stata sviluppata utilizzando **Python 3.14.3**.  
Per eseguire il progetto è necessario avere installato **Python 3.x**.

---

## Avvio dell’applicazione

Aprire un terminale (o prompt dei comandi), posizionarsi nella directory principale del progetto ed eseguire il seguente comando:

```bash
python src/main.py
```

---

## Librerie utilizzate

L’applicazione utilizza esclusivamente moduli standard inclusi nella distribuzione ufficiale di Python, senza dipendenze esterne.

In particolare:

- `sqlite3` — gestione del database SQLite
- `datetime` — validazione e gestione delle date
- `pathlib` — gestione dei percorsi dei file in modo portabile

---

## Database

Il progetto utilizza un database SQLite denominato:

```text
demo/expenses.db
```

Nel repository è già incluso un database SQLite dimostrativo preconfigurato e popolato con categorie, transazioni e dati di esempio utili per testare immediatamente le funzionalità dell’applicazione e la generazione dei report, senza necessità di configurazioni aggiuntive.

---

## Inizializzazione del Database

Nel caso si desideri ricreare il database da zero, è possibile eliminare il file `demo/expenses.db`

ed eseguire, dalla directory principale del progetto, il seguente comando:

```bash
python src/init_db.py
```

Lo script esegue automaticamente il file `sql/schema.sql`, creando la struttura del database e tutte le tabelle necessarie al funzionamento dell’applicazione.


Il repository include inoltre lo script `demo/load_seed_data.py`, utilizzato per popolare il database con alcune categorie di esempio.

Per eseguire lo script dalla directory principale del progetto:

```bash
python demo/load_seed_data.py
```
---

## Note

L’applicazione è configurata per utilizzare automaticamente il database presente nella cartella `demo/`.
