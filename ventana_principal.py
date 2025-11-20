import tkinter as tk
import Memoria_Facil
import Memoria_Medio
import Memoria_Dificil


def actualizar_records(nivel, movimientos):
    
    RECORDS_GLOBALES = ventana_principal.RECORDS_GLOBALES 
    
    RECORDS_GLOBALES[nivel].append(movimientos)
    RECORDS_GLOBALES[nivel].sort() 
    RECORDS_GLOBALES[nivel] = RECORDS_GLOBALES[nivel][:3]
    
    return movimientos in RECORDS_GLOBALES[nivel]


def mostrar_top_3(nivel):
    
    puntajes = ventana_principal.RECORDS_GLOBALES.get(nivel, [])
    
    ventana_principal.withdraw()

    ventana_records = tk.Toplevel()
    ventana_records.title(f'Top 3 Récords - {nivel.capitalize()}')
    ventana_records.geometry('300x250')
    ventana_records.resizable(False, False)

    def cerrar_records():
        ventana_records.destroy()
        ventana_principal.deiconify()

    ventana_records.protocol("WM_DELETE_WINDOW", cerrar_records)
    
    tk.Label(ventana_records, text=f"Mejores Movimientos ({nivel.capitalize()})", 
             font=('Arial', 14, 'bold')).pack(pady=10)
    
    if puntajes:
        for i, puntaje in enumerate(puntajes):
            tk.Label(ventana_records, text=f"#{i+1}: {puntaje} movimientos", font=('Arial', 12)).pack(pady=2)
    else:
        tk.Label(ventana_records, text="No hay récords aún.", font=('Arial', 12)).pack(pady=5)
    
    btn_cerrar = tk.Button(ventana_records, text="Cerrar", 
                           command=cerrar_records)
    btn_cerrar.pack(pady=15)


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



ventana_principal = tk.Tk()
ventana_principal.title('Juego de Memoria')
ventana_principal.geometry('300x450') 
ventana_principal.resizable(False, False)

ventana_principal.RECORDS_GLOBALES = { 
    "facil": [],
    "medio": [],
    "dificil": []
}

etiqueta = tk.Label(ventana_principal, text='Elige una dificultad', font=('Times New Roman', 16))
etiqueta.pack(pady=20)


btn_facil = tk.Button(ventana_principal, text='Fácil', font=('Arial', 14), width=15,
                      command=abrir_memoria_facil) 
btn_facil.pack(pady=10)

btn_normal = tk.Button(ventana_principal, text='Medio', font=('Arial', 14), width=15,
                       command=abrir_memoria_medio) 
btn_normal.pack(pady=10)

btn_dificil = tk.Button(ventana_principal, text='Difícil', font=('Arial', 14), width=15,
                        command=abrir_memoria_dificil) 
btn_dificil.pack(pady=10)




def mostrar_top_3_selector():
   
    ventana_selector_records = tk.Toplevel(ventana_principal)
    ventana_selector_records.title('Selecciona Nivel de Récord')
    ventana_selector_records.geometry('250x250')
    ventana_selector_records.resizable(False, False)
    ventana_selector_records.transient(ventana_principal)
    
    ventana_principal.withdraw() 

    def abrir_record_y_cerrar_selector(nivel):
        ventana_selector_records.destroy()
        mostrar_top_3(nivel)

    def cerrar_selector():
        ventana_selector_records.destroy()
        ventana_principal.deiconify()
    
    ventana_selector_records.protocol("WM_DELETE_WINDOW", cerrar_selector)

    tk.Label(ventana_selector_records, text='Ver Top 3 de:', font=('Arial', 14)).pack(pady=15)

    tk.Button(ventana_selector_records, text='Fácil', width=10, 
              command=lambda: abrir_record_y_cerrar_selector("facil")).pack(pady=5)
    tk.Button(ventana_selector_records, text='Medio', width=10, 
              command=lambda: abrir_record_y_cerrar_selector("medio")).pack(pady=5)
    tk.Button(ventana_selector_records, text='Difícil', width=10, 
              command=lambda: abrir_record_y_cerrar_selector("dificil")).pack(pady=5)
    

ventana_principal.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
ventana_principal.mainloop()