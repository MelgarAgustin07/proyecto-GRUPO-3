import tkinter as tk
from tkinter import messagebox
import random
import os

def main(ventana_principal, funcion_actualizar_records):
    
    ventana_records_abierta = False

    def cerrar_aplicacion():
        ventana.destroy()
        ventana_principal.deiconify()

    def manejar_click(index):
        nonlocal bloqueado
        if bloqueado or botones[index]['state'] == 'disabled':
            return

        boton = botones[index]
        boton.config(image=imagenes_duplicadas[index])
        boton['state'] = 'disabled'

        seleccionados.append((index, imagenes_duplicadas[index]))

        if len(seleccionados) == 2:
            button1, img1 = seleccionados[0]
            button2, img2 = seleccionados[1]

            if img1 == img2:
                seleccionados.clear()
                contar_par()
            else:
                bloqueado = True
                ventana.after(300, lambda: ocultar_no_coincidentes(button1, button2))

    def ocultar_no_coincidentes(button1, button2):
        nonlocal bloqueado
        botones[button1].config(image=imagen_reverso, state='normal')
        botones[button2].config(image=imagen_reverso, state='normal')
        valor_actual = contador_monvimientos_var.get()
        valor_actual += 1 
        contador_monvimientos_var.set(valor_actual)     
        seleccionados.clear()
        bloqueado = False

    def contar_par():
        nonlocal pares_encontrados
        pares_encontrados += 1
        if pares_encontrados == 4:
            mensaje_ganador()

    def mensaje_ganador():
        nonlocal contador_monvimientos_var
        movimientos = contador_monvimientos_var.get()
        
        if funcion_actualizar_records("facil", movimientos):
            msg = f'¡Felicidades! ¡NUEVO RÉCORD con {movimientos} movimientos!'
        else:
            msg = f'¡Ganaste con {movimientos} movimientos!'
            
        messagebox.showinfo('¡Juego Terminado!', msg)
        ventana.destroy()
        ventana_principal.deiconify()

    def mostrar_records_juego():
        nonlocal ventana_records_abierta
        
        if ventana_records_abierta:
            messagebox.showwarning("Atención", "La ventana de récords ya está abierta.")
            return

        puntajes = ventana_principal.RECORDS_GLOBALES["facil"] 
        
        ventana_records = tk.Toplevel(ventana)
        ventana_records.title('Top 3 Récords - Fácil')
        ventana_records.geometry('300x200')
        ventana_records.resizable(False, False)
        ventana_records.transient(ventana)

        def cerrar_records_juego():
            nonlocal ventana_records_abierta
            ventana_records_abierta = False
            ventana_records.destroy()

        ventana_records.protocol("WM_DELETE_WINDOW", cerrar_records_juego)
        ventana_records_abierta = True
        
        tk.Label(ventana_records, text="Mejores Movimientos (Fácil)", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        if puntajes:
            for i, puntaje in enumerate(puntajes):
                tk.Label(ventana_records, text=f"#{i+1}: {puntaje} movimientos", font=('Arial', 12)).pack(pady=2)
        else:
            tk.Label(ventana_records, text="No hay récords aún.", font=('Arial', 12)).pack(pady=5)
            
    ventana = tk.Toplevel()
    ventana.title('Juego de Memoria')
    ventana.geometry('600x400')
    ventana.resizable(False, False) 
    ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

    contador_monvimientos_var = tk.IntVar()
    contador_monvimientos_var.set(0)
    
    frame_superior = tk.Frame(ventana)
    frame_superior.pack(pady=10)
    
    etiqueta_movimientos = tk.Label(frame_superior, 
                                    textvariable=contador_monvimientos_var, 
                                    font=('Times New Roman', 16))
    etiqueta_movimientos.pack(side=tk.LEFT, padx=20)
    
    btn_records = tk.Button(frame_superior, text="Ver Récords", 
                            command=mostrar_records_juego)
    btn_records.pack(side=tk.RIGHT, padx=20)

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=20)

    Imagenes = [
    os.path.join(ruta_imagenes, "amd.png"),
    os.path.join(ruta_imagenes, "basedatos.png"),
    os.path.join(ruta_imagenes, "binario.png"),
    os.path.join(ruta_imagenes, "c++.png"),
    os.path.join(ruta_imagenes, "code.png"),
    os.path.join(ruta_imagenes, "computadora.png"),
    os.path.join(ruta_imagenes, "html.png"),
    os.path.join(ruta_imagenes, "intel.png"),
    os.path.join(ruta_imagenes, "javas.png"),
    os.path.join(ruta_imagenes, "python.png"),]

    imagen_reverso = tk.PhotoImage(file=os.path.join(ruta_imagenes, "reverso.png"))

    imagenes_seleccionadas = random.sample(Imagenes, 4)
    imagenes_tk = [tk.PhotoImage(file=img) for img in imagenes_seleccionadas]
    imagenes_duplicadas = imagenes_tk * 2
    random.shuffle(imagenes_duplicadas)

    botones = []
    seleccionados = []
    bloqueado = False
    pares_encontrados = 0

    for i in range(8):
        boton = tk.Button(frame_botones, image=imagen_reverso,
                          command=lambda i=i: manejar_click(i))
        boton.grid(row=i//4, column=i%4, padx=10, pady=10)
        botones.append(boton)

    ventana.imagenes_tk = imagenes_duplicadas
    ventana.imagen_reverso = imagen_reverso
    
    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

if __name__ == "__main__":
    main()