# 🚀 Library Management System - Installation Guide

Complete step-by-step guide to get your library management system running.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup (Neon - Recommended)](#database-setup-neon---recommended)
3. [Alternative: Local PostgreSQL](#alternative-local-postgresql)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Install these before starting:

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| Python | 3.8+ | https://www.python.org/downloads/ |
| Node.js | 16+ | https://nodejs.org/ |
| Git | Latest | https://git-scm.com/ |

### Verify Installation

```bash
python --version    # Should show 3.8 or higher
node --version      # Should show 16 or higher
npm --version       # Should show 8 or higher
git --version       # Should show installed version
```

---

## Database Setup (Neon - Recommended)

**Why Neon?**
- ✅ Free tier (no credit card required)
- ✅ No local PostgreSQL installation needed
- ✅ Cloud-hosted (access from anywhere)
- ✅ Automatic backups
- ✅ Takes only 2 minutes to setup

### Step 1: Create Neon Account

1. Go to **https://neon.tech**
2. Click **"Sign Up"**
3. Sign up with GitHub, Google, or Email
4. Verify your email (if required)

### Step 2: Create Project

1. Click **"Create a project"** or **"New Project"**
2. Fill in details:
   - **Project name:** `library-management`
   - **PostgreSQL version:** 16 (recommended)
   - **Region:** Choose closest to you
3. Click **"Create project"**

### Step 3: Get Connection String

After project creation, you'll see a **Connection Details** section.

1. Click **"Connection string"**
2. Select **"Pooled connection"** (recommended)
3. Copy the entire connection string

It looks like:
```
postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Step 4: Save Connection String

Keep this string safe - you'll need it in the next section!

**⚠️ Important:** Never share this string publicly or commit it to GitHub.

---

## Alternative: Local PostgreSQL

Only follow this if you don't want to use Neon.

### Install PostgreSQL

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**On macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**On Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run installer with default settings
- Remember the password you set for postgres user

### Create Database

```bash
# Access PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE library_db;

# Exit
\q
```

---

## Backend Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/swagat017/dbms.git
cd dbms
```

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**If you get "pip: command not found":**
```bash
python -m pip install -r requirements.txt
```

### Step 3: Configure Database

```bash
# Create .env file
cp .env.example .env
```

Now edit the `.env` file:

**For Neon (Recommended):**
```bash
# Open .env in your text editor
# Replace this line with your actual Neon connection string:
DATABASE_URL=postgresql://your-actual-connection-string-here
```

**For Local PostgreSQL:**
```bash
# In .env file, comment out DATABASE_URL and uncomment these:
# DATABASE_URL=...  (comment this out)

DB_HOST=localhost
DB_PORT=5432
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

### Step 4: Initialize Database

```bash
python setup_db.py
```

**Expected output:**
```
============================================================
Library Management System - Database Setup
============================================================

Step 1: Creating database...
✓ Database 'library_db' created successfully

Step 2: Initializing schema...
✓ Database schema initialized successfully

Step 3: Creating default admin user...
✓ Admin user created (email: admin@library.com, password: admin123)

============================================================
✓ Database setup completed successfully!
============================================================
```

### Step 5: Test Backend

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
```

**Test it:** Open http://localhost:5000/health in browser
- Should see: `{"status":"healthy","database":"connected"}`

Press `Ctrl+C` to stop the server.

---

## Frontend Setup

Open a **NEW terminal** (keep backend running).

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

**This might take 2-3 minutes.**

### Step 2: Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

---

## Running the Application

### Start Both Services

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Access Application

1. Open browser: **http://localhost:3000**
2. You'll see the login page

### Default Admin Login

```
Email:    admin@library.com
Password: admin123
```

**⚠️ IMPORTANT:** Change the admin password after first login!

---

## First Steps After Login

1. **Change Password** (recommended)
2. **Create a test user:**
   - Click "Register" (logout first)
   - Fill in details
   - Login as admin
   - Go to "User Management" → Approve the user
3. **Add some books:**
   - Go to "Book Management"
   - Click "Add Book"
4. **Test borrowing:**
   - Login as the approved user
   - Browse books
   - Admin can issue books to users

---

## Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

#### "psycopg2 installation error"
```bash
# Try this instead:
pip install psycopg2-binary
```

#### "Database connection failed"
- **Neon:** Check your DATABASE_URL is correct
- **Local:** Make sure PostgreSQL is running
  ```bash
  # Check status
  sudo systemctl status postgresql  # Linux
  brew services list               # macOS
  ```

#### "Port 5000 already in use"
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows
```

### Frontend Issues

#### "npm: command not found"
- Install Node.js from https://nodejs.org/

#### "npm install fails"
```bash
# Clear cache and try again
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### "Cannot connect to backend API"
- Make sure backend is running on port 5000
- Check browser console for errors
- Try: http://localhost:5000/health

#### "Port 3000 already in use"
- Vite will automatically use port 3001 or 3002
- Or kill the process:
  ```bash
  lsof -ti:3000 | xargs kill -9  # Mac/Linux
  ```

### Database Issues

#### "Authentication failed"
- **Neon:** Double-check your connection string
- **Local:** Verify postgres password

#### "Database does not exist"
```bash
# Run setup script again
python setup_db.py
```

#### "SSL required" (Neon)
- Make sure connection string ends with `?sslmode=require`

---

## Verification Checklist

- [ ] Backend runs on http://localhost:5000
- [ ] `/health` endpoint returns healthy status
- [ ] Frontend runs on http://localhost:3000
- [ ] Can see login page
- [ ] Can login with admin credentials
- [ ] Dashboard loads successfully

---

## Quick Reference

### Start Application
```bash
# Terminal 1
cd backend && python app.py

# Terminal 2
cd frontend && npm run dev
```

### Stop Application
- Press `Ctrl+C` in both terminals

### Reset Database
```bash
cd backend
python setup_db.py  # This will recreate everything
```

### View Logs
- Backend: Check terminal where `app.py` is running
- Frontend: Check browser console (F12)

---

## Next Steps

1. ✅ Change admin password
2. ✅ Create test users and approve them
3. ✅ Add books to the library
4. ✅ Test borrowing workflow
5. ✅ Explore admin features

---

## Need Help?

- **Documentation:** See `SETUP_GUIDE.txt` and `README.md`
- **Database Schema:** Check `backend/database/schema.sql`
- **API Docs:** See `backend/SETUP.txt`

---

## Development Tips

### Add New Python Package
```bash
cd backend
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

### Add New npm Package
```bash
cd frontend
npm install package-name
```

### View Database (Neon)
1. Go to https://console.neon.tech
2. Select your project
3. Click "SQL Editor"
4. Run queries directly

### View Database (Local)
```bash
psql -U postgres -d library_db
\dt  # List tables
\q   # Quit
```

---

## Production Deployment

For deploying to production, see our deployment guides:
- Backend: Deploy to Render/Railway/Heroku
- Frontend: Deploy to Vercel/Netlify
- Database: Use Neon (already production-ready!)

---

**🎉 Congratulations! Your Library Management System is ready!**

Happy coding! 📚✨
