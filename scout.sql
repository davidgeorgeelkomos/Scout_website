DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gallery;
DROP TABLE IF EXISTS maps;

-- USER ACCOUNTS (everyone = student for now)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,

    birthday TEXT NOT NULL,
    phone TEXT NOT NULL,

    -- student sector
    sector TEXT NOT NULL CHECK(sector IN ('أشبال وزهرات', 'مبتداء ومرشدات', 'متقدم', 'جوالة')),

    approved INTEGER NOT NULL DEFAULT 1
);

-- GALLERY: for future face recognition
CREATE TABLE gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    face_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- HOME LOCATION stored cleanly here
CREATE TABLE maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
