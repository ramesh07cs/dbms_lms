-- LMS Schema (raw SQL, no ORM)

CREATE TABLE IF NOT EXISTS roles (
    role_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed roles (idempotent)
INSERT INTO roles (role_name)
VALUES ('ADMIN'), ('TEACHER'), ('STUDENT')
ON CONFLICT (role_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(role_id) ON DELETE SET NULL,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'PENDING'
    CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    approved_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    book_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    category VARCHAR(50),
    isbn VARCHAR(20) UNIQUE,
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS borrows (
    borrow_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id  INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(book_id),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    borrow_status VARCHAR(20) DEFAULT 'ISSUED'
    CHECK (borrow_status IN ('ISSUED', 'RETURNED', 'OVERDUE'))
);

CREATE TABLE IF NOT EXISTS auditlog (
    audit_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(50),
    record_id INTEGER,
    description TEXT,
    log_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fine (
    fine_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    borrow_id  INTEGER NOT NULL REFERENCES borrows(borrow_id),
    user_id  INTEGER NOT NULL REFERENCES users(user_id),
    amount DECIMAL(10, 2) NOT NULL,
    paid_status BOOLEAN DEFAULT FALSE,
    paid_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    book_id INTEGER REFERENCES books(book_id),
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    reservation_status VARCHAR(20) DEFAULT 'ACTIVE'
    CHECK (reservation_status IN ('ACTIVE', 'EXPIRED', 'CANCELLED'))
);

