import customtkinter as ctk
from tkinter import messagebox
from modules.database_ops import get_all_records, insert_record

class GenericManager(ctk.CTkToplevel):
    """Ventana genérica para gestionar CRUD de cualquier tabla del sistema."""
    def __init__(self, master, title, table, fields):
        super().__init__(master)
        self.title(f"Gestión de {title}")
        self.geometry("700x600")
        self.table = table
        self.fields = fields # Lista de tuplas (Label, Columna_DB)
        
        # Configuración de grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(len(self.fields) + 2, weight=1)
        
        # Título del formulario
        ctk.CTkLabel(self, text=f"Registrar Nuevo {title}", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Generación dinámica de campos de entrada
        self.entries = {}
        for i, (label_text, db_col) in enumerate(self.fields):
            ctk.CTkLabel(self, text=label_text).grid(row=i+1, column=0, padx=20, pady=10, sticky="e")
            if db_col == "gender":
                entry = ctk.CTkOptionMenu(self, values=["Masculino", "Femenino", "Otro"], width=300)
                entry.set("Seleccione Género")
            else:
                entry = ctk.CTkEntry(self, width=300)
            
            entry.grid(row=i+1, column=1, padx=20, pady=10, sticky="w")
            self.entries[db_col] = entry
            
        # Botón Guardar
        self.btn_save = ctk.CTkButton(self, text="Guardar Registro", command=self.save_data, fg_color="#2ecc71")
        self.btn_save.grid(row=len(self.fields)+1, column=0, columnspan=2, pady=20)
        
        # Área de visualización de registros actuales
        self.view_area = ctk.CTkTextbox(self, height=200)
        self.view_area.grid(row=len(self.fields)+2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        self.refresh_view()

    def refresh_view(self):
        """Consulta la base de datos y actualiza la lista visual."""
        records = get_all_records(self.table)
        self.view_area.configure(state="normal")
        self.view_area.delete("1.0", "end")
        
        if records:
            header = " | ".join([col.upper() for col in records[0].keys()])
            self.view_area.insert("end", f"{header}\n" + "-"*80 + "\n")
            for r in records:
                line = " | ".join([str(v) for v in r.values()])
                self.view_area.insert("end", f"{line}\n")
        else:
            self.view_area.insert("end", "No hay registros disponibles.")
            
        self.view_area.configure(state="disabled")

    def save_data(self):
        """Extrae los datos de los campos y realiza la petición SQL."""
        data = {col: entry.get() for col, entry in self.entries.items()}
        
        # Validación simple
        if any(not str(val).strip() or val == "Seleccione Género" for val in data.values()):
            messagebox.showwarning("Atención", "Por favor completa todos los campos del formulario.")
            return
            
        if insert_record(self.table, data):
            messagebox.showinfo("Éxito", f"Registro en '{self.table}' guardado correctamente.")
            for entry in self.entries.values():
                if isinstance(entry, ctk.CTkEntry):
                    entry.delete(0, 'end')
                elif isinstance(entry, ctk.CTkOptionMenu):
                    entry.set("Seleccione Género")
            
            self.refresh_view()
            # Intentar actualizar el dashboard principal si está abierto
            if hasattr(self.master, 'update_stats_display'):
                self.master.update_stats_display()
        else:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos o hubo un error en la consulta.")