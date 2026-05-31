import os
import mysql.connector
import traceback

DB_NAME = "hospital_system"


def _get_setup_sql_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "setup.sql")


def _load_setup_sql():
    path = _get_setup_sql_path()
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _execute_setup_sql(conn):
    sql = _load_setup_sql()
    if not sql:
        return
    cursor = conn.cursor()
    try:
        for statement in sql.split(";"):
            statement = statement.strip()
            if not statement or statement.startswith("--"):
                continue
            cursor.execute(statement)
        conn.commit()
    finally:
        cursor.close()


def _log_error(exc):
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_error.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(traceback.format_exc())


def connect_db():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # ¡CAMBIA ESTO POR TU CONTRASEÑA REAL!
            autocommit=False,
        )
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
            conn.database = DB_NAME
        finally:
            cursor.close()

        _execute_setup_sql(conn)
        return conn
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        _log_error(e)
        return None