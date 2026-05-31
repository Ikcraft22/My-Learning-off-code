import customtkinter as ctk
import time
import random

class SimulationWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Simulación de Flujo Hospitalario")
        self.geometry("600x400")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Status label
        self.grid_rowconfigure(1, weight=1) # Queue display
        self.grid_rowconfigure(2, weight=0) # Progress label

        self.status_label = ctk.CTkLabel(self, text="Iniciando simulación...", font=("Arial", 16))
        self.status_label.grid(row=0, column=0, pady=10, sticky="ew")

        self.queue_frame = ctk.CTkFrame(self)
        self.queue_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.queue_frame.grid_columnconfigure(0, weight=1)
        self.queue_frame.grid_rowconfigure(1, weight=1) # Textbox for queue

        self.queue_title_label = ctk.CTkLabel(self.queue_frame, text="Cola de Pacientes:", font=("Arial", 14, "bold"))
        self.queue_title_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        self.queue_text = ctk.CTkTextbox(self.queue_frame, wrap="word", state="disabled", height=150)
        self.queue_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.progress_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.progress_label.grid(row=2, column=0, pady=5, sticky="ew")

        self.patients_to_simulate = 0
        self.current_queue = []
        self.processed_count = 0

    def _update_queue_display(self):
        self.queue_text.configure(state="normal")
        self.queue_text.delete("1.0", "end")
        if self.current_queue:
            for i, patient in enumerate(self.current_queue):
                self.queue_text.insert("end", f"{i+1}. {patient}\n")
        else:
            self.queue_text.insert("end", "Cola vacía.\n")
        self.queue_text.configure(state="disabled")

    def start_simulation(self, num_patients=5):
        # Listas para personalización
        nombres = [
            "Mariana", "Juan", "Carlos", "Elena", "Roberto", 
            "Lucía", "Diego", "Sofía", "Miguel", "Valentina",
            "Andrés", "Camila", "Javier", "Isabella", "Ricardo"
        ]
        emojis = ["🤒", "🤕", "🤢", "🚑", "🏥", "👤", "🚶", "🏃"]

        self.patients_to_simulate = num_patients
        
        # Creamos pacientes con nombres al azar y emojis
        self.current_queue = []
        for _ in range(self.patients_to_simulate):
            p_nombre = random.choice(nombres)
            p_emoji = random.choice(emojis)
            self.current_queue.append(f"{p_emoji} {p_nombre}")

        self.processed_count = 0
        self.status_label.configure(text="Iniciando simulación...")
        self._update_queue_display()
        self._process_next_patient()

    def _process_next_patient(self):
        if not self.current_queue:
            self.status_label.configure(text="--- Simulación finalizada ---")
            self.progress_label.configure(text=f"Total de pacientes procesados: {self.processed_count}")
            return

        patient = self.current_queue.pop(0)
        self.processed_count += 1
        self._update_queue_display()

        self.status_label.configure(text=f"[TRIAGE] Evaluando a {patient}...")
        self.progress_label.configure(text=f"Procesando {patient} ({self.processed_count}/{self.patients_to_simulate})")

        self.after(1000, lambda: self._assign_status(patient)) # Simula 1 segundo de triaje

    def _assign_status(self, patient):
        processing_time = random.uniform(1, 3)
        status = random.choice(["Urgencia", "Consulta General", "Prioritario"])
        self.status_label.configure(text=f"[ATENCIÓN] {patient} asignado a: {status}. Tiempo estimado: {processing_time:.2f}h")

        # Simula el tiempo de atención (convertido a milisegundos)
        self.after(int(processing_time * 1000), self._process_next_patient)