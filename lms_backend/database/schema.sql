-- =========================
-- ROLES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS roles (
    role_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed roles (idempotent)
INSERT INTO roles (role_name)
VALUES ('ADMIN'), ('TEACHER'), ('STUDENT')
ON CONFLICT (role_name) DO NOTHING;


-- =========================
-- USERS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles(role_id) ON DELETE RESTRICT,
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_by INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    approved_at TIMESTAMP
);


-- =========================
-- BOOKS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS books (
    book_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    category VARCHAR(50),
    isbn VARCHAR(20) UNIQUE,
    total_copies INTEGER NOT NULL CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL CHECK (
        available_copies >= 0 AND available_copies <= total_copies
    ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);


-- =========================
-- BORROWS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS borrows (
    borrow_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    book_id INTEGER NOT NULL REFERENCES books(book_id),
    issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    borrow_status VARCHAR(20) DEFAULT 'ISSUED'
        CHECK (borrow_status IN ('ISSUED', 'RETURNED', 'OVERDUE'))
);

-- Prevent same user borrowing same book twice without returning
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_borrow
ON borrows(user_id, book_id)
WHERE borrow_status = 'ISSUED';


-- =========================
-- FINE TABLE
-- =========================
CREATE TABLE IF NOT EXISTS fines (
    fine_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    borrow_id INTEGER NOT NULL REFERENCES borrows(borrow_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    paid_status BOOLEAN DEFAULT FALSE,
    paid_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_borrow_fine UNIQUE (borrow_id)
);



-- =========================
-- RESERVATIONS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(book_id) ON DELETE CASCADE,
    reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date TIMESTAMP,
    reservation_status VARCHAR(20) DEFAULT 'ACTIVE'
    CHECK (reservation_status IN ('ACTIVE', 'FULFILLED', 'EXPIRED', 'CANCELLED'))
);

-- Prevent duplicate active reservation by same user
CREATE UNIQUE INDEX IF NOT EXISTS unique_active_reservation
ON reservations(user_id, book_id)
WHERE reservation_status = 'ACTIVE';


-- =========================
-- AUDIT LOGS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    description TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

