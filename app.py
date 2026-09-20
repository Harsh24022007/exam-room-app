import os
from datetime import date, datetime, time
from urllib.parse import quote_plus

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import MetaData, Table, and_, create_engine, delete, inspect, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.sqltypes import Boolean, Date, DateTime, Integer, Numeric, Time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = f"sqlite:///{os.path.join(BASE_DIR, 'exam_room_allocation.db')}"
DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DB)

if os.getenv('DB_HOST') and os.getenv('DB_NAME') and not os.getenv('DATABASE_URL'):
    user = quote_plus(os.getenv('DB_USER', 'root'))
    password = quote_plus(os.getenv('DB_PASSWORD', ''))
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '3306')
    name = os.getenv('DB_NAME')
    DATABASE_URL = f"mysql+pymysql://root:rhs242007@127.0.0.1:3306/exam_room_allocation_system"


engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)
metadata = MetaData()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change-this-secret-in-production')


def table_names():
    return inspect(engine).get_table_names()


def get_table(name):
    if name not in table_names():
        raise ValueError(f"Unknown table: {name}")
    return Table(name, metadata, autoload_with=engine)


def display_value(value):
    if value is None:
        return ''
    return value.isoformat(sep=' ') if isinstance(value, datetime) else str(value)


def parse_value(column, raw):
    if raw == '':
        return None
    typ = column.type
    if isinstance(typ, Boolean):
        return raw.lower() in ('1', 'true', 'yes', 'on')
    if isinstance(typ, Integer):
        return int(raw)
    if isinstance(typ, Numeric):
        return float(raw)
    if isinstance(typ, Date):
        return date.fromisoformat(raw)
    if isinstance(typ, DateTime):
        return datetime.fromisoformat(raw)
    if isinstance(typ, Time):
        return time.fromisoformat(raw)
    return raw


def row_dict(row):
    return {key: display_value(value) for key, value in row._mapping.items()}


@app.template_filter('pretty')
def pretty(value):
    return str(value).replace('_', ' ').title()


@app.route('/')
def index():
    names = table_names()
    return redirect(url_for('browse', table_name=names[0])) if names else render_template('empty.html')


@app.route('/table/<table_name>')
def browse(table_name):
    try:
        table = get_table(table_name)
        names = table_names()
        columns = list(table.columns)
        pk_names = [column.name for column in table.primary_key.columns]
        with engine.connect() as conn:
            rows = [row_dict(row) for row in conn.execute(select(table).order_by(*table.primary_key.columns) if pk_names else select(table))]
        return render_template('table.html', table_name=table_name, names=names, columns=columns,
                               pk_names=pk_names, rows=rows)
    except (ValueError, SQLAlchemyError) as exc:
        flash(str(exc), 'error')
        return redirect(url_for('index'))


@app.post('/table/<table_name>/insert')
def insert_row(table_name):
    try:
        table = get_table(table_name)
        values = {}
        for column in table.columns:
            raw = request.form.get(column.name, '').strip()
            if raw != '':
                values[column.name] = parse_value(column, raw)
        if not values:
            raise ValueError('Enter at least one value.')
        with engine.begin() as conn:
            conn.execute(table.insert().values(**values))
        flash(f'Row added to {table_name}.', 'success')
    except (ValueError, SQLAlchemyError) as exc:
        flash(f'Could not add row: {exc}', 'error')
    return redirect(url_for('browse', table_name=table_name))


@app.post('/table/<table_name>/delete')
def delete_row(table_name):
    try:
        table = get_table(table_name)
        if not table.primary_key.columns:
            raise ValueError('This table has no primary key, so safe deletion is unavailable.')
        pk_values = {}
        for column in table.primary_key.columns:
            raw = request.form.get(f'pk_{column.name}', '')
            if raw == '':
                raise ValueError('A primary-key value is required.')
            pk_values[column.name] = parse_value(column, raw)
        with engine.begin() as conn:
            result = conn.execute(delete(table).where(and_(*(table.c[key] == value for key, value in pk_values.items()))))
            if result.rowcount == 0:
                raise ValueError('No matching row found.')
        flash(f'Row deleted from {table_name}.', 'success')
    except (ValueError, SQLAlchemyError) as exc:
        flash(f'Could not delete row: {exc}', 'error')
    return redirect(url_for('browse', table_name=table_name))


@app.context_processor
def inject_helpers():
    return {'database_url': DATABASE_URL.split('@')[-1], 'is_sqlite': DATABASE_URL.startswith('sqlite')}


if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST', '0.0.0.0'), port=int(os.getenv('PORT', '5000')), debug=os.getenv('FLASK_DEBUG', '1') == '1')
