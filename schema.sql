
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE,
    name TEXT,
    balance REAL DEFAULT 0,
    points INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE,
    name TEXT,
    price REAL,
    cost REAL,
    stock INTEGER DEFAULT 0,
    is_alcohol INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    type TEXT,
    value REAL,
    min_spend REAL DEFAULT 0,
    expire_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no TEXT UNIQUE,
    member_id INTEGER,
    total REAL,
    status TEXT DEFAULT 'open',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(member_id) REFERENCES members(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    inventory_id INTEGER,
    qty INTEGER,
    price REAL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(inventory_id) REFERENCES inventory(id)
);

CREATE TABLE IF NOT EXISTS stored_bottles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    inventory_id INTEGER,
    bottle_label TEXT UNIQUE,
    qty INTEGER DEFAULT 1,
    stored_at TEXT DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    FOREIGN KEY(member_id) REFERENCES members(id),
    FOREIGN KEY(inventory_id) REFERENCES inventory(id)
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);
