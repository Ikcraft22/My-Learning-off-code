import pandas as pd
from reportlab.pdfgen import canvas
from database.connection import connect_db
import os

def generate_excel_report(report_type):
    """Exporta dinámicamente registros a Excel según el tipo seleccionado."""
    conn = connect_db()
    if conn:
        try:
            filename = f"reporte_{report_type.lower().split()[0]}.xlsx"
            query = ""
            
            if "Pacientes" in report_type:
                query = "SELECT * FROM patients"
            elif "Doctores" in report_type:
                query = "SELECT * FROM doctors"
            elif "Citas" in report_type or "Casos" in report_type:
                query = """
                    SELECT p.name AS Paciente, d.name AS Doctor, a.appointment_date AS Fecha, a.reason AS Motivo, a.status AS Estado
                    FROM appointments a
                    LEFT JOIN patients p ON a.patient_id = p.id
                    LEFT JOIN doctors d ON a.doctor_id = d.id
                """
            
            df = pd.read_sql(query, conn)
            df.to_excel(filename, index=False)
            print(f"Reporte Excel generado: {filename}")
        except Exception as e:
            print(f"Error al generar Excel: {e}")
        finally:
            conn.close()

def generate_pdf_report(report_type):
    """Genera un reporte PDF basado en la selección: Pacientes, Doctores o Citas."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            filename = f"reporte_{report_type.lower().split()[0]}.pdf"
            c = canvas.Canvas(filename)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 800, f"Reporte Oficial de {report_type}")
            c.setFont("Helvetica", 10)
            
            y = 750
            
            if "Pacientes" in report_type:
                cursor.execute("SELECT name, age, gender, allergy FROM patients")
                for r in cursor.fetchall():
                    c.drawString(100, y, f"Nombre: {r[0]} | Edad: {r[1]} | Género: {r[2]} | Alergia: {r[3]}")
                    y -= 20
                    if y < 50: break
            
            elif "Doctores" in report_type:
                cursor.execute("SELECT name, specialty, phone FROM doctors")
                for r in cursor.fetchall():
                    c.drawString(100, y, f"Nombre: {r[0]} | Especialidad: {r[1]} | Tel: {r[2]}")
                    y -= 20
                    if y < 50: break
            
            elif "Citas" in report_type or "Casos" in report_type:
                query = """
                    SELECT p.name, d.name, a.appointment_date, a.reason 
                    FROM appointments a 
                    LEFT JOIN patients p ON a.patient_id = p.id 
                    LEFT JOIN doctors d ON a.doctor_id = d.id
                """
                cursor.execute(query)
                for r in cursor.fetchall():
                    c.drawString(100, y, f"Pac: {r[0]} | Dr: {r[1]} | Fecha: {str(r[2])[:16]} | Motivo: {r[3]}")
                    y -= 20
                    if y < 50: break

            c.save()
            print(f"Reporte PDF generado: {filename}")
        except Exception as e:
            print(f"Error al generar reporte: {e}")
        finally:
            conn.close()