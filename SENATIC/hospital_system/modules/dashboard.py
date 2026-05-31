import matplotlib.pyplot as plt
import pandas as pd
from database.connection import connect_db

def show_patient_distribution(criteria="gender"):
    """Muestra una gráfica interactiva donde cada paciente es una sección de la barra con su nombre al pasar el mouse."""
    conn = connect_db()
    if conn:
        try:
            label = "Género" if criteria == "gender" else "Alergia"
            # Obtenemos nombres y el criterio para construir las secciones individuales
            query = f"SELECT name, {criteria} FROM patients"
            df = pd.read_sql(query, conn)
            
            if not df.empty:
                df[criteria] = df[criteria].fillna("No especificado")
                fig, ax = plt.subplots(figsize=(10, 7))
                
                categories = df[criteria].unique()
                colors_palette = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f', '#9b59b6', '#1abc9c']
                rects_info = [] # Guardará tuplas (objeto_rectangulo, nombre_paciente)

                for i, cat in enumerate(categories):
                    cat_df = df[df[criteria] == cat]
                    cat_color = colors_palette[i % len(colors_palette)]
                    
                    bottom = 0
                    for _, row in cat_df.iterrows():
                        # Dibujamos cada paciente como un bloque de altura 1
                        rect = ax.bar(str(cat), 1, bottom=bottom, color=cat_color, 
                                      edgecolor='white', linewidth=0.7)[0]
                        rects_info.append((rect, row['name']))
                        bottom += 1
                
                ax.set_title(f"Estadísticas: Pacientes por {label}\n(Pasa el cursor sobre las secciones)", fontsize=14)
                plt.xlabel(label)
                plt.ylabel("Número de Pacientes")
                
                # Configuración del Tooltip (Anotación flotante)
                annot = ax.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="white", ec="gray", alpha=0.9),
                                    arrowprops=dict(arrowstyle="->"))
                annot.set_visible(False)

                def hover(event):
                    vis = annot.get_visible()
                    if event.inaxes == ax:
                        for rect, name in rects_info:
                            cont, _ = rect.contains(event)
                            if cont:
                                annot.xy = (rect.get_x() + rect.get_width()/2, rect.get_y() + rect.get_height()/2)
                                annot.set_text(f"Paciente: {name}")
                                annot.set_visible(True)
                                fig.canvas.draw_idle()
                                return
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

                fig.canvas.mpl_connect("motion_notify_event", hover)
                plt.tight_layout()
                plt.show()
            else:
                print("No hay datos de pacientes registrados para mostrar.")
        except Exception as e:
            print(f"Error al generar la gráfica interactiva: {e}")
        finally:
            conn.close()