import customtkinter as ctk
import sys
from modules.simulation import SimulationWindow # Importa la nueva clase de ventana de simulación
from modules.forms import GenericManager
from modules.database_ops import get_summary_stats

# Intentamos importar los módulos, si fallan, lo sabremos de inmediato
try:
    from modules.reports import generate_pdf_report, generate_excel_report
    print("Módulos cargados correctamente.")
except ImportError as e: # Cambiado a ImportError para ser más específico
    print(f"Aviso: Algunos módulos funcionales no se cargaron: {e}")

# Intentamos cargar el dashboard por separado para manejar su ausencia
try:
    from modules.dashboard import show_patient_distribution
except ImportError:
    show_patient_distribution = None
    print("Aviso: No se pudo cargar el módulo de Dashboard.")

class HospitalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Salud Vital - Sistema de Gestión Integral")
        self.geometry("900x600")

        # Layout Principal (Sidebar y Contenido)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="HOSPITAL\nSALUD VITAL", font=("Arial", 20, "bold")).pack(pady=20)
        
        # Sección Gestión
        ctk.CTkLabel(self.sidebar, text="GESTIÓN", font=("Arial", 12, "bold")).pack(pady=(10,0))
        ctk.CTkButton(self.sidebar, text="Pacientes", command=lambda: self.manage("Pacientes", "patients", [("Nombre", "name"), ("Edad", "age"), ("Género", "gender"), ("Alergia", "allergy"), ("Teléfono", "phone")])).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="Doctores", command=lambda: self.manage("Doctores", "doctors", [("Nombre", "name"), ("Especialidad", "specialty"), ("Teléfono", "phone")])).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="Citas Médicas", command=lambda: self.manage("Citas", "appointments", [("ID Paciente", "patient_id"), ("ID Doctor", "doctor_id"), ("Motivo", "reason")])).pack(pady=5, padx=10)

        # Sección Reportes y Herramientas
        ctk.CTkLabel(self.sidebar, text="HERRAMIENTAS", font=("Arial", 12, "bold")).pack(pady=(20,0))
        ctk.CTkButton(self.sidebar, text="Simular Flujo", fg_color="#3498db", command=self.open_simulation_window).pack(pady=5, padx=10)
        
        self.stats_option = ctk.CTkOptionMenu(self.sidebar, values=["Género", "Alergia"])
        self.stats_option.pack(pady=5, padx=10)
        self.stats_option.set("Género")
        ctk.CTkButton(self.sidebar, text="Estadísticas", fg_color="#2ecc71", command=self.open_dashboard).pack(pady=5, padx=10)
        
        self.report_option = ctk.CTkOptionMenu(self.sidebar, values=["Pacientes", "Doctores", "Citas (Casos)"])
        self.report_option.pack(pady=(20, 5), padx=10)
        self.report_option.set("Pacientes")
        ctk.CTkButton(self.sidebar, text="Exportar PDF", fg_color="#e74c3c", command=lambda: generate_pdf_report(self.report_option.get())).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="Exportar Excel", fg_color="#f1c40f", text_color="black", command=lambda: generate_excel_report(self.report_option.get())).pack(pady=5, padx=10)

        # Panel Central de Bienvenida
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.welcome_label = ctk.CTkLabel(self.main_frame, text="Bienvenido al Sistema de Gestión", font=("Arial", 24))
        self.welcome_label.pack(pady=30)

        # Elementos de estadísticas (se crean una sola vez)
        self.stats_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 16), justify="left")
        self.stats_label.pack(pady=20)
        
        self.btn_refresh = ctk.CTkButton(self.main_frame, text="Actualizar Datos", command=self.update_stats_display)
        self.btn_refresh.pack()

        self.update_stats_display()

    def update_stats_display(self):
        stats = get_summary_stats()
        stats_text = f"Resumen Actual:\n\n👥 Pacientes: {stats['pacientes']}\n👨‍⚕️ Doctores: {stats['doctores']}\n📅 Citas: {stats['citas']}"
        self.stats_label.configure(text=stats_text)

    def manage(self, title, table, fields):
        GenericManager(self, title, table, fields)

    def open_dashboard(self):
        if show_patient_distribution is not None:
            # Determinamos el criterio según la opción seleccionada en el menú
            criteria = "gender" if self.stats_option.get() == "Género" else "allergy"
            try:
                show_patient_distribution(criteria)
            except Exception as e:
                print(f"Error al ejecutar el dashboard: {e}")
        else:
            print("Error: La función 'show_patient_distribution' no está disponible. Revisa 'modules/dashboard.py'.")

    def open_simulation_window(self):
        simulation_win = SimulationWindow(self)
        simulation_win.start_simulation(num_patients=7) # Puedes ajustar el número de pacientes aquí

if __name__ == "__main__":
    try:
        print("Iniciando aplicación...")
        app = HospitalApp()
        app.mainloop()
    except Exception as e:
        print(f"OCURRIÓ UN ERROR CRÍTICO: {e}")
        # Esto evita que la ventana de la terminal se cierre si hay un error
        input("Presiona Enter para salir...")