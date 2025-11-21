import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # <-- NECESARIO: Importamos PIL para manejar PNG/JPG
import Memoria_Facil
import Memoria_Medio
import Memoria_Dificil
import os

# --- CONSTANTES ---
COLOR_FONDO = "#2c3e50"
COLOR_BOTON_NORMAL = "#3498db"
COLOR_BOTON_RECORDS = "#e67e22"
COLOR_TEXTO_CLARO = "white"
COLOR_TEXTO_OSCURO = "#2c3e50"
FUENTE_TITULO = ('Helvetica', 18, 'bold')
FUENTE_BOTON = ('Helvetica', 12, 'bold')
ANCHO_VENTANA = 350 
ALTO_VENTANA = 500 

# --- FUNCIONES ---

def actualizar_records(nivel, movimientos):
    
    RECORDS_GLOBALES = ventana_principal.RECORDS_GLOBALES 
    
    if movimientos <= 0:
        return False
    
    RECORDS_GLOBALES[nivel].append(movimientos)
    RECORDS_GLOBALES[nivel].sort() 
    RECORDS_GLOBALES[nivel] = RECORDS_GLOBALES[nivel][:3]
    
    return movimientos in RECORDS_GLOBALES[nivel]


def cerrar_aplicacion():
    ventana_principal.destroy()


def abrir_memoria_facil():
    ventana_principal.withdraw() 
    Memoria_Facil.main(ventana_principal, actualizar_records) 

def abrir_memoria_medio():
    ventana_principal.withdraw() 
    Memoria_Medio.main(ventana_principal, actualizar_records) 


def abrir_memoria_dificil():
    ventana_principal.withdraw() 
    Memoria_Dificil.main(ventana_principal, actualizar_records) 

# --- CONFIGURACIÓN DE VENTANA ---

ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

ventana_principal = tk.Tk()
ventana_principal.title('Juego de Memoria')
ventana_principal.geometry(f'{ANCHO_VENTANA}x{ALTO_VENTANA}') # Uso de f-string para tamaño
ventana_principal.resizable(False, False)
ventana_principal.configure(bg=COLOR_FONDO)

global img_fondo_principal # Se declara global para evitar que Python la borre (Garbage Collector)

try:
    ruta_fondo_principal = os.path.join(ruta_imagenes, "imagen_fondo.png")
    
    # 1. Carga la imagen usando PIL/Pillow y la redimensiona
    # Nota: Asegúrate de tener una imagen llamada 'imagen_fondo.png' en la carpeta 'imagenes'.
    img_pil = Image.open(ruta_fondo_principal)
    img_redimensionada = img_pil.resize((ANCHO_VENTANA, ALTO_VENTANA), Image.LANCZOS)
    img_fondo_principal = ImageTk.PhotoImage(img_redimensionada) 

    # 2. Creamos un Canvas para colocar la imagen de fondo y los widgets encima
    canvas = tk.Canvas(ventana_principal, width=ANCHO_VENTANA, height=ALTO_VENTANA)
    canvas.pack(fill="both", expand=True) 
    canvas.create_image(0, 0, image=img_fondo_principal, anchor="nw") 
    
    contenedor_widgets = canvas # Los widgets se colocarán en el Canvas
    
except Exception as e: # Captura cualquier error de archivo o PIL
    print(f"Error cargando imagen de fondo: {e}. Usando color de fondo estático.")
    ventana_principal.configure(bg=COLOR_FONDO)
    contenedor_widgets = ventana_principal # Los widgets irán sobre la ventana principal si falla

# Lógica del Icono
try:
    img_icon = tk.PhotoImage(file=os.path.join(ruta_imagenes, "icono.png"))
    ventana_principal.iconphoto(True, img_icon)
except tk.TclError:
    pass

# Inicialización de RECORDS_GLOBALES
ventana_principal.RECORDS_GLOBALES = { 
    "facil": [],
    "medio": [],
    "dificil": []
}

# --- WIDGETS ---

# Título
etiqueta = tk.Label(contenedor_widgets, text='🧠 Selecciona la Dificultad', 
font=FUENTE_TITULO, 
bg='black' if contenedor_widgets != ventana_principal else COLOR_FONDO, # Fondo oscuro si está sobre Canvas
fg=COLOR_TEXTO_CLARO)

# Colocación de Widgets
centro_x = ANCHO_VENTANA / 2 
current_y = 50 # Posición Y del título (ajustada para Canvas)

# Función auxiliar para colocar los botones. Usa pack o create_window.
def colocar_widget(widget, y_pos=None):
    if contenedor_widgets == ventana_principal:
        widget.pack(pady=10 if isinstance(widget, tk.Button) else 30)
    else:
        contenedor_widgets.create_window(centro_x, y_pos, window=widget)


# Colocación del Título
colocar_widget(etiqueta, y_pos=current_y)
current_y += 60

# Función auxiliar para crear botones
def crear_boton(texto, comando):
    return tk.Button(contenedor_widgets, 
                     text=texto, 
                     command=comando,
                     font=FUENTE_BOTON, 
                     bg=COLOR_BOTON_NORMAL, 
                     fg=COLOR_TEXTO_CLARO, 
                     width=20, 
                     relief=tk.RIDGE,
                     bd=3)

# Botones de Dificultad
btn_facil = crear_boton(texto='⭐ Fácil (4 Pares)', comando=abrir_memoria_facil)
colocar_widget(btn_facil, y_pos=current_y)
current_y += 60

btn_normal = crear_boton(texto='🌟 Medio (8 Pares)', comando=abrir_memoria_medio)
colocar_widget(btn_normal, y_pos=current_y)
current_y += 60

btn_dificil = crear_boton(texto='👑 Difícil (12 Pares)', comando=abrir_memoria_dificil)
colocar_widget(btn_dificil, y_pos=current_y)
current_y += 60

# Botón de Récords
btn_records = crear_boton(texto='🏆 Ver Récords', comando=lambda: messagebox.showinfo("Récords", "Función pendiente."))
btn_records.config(bg=COLOR_BOTON_RECORDS)
colocar_widget(btn_records, y_pos=current_y + 30)
current_y += 90

# Botón Salir
btn_salir = crear_boton(texto='❌ Salir', comando=cerrar_aplicacion)
btn_salir.config(bg='#FF0000', fg='white')
colocar_widget(btn_salir, y_pos=current_y + 30)


# --- FINALIZACIÓN DEL PROGRAMA ---
ventana_principal.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
ventana_principal.mainloop()