# Library Management System (LMS)

A full-stack Library Management System for **Tribhuvan University, Thapathali Campus** built with Flask (Python) and React.

---

## Overview

The LMS manages library operations including user registration, book catalog, borrowing, returns, reservations with auto-assignment, fine management, and audit logging. It supports three roles: **Admin**, **Teacher**, and **Student**.

---

## Features

### Authentication & Roles

- JWT-based authentication (token in memory, no localStorage)
- Three roles: Admin (`role_id=1`), Teacher (`role_id=2`), Student (`role_id=3`)
- User registration (status starts as PENDING; admin must approve)
- Admin can approve or reject pending registrations

### Admin Panel

- **Dashboard** — Stats: Total Issued Books, Available Books, Students, Teachers, Fine Collected
- **Verify Users** — List and approve/reject pending registrations
- **Manage Books** — Add, Edit, Delete books (title, author, category, ISBN, total copies)
- **Issue Book** — Assign a book to any approved user
- **Return Book** — Process returns (shows fine if applicable)
- **All Reservations** — View all reservations
- **Fine Management** — List fines, mark as paid
- **Audit Logs** — View all audit activity

### Teacher Panel

- **Dashboard** — Issued books count, due today, overdue list
- **Available Books** — Borrow books (available copies > 0)
- **View Books** — Full book catalog
- **Borrowed Books** — Return borrowed books
- **Reservations** — Reserve unavailable books

### Student Panel

- **Dashboard** — Currently borrowed, due soon, total fines, active reservations
- **Available Books** — Borrow books (available copies > 0)
- **View Books** — Full catalog
- **Borrowed Books** — View and return borrowed books
- **Reservations** — Reserve unavailable books (join waiting queue)
- **My Fines** — View unpaid fines

### Reservation System

- **Reservation priority** — If a book has ACTIVE reservations, only the first user in queue can borrow; others receive "Book reserved by another user"
- **Auto-assignment** — When a book is returned, it is automatically issued to the first user in the reservation queue
- FIFO queue with expiry handling

---

## Tech Stack

| Layer     | Technology                    |
|-----------|-------------------------------|
| Backend   | Python, Flask, PostgreSQL     |
| Database  | Raw SQL (psycopg2, RealDictCursor) |
| Frontend  | React 18, Vite                |
| Styling   | TailwindCSS                   |
| Auth      | JWT (Flask-JWT-Extended)      |
| API       | REST, Axios                   |

---

## Project Structure

```
updated_lms_dbms/
├── Readme.md           # Project overview (this file)
├── installation.md     # Detailed setup & API reference
├── setup_guide.txt     # Quick reference
├── lms_backend/        # Flask API
│   ├── app/
│   │   ├── models/     # DB queries
│   │   ├── routes/     # API endpoints
│   │   ├── services/   # Business logic
│   │   ├── schemas/    # Validation
│   │   └── utils/      # Decorators, error handlers
│   ├── database/
│   │   └── schema.sql  # DB schema & seeds
│   ├── run.py          # Start server
│   ├── init_database.py
│   └── .env.example
└── lms_frontend/       # React app
    ├── src/
    │   ├── api/        # API services
    │   ├── context/    # Auth context
    │   ├── layouts/    # Sidebar layouts
    │   ├── pages/      # Route components
    │   └── components/
    ├── package.json
    └── vite.config.js
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL (or [Neon](https://neon.tech) for cloud DB)

### 1. Database Setup

Create a PostgreSQL database and apply the schema:

```bash
psql -h <host> -U <user> -d <database> -f lms_backend/database/schema.sql
```

### 2. Backend Setup

```bash
cd lms_backend
cp .env.example .env
# Edit .env and set DATABASE_URL
pip install -r requirements.txt
python init_database.py
python run.py
```

Backend runs at **http://localhost:5000**

### 3. Frontend Setup

```bash
cd lms_frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:5173**

### 4. Access

Open http://localhost:5173 in a browser.

**Default admin** (after `init_database.py`):

- Email: `admin@example.com`
- Password: `admin123`

⚠️ Change the password after first login.

---

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/login` | Login |
| POST | `/users/register` | Register |
| POST | `/users/logout` | Logout |
| GET | `/users/pending` | List pending users (admin) |
| POST | `/users/approve/<id>` | Approve user (admin) |
| GET | `/books/` | List all books |
| GET | `/books/unavailable` | Books with no copies |
| POST | `/borrow/issue` | Borrow book (student/teacher) |
| POST | `/borrow/return` | Return book |
| GET | `/borrow/my/active` | My active borrows |
| POST | `/reservation/create` | Create reservation |
| DELETE | `/reservation/cancel/<id>` | Cancel reservation |
| GET | `/fine/my` | My unpaid fines |
| GET | `/audit/my-logs` | My audit logs |
| GET | `/audit/all` | All audit logs (admin) |

See `installation.md` for the complete API reference.

---

## Running Tests

Backend tests (pytest) are available under `lms_backend/tests`.

```bash
cd lms_backend
pytest
```

All tests should pass for the final LMS build.

---

## Security

- JWT tokens stored in memory only (not localStorage)
- Role-based access control
- Students/Teachers cannot issue books for other users
- Only Admin can issue books for any user
- Password hashing (Werkzeug)
- Parameterized SQL (SQL injection prevention)

---

## License

This project is for educational purposes (Tribhuvan University, Thapathali Campus).
