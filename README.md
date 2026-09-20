# Exam Room Allocation Database Manager

A simple Flask + SQLAlchemy website for managing the supplied exam-room-allocation database. The initial version intentionally focuses on only two operations: **add rows** and **delete rows**.

## Run with the included local demo database

```bash
cd exam-room-app
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Open `http://localhost:5000`.

## Connect to your local DBMS

Set `DATABASE_URL` before starting the app.

```bash
# MySQL / MariaDB
export DATABASE_URL='mysql+pymysql://root:rhs242007@127.0.0.1:3306/exam_room_allocation_system'

# PostgreSQL
export DATABASE_URL='postgresql+psycopg2://USERNAME:PASSWORD@127.0.0.1:5432/DATABASE_NAME'

# SQLite
export DATABASE_URL='sqlite:////absolute/path/to/exam_room_allocation.db'

python app.py
```

For MySQL, the alternative variables `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` are also supported.

## What the website does

The left sidebar lists every table discovered in the connected database. Select a table to view its rows, enter values in the add-row form, or delete an existing row using its primary key. All inserts and deletes are executed directly against the connected database, so database constraints such as required fields, foreign keys, unique values, and primary keys remain active.

The application does not include report builders, CSV exports, advanced query builders, or arbitrary SQL execution in this initial version. Those features can be added later after the basic database operations are comfortable to use.
