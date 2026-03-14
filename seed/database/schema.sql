-- Test schema for Database domain evaluation (SQLite).
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT
);
CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  amount REAL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY,
  name TEXT,
  price REAL
);
INSERT OR REPLACE INTO users (id, name, role) VALUES (1, 'Alice', 'admin'), (2, 'Bob', 'user'), (3, 'Carol', 'user');
INSERT OR REPLACE INTO orders (id, user_id, amount) VALUES (1, 1, 10.5), (2, 1, 20.0), (3, 2, 15.0);
INSERT OR REPLACE INTO products (id, name, price) VALUES (1, 'A', 1.5), (2, 'B', 2.0), (3, 'C', 3.0);
