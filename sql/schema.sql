PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS lessons;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS leads;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    registration_date TEXT NOT NULL,
    country TEXT NOT NULL,
    city TEXT NOT NULL,
    age INTEGER NOT NULL,
    traffic_source TEXT NOT NULL,
    device TEXT NOT NULL,
    is_active INTEGER NOT NULL
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    category TEXT NOT NULL,
    course_price REAL NOT NULL,
    duration_weeks INTEGER NOT NULL
);

CREATE TABLE leads (
    lead_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    lead_date TEXT NOT NULL,
    lead_status TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_status TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE lessons (
    lesson_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    lesson_date TEXT NOT NULL,
    lesson_type TEXT NOT NULL,
    attendance_status TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);