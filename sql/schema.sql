PRAGMA foreign_keys = ON;

-- =====================================
-- TABLE: expense_category
-- =====================================
CREATE TABLE IF NOT EXISTS expense_category (
    category_id     INTEGER PRIMARY KEY AUTOINCREMENT, -- sqlite_sequence
    category_name   TEXT NOT NULL UNIQUE,
    category_status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME
);

-- =====================================
-- TABLE: expense_transaction
-- =====================================
CREATE TABLE IF NOT EXISTS expense_transaction (
    expense_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_date    TEXT NOT NULL CHECK (transaction_date LIKE '____-__-__'),
    transaction_amount  NUMERIC NOT NULL CHECK (transaction_amount > 0),
    category_id         INTEGER NOT NULL,
    expense_description TEXT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id)
        REFERENCES expense_category(category_id)
);

-- =====================================
-- TABLE: monthly_budget
-- =====================================
CREATE TABLE IF NOT EXISTS monthly_budget (
    budget_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    budget_period   TEXT NOT NULL CHECK (budget_period LIKE '____-__'),
    category_id     INTEGER NOT NULL,
    budget_amount   NUMERIC NOT NULL CHECK (budget_amount > 0),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME,

    UNIQUE (budget_period, category_id),

    FOREIGN KEY (category_id)
        REFERENCES expense_category(category_id)
);