DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gallery;
DROP TABLE IF EXISTS maps;

-- USER ACCOUNTS
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,

    birthday TEXT NOT NULL,
    phone TEXT NOT NULL,
    stage TEXT NOT NULL CHECK(stage IN ('Primary', 'Middle', 'High', 'Older')),

    home_location TEXT NOT NULL,

    role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'leader', 'admin')) DEFAULT 'student',

    sector TEXT CHECK(sector IN ('أشبال وزهرات', 'مبتداء ومرشدات', 'متقدم', 'جوالة')),

    approved INTEGER NOT NULL DEFAULT 0
);

-- GALLERY: photos/videos for face recognition
CREATE TABLE gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    face_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- HOME LOCATION MAP COORDINATES
CREATE TABLE maps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
