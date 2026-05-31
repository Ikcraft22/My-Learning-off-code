from database.connection import connect_db

def get_all_records(table):
    """Obtiene todos los registros de una tabla específica."""
    conn = connect_db()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()
    finally:
        conn.close()

def insert_record(table, data):
    """Inserta un registro dinámicamente en cualquier tabla."""
    conn = connect_db()
    if not conn: return False
    try:
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al insertar en {table}: {e}")
        return False
    finally:
        conn.close()

def get_summary_stats():
    """Obtiene estadísticas rápidas para el sistema."""
    conn = connect_db()
    stats = {"pacientes": 0, "doctores": 0, "citas": 0}
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        stats["pacientes"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM doctors")
        stats["doctores"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM appointments")
        stats["citas"] = cursor.fetchone()[0]
        conn.close()
    return stats