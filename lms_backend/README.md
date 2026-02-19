LMS Backend
===========

Minimal Flask-based LMS backend. This README covers quick setup and how to run tests.

Setup
-----

1. Create a `.env` in the `lms_backend` folder with either:

   - `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
   or
   - set `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and optionally `DB_PORT`.

2. Install dependencies (preferably in a venv):

```bash
python -m pip install -r requirements.txt
```

Initialize database
-------------------

Run the DB initialization script to create tables:

```bash
python init_database.py
```

Run the app
-----------

```bash
python run.py
```

Running tests
-------------

Unit and service-level tests use `pytest`.

Install dev deps and run tests:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

Notes
-----
- Tests under `tests/` are isolated and mock DB/model interactions where appropriate.
- For full integration tests you need a running Postgres instance and a DATABASE_URL.
