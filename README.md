# 📚 Library Management System (LMS) Backend

A Flask-based backend for a Library Management System built using **Raw SQL (no ORM)** and PostgreSQL.

---

## 🚀 Features

- User Registration & Login
- Role-based system (Admin, Teacher, Student)
- Book Management
- Borrow & Return System
- Transaction Handling
- Clean Layered Architecture
- Password Hashing (Secure Storage)

---

## 🏗 Architecture

Client → Routes → Services → Query Layer → PostgreSQL

- **Routes** → API Endpoints
- **Services** → Business Logic
- **Models (Query Layer)** → Raw SQL Queries
- **Database** → PostgreSQL

---

## 🛠 Tech Stack

- Python (Flask)
- PostgreSQL
- psycopg2
- Raw SQL
- python-dotenv
- werkzeug (password hashing)

---

## 📂 Project Structure

Project root
- `app/` — application code (routes, services, models)
  - `models/` — DB connection and raw SQL query modules
  - `routes/` — Flask blueprints / endpoints
  - `services/` — business logic
- `database/`
  - `schema.sql` — **database schema and seeds** (moved here from `app/models`)
- `run.py` — start the Flask app
- `requirements.txt` — Python dependencies
- `.env.example` — example environment variables

---

## 🗂 Database schema (important) 🔧
- The SQL schema file is now located at `database/schema.sql`. If you previously referenced `app/models/schema.sql`, update your scripts or documentation.
- The Flask app does **not** load `schema.sql` at runtime; it only manages DB connections (see `app/models/db.py`).

How to apply the schema manually:

```bash
psql -h <host> -U <user> -d <database> -f database/schema.sql
```

Use this when creating or resetting the database locally or in CI.

---

## 🚀 Run locally
1. Copy `.env.example` → `.env` and set DB credentials.
2. Activate virtualenv: `lms_env\Scripts\activate` (Windows).
3. Install deps: `pip install -r requirements.txt`.
4. Start server: `python run.py`.

---

## 💡 Notes
- Moving `schema.sql` only affects setup/automation that reference the file path; the runtime DB connection will not be affected.
- I can update other docs or CI scripts that still point to the old path — tell me which files to change.

