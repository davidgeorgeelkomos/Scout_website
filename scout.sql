DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gallery;
DROP TABLE IF EXISTS maps;

-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,

    birthday TEXT NOT NULL,
    phone TEXT NOT NULL,

    sector TEXT NOT NULL CHECK (
        sector IN ('أشبال وزهرات', 'مبتداء ومرشدات', 'متقدم', 'جوالة')
    ),

    approved INTEGER NOT NULL DEFAULT 1
);

-- =========================
-- MAP LOCATIONS
-- =========================
CREATE TABLE maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- =========================
-- GALLERY (FUTURE USE)
-- =========================
CREATE TABLE gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    face_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);