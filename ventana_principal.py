import tkinter as tk
from tkinter import messagebox
import Memoria_Facil
import Memoria_Medio
import Memoria_Dificil
import os

COLOR_FONDO = "#2c3e50"
COLOR_BOTON_NORMAL = "#3498db"
COLOR_BOTON_RECORDS = "#e67e22"
COLOR_TEXTO_CLARO = "white"
COLOR_TEXTO_OSCURO = "#2c3e50"
FUENTE_TITULO = ('Helvetica', 18, 'bold')
FUENTE_BOTON = ('Helvetica', 12, 'bold')





def actualizar_records(nivel, movimientos):
    
    RECORDS_GLOBALES = ventana_principal.RECORDS_GLOBALES 
    
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


ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

ventana_principal = tk.Tk()
ventana_principal.title('Juego de Memoria')
ventana_principal.geometry('350x500')
ventana_principal.resizable(False, False)
ventana_principal.configure(bg=COLOR_FONDO)

try:
    ruta_fondo_principal = os.path.join(ruta_imagenes, "imagen_fondo.png")
    imagen_fondo_principal_obj = tk.PhotoImage(file=ruta_fondo_principal)
    ventana_principal.imagen_fondo_principal_ref = imagen_fondo_principal_obj

    label_fondo_principal = tk.Label(ventana_principal, image=imagen_fondo_principal_obj)
    label_fondo_principal.place(x=0, y=0, relwidth=1, relheight=1)
    
    contenedor_widgets = label_fondo_principal
    bg_widgets_color = label_fondo_principal['bg'] 
    
except tk.TclError:
    ventana_principal.configure(bg=COLOR_FONDO)
    contenedor_widgets = ventana_principal
    bg_widgets_color = COLOR_FONDO
try:
  
    img = tk.PhotoImage(file=os.path.join(ruta_imagenes, "icono.png"))
    ventana_principal.iconphoto(True, img)

except tk.TclError:
    pass


ventana_principal.RECORDS_GLOBALES = { 
    "facil": [],
    "medio": [],
    "dificil": []
}

etiqueta = tk.Label(ventana_principal, text='🧠 Selecciona la Dificultad', 
                    font=FUENTE_TITULO, 
                    bg=COLOR_FONDO, 
                    fg=COLOR_TEXTO_CLARO)
etiqueta.pack(pady=30)

btn_facil = tk.Button(ventana_principal, text='⭐ Fácil (4 Pares)', 
                      command=abrir_memoria_facil,
                      font=FUENTE_BOTON, 
                      bg=COLOR_BOTON_NORMAL, 
                      fg=COLOR_TEXTO_CLARO, 
                      width=20, 
                      relief=tk.RIDGE,
                      bd=3)
btn_facil.pack(pady=10)

btn_normal = tk.Button(ventana_principal, text='🌟 Medio (8 Pares)', 
                       command=abrir_memoria_medio,
                       font=FUENTE_BOTON, 
                       bg=COLOR_BOTON_NORMAL, 
                       fg=COLOR_TEXTO_CLARO, 
                       width=20,
                       relief=tk.RIDGE,
                       bd=3) 
btn_normal.pack(pady=10)

btn_dificil = tk.Button(ventana_principal, text='👑 Difícil (12 Pares)', 
                        command=abrir_memoria_dificil,
                        font=FUENTE_BOTON, 
                        bg=COLOR_BOTON_NORMAL, 
                        fg=COLOR_TEXTO_CLARO, 
                        width=20,
                        relief=tk.RIDGE,
                        bd=3) 
btn_dificil.pack(pady=10)




ventana_principal.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
ventana_principal.mainloop()