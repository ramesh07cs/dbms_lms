# Library Management System — Installation Guide

Complete setup instructions for the LMS project.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Application](#running-the-application)
6. [API Reference](#api-reference)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Software  | Version | Download |
|-----------|---------|----------|
| Python    | 3.8+    | https://www.python.org/downloads/ |
| Node.js   | 16+     | https://nodejs.org/ |
| PostgreSQL| 12+     | https://www.postgresql.org/ (or use [Neon](https://neon.tech)) |
| Git       | Latest  | https://git-scm.com/ |

### Verify Installation

```bash
python --version   # 3.8+
node --version     # 16+
npm --version      # 8+
```

---

## Database Setup

### Option A: Neon (Cloud, Recommended)

1. Sign up at **https://neon.tech**
2. Create a new project
3. Copy the connection string (e.g. `postgresql://user:pass@ep-xxx.region.aws.neon.tech/neondb?sslmode=require`)
4. Store it for the Backend Setup step

### Option B: Local PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:** Download from https://www.postgresql.org/download/windows/

### Create Database & Apply Schema

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE lms_db;
\q

# Apply schema
psql -h localhost -U postgres -d lms_db -f lms_backend/database/schema.sql
```

For Neon, use their SQL Editor or connect with:
```bash
psql "your_neon_connection_string" -f lms_backend/database/schema.sql
```

---

## Backend Setup

### 1. Clone and Enter Backend

```bash
cd lms_backend
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv lms_env
lms_env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv lms_env
source lms_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `psycopg2` fails, try:
```bash
pip install psycopg2-binary
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

**For Neon or any PostgreSQL URL:**
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

**For local PostgreSQL (alternative):**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=lms_db
DB_USER=postgres
DB_PASSWORD=your_password
```

Optional admin defaults:
```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrator
```

### 5. Initialize Database

```bash
python init_database.py
```

This creates tables (if schema was not applied manually) and adds a default admin user.

### 6. Start Backend

```bash
python run.py
```

Backend runs at **http://localhost:5000**

Test: http://localhost:5000/ → `{"message":"LMS Backend Running Successfully"}`

---

## Frontend Setup

### 1. Enter Frontend Directory

```bash
cd lms_frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure API URL (Optional)

By default the frontend proxies `/api` to `http://localhost:5000`. If your backend runs elsewhere:

Create `.env`:
```env
VITE_API_URL=http://localhost:5000
```

### 4. Start Development Server

```bash
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## Running the Application

### Start Both Services

**Terminal 1 — Backend:**
```bash
cd lms_backend
python run.py
```

**Terminal 2 — Frontend:**
```bash
cd lms_frontend
npm run dev
```

### Access

Open **http://localhost:5173** in a browser.

**Default admin credentials:**
- Email: `admin@example.com`
- Password: `admin123`

Change the password after first login.

---

## API Reference

Base URL: `http://localhost:5000` (or your backend URL)

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register (name, email, phone?, password, role_id: 2=Teacher, 3=Student) |
| POST | `/users/login` | Login (email, password) |
| POST | `/users/logout` | Logout (requires JWT) |
| GET | `/users/profile` | Get current user (requires JWT) |
| GET | `/users/pending` | Pending registrations (admin) |
| POST | `/users/approve/<user_id>` | Approve user (admin) |
| POST | `/users/reject/<user_id>` | Reject user (admin) |

### Books

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books/` | List all books |
| GET | `/books/unavailable` | Books with available_copies = 0 |
| GET | `/books/<id>` | Get book by ID |
| POST | `/books/` | Add book (admin) |
| PUT | `/books/<id>` | Update book (admin) |
| DELETE | `/books/<id>` | Soft delete book (admin) |

### Borrow

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/borrow/issue` | Borrow book (body: `{book_id}`) |
| POST | `/borrow/return` | Return book (body: `{book_id}`) |
| GET | `/borrow/my/active` | My active borrows |
| GET | `/borrow/my/history` | My borrow history |
| GET | `/borrow/admin/users` | Users for admin issue (admin) |
| GET | `/borrow/admin/active` | All active borrows (admin) |
| POST | `/borrow/admin/issue` | Issue to user (body: `{user_id, book_id}`) |
| POST | `/borrow/admin/return` | Return by borrow_id (body: `{borrow_id}`) |

### Reservations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reservation/create` | Create (body: `{book_id}`) |
| DELETE | `/reservation/cancel/<id>` | Cancel reservation |
| GET | `/reservation/my` | My reservations |
| GET | `/reservation/all` | All reservations (admin) |

### Fines

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/fine/my` | My unpaid fines |
| GET | `/fine/all` | All fines (admin) |
| POST | `/fine/pay/<fine_id>` | Mark paid (admin) |

### Audit

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/audit/my-logs` | My audit logs |
| GET | `/audit/all` | All audit logs (admin) |

### Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stats/admin` | Admin dashboard stats |
| GET | `/stats/teacher` | Teacher dashboard stats |
| GET | `/stats/student` | Student dashboard stats |

---

## Troubleshooting

### Backend

**"ModuleNotFoundError: No module named 'flask'"**
```bash
pip install -r requirements.txt
```

**"Database connection failed"**
- Verify `DATABASE_URL` in `.env`
- Ensure PostgreSQL is running
- For Neon: ensure `?sslmode=require` is in the URL

**"Port 5000 already in use"**
```bash
# Find process (Windows)
netstat -ano | findstr :5000

# Find process (Linux/macOS)
lsof -i :5000
```

### Frontend

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"Cannot connect to backend"**
- Ensure backend is running on port 5000
- Check proxy in `vite.config.js` (default: `/api` → `http://localhost:5000`)

**"Port 5173 already in use"**
- Vite will try 5174, 5175, etc., or stop the other process

### Database
        
**" relation does not exist"**
```bash
python init_database.py
# Or apply schema manually:
psql -h <host> -U <user> -d <db> -f lms_backend/database/schema.sql
```
        
**"User not approved"**
- Register as Student/Teacher
- Login as admin and approve from Verify Users
        
---

## Running Backend Tests

From the `lms_backend` directory, run:

```bash
pytest
```

All tests should pass for the final LMS build.
        
---
        
## Build for Production

**Backend:**
```bash
# Use gunicorn or similar
gunicorn -w 4 -b 0.0.0.0:5000 "run:app"
```

**Frontend:**
```bash
cd lms_frontend
npm run build
# Serve the dist/ folder with nginx or any static server
```

Ensure `VITE_API_URL` points to your production backend URL.
