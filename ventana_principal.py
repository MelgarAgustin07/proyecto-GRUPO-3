import tkinter as tk
from tkinter import messagebox
import Memoria_Facil
import Memoria_Medio
import Memoria_Dificil



def cerrar_aplicacion():
    ventana_principal.destroy()


def abrir_memoria_facil():
    Memoria_Facil.main(ventana_principal)  

def abrir_memoria_medio():
    Memoria_Medio.main(ventana_principal)  



def abrir_memoria_dificil():
    Memoria_Dificil.main(ventana_principal)  

ventana_principal = tk.Tk()
ventana_principal.title('Juego de Memoria')
ventana_principal.geometry('300x400') 
ventana_principal.resizable(False, False)

etiqueta = tk.Label(ventana_principal, text='Elige una dificultad', font=('Times New Roman', 16))
etiqueta.pack(pady=40)

btn_facil = tk.Button(ventana_principal, text='Fácil', font=('Arial', 14), width=15,
                      command=abrir_memoria_facil)
btn_facil.pack(pady=10)

btn_normal = tk.Button(ventana_principal, text='Medio', font=('Arial', 14), width=15,
                       command=abrir_memoria_medio)
btn_normal.pack(pady=10)

btn_dificil = tk.Button(ventana_principal, text='Difícil', font=('Arial', 14), width=15,
                        command=abrir_memoria_dificil)
btn_dificil.pack(pady=10)

ventana_principal.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
ventana_principal.mainloop()