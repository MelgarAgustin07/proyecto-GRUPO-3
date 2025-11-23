import tkinter as tk
from tkinter import messagebox
import random
import os
import musica

COLOR_FONDO = "#34495e"
COLOR_SUPERIOR = "#2c3e50"
COLOR_BOTON_NORMAL = "#3498db"
COLOR_BOTON_RECORDS = "#e67e22"
COLOR_TEXTO_CLARO = "white"
FUENTE_MOVIMIENTOS = ('Courier New', 20, 'bold')
FUENTE_TITULO_RECORDS = ('Helvetica', 14, 'bold')
FUENTE_PUNTAJE_RECORDS = ('Helvetica', 12)


def main(ventana_principal, funcion_actualizar_records):
    musica.reproducir_medio()
    ventana_records_abierta = False


    def cerrar_aplicacion():
        musica.detener_musica()
        musica.reproducir_intro() 
        ventana.destroy()
        ventana_principal.deiconify()

    def manejar_click(index):
        nonlocal bloqueado
        if bloqueado or botones[index]['state'] == 'disabled':
            return

        boton = botones[index]
        boton.config(image=imagenes_duplicadas[index], highlightbackground=COLOR_BOTON_NORMAL)
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
                ventana.after(600, lambda: ocultar_no_coincidentes(button1, button2))

    def ocultar_no_coincidentes(button1, button2):
        nonlocal bloqueado
        botones[button1].config(image=imagen_reverso, state='normal', highlightbackground=COLOR_SUPERIOR)
        botones[button2].config(image=imagen_reverso, state='normal', highlightbackground=COLOR_SUPERIOR)
        
        valor_actual = contador_monvimientos_var.get()
        valor_actual += 1 
        contador_monvimientos_var.set(valor_actual)
        
        seleccionados.clear()
        bloqueado = False

    def contar_par():
        nonlocal pares_encontrados
        pares_encontrados += 1
        if pares_encontrados == 8: 
            mensaje_ganador()

    def mensaje_ganador():
        nonlocal contador_monvimientos_var
        movimientos = contador_monvimientos_var.get()
        
        if funcion_actualizar_records("medio", movimientos):
            msg = f'¡Felicidades! ¡NUEVO RÉCORD con {movimientos} movimientos!'
        else:
            msg = f'¡Ganaste con {movimientos} movimientos!'
            
        messagebox.showinfo('🎉 Juego Terminado!', msg)
        musica.detener_musica()
        musica.reproducir_intro() 
        ventana.destroy()
        ventana_principal.deiconify()
        
    def mostrar_records_juego():
        nonlocal ventana_records_abierta
        
        if ventana_records_abierta:
            messagebox.showwarning("Atención", "La ventana de récords ya está abierta.")
            return

        puntajes = ventana_principal.RECORDS_GLOBALES["medio"] 
        
        ventana_records = tk.Toplevel(ventana)
        ventana_records.title('🏆 Top 3 Récords - Medio')
        ventana_records.geometry('300x200')
        ventana_records.resizable(False, False)
        ventana_records.transient(ventana)
        ventana_records.configure(bg=COLOR_SUPERIOR)

        def cerrar_records_juego():
            nonlocal ventana_records_abierta
            ventana_records_abierta = False
            ventana_records.destroy()

        ventana_records.protocol("WM_DELETE_WINDOW", cerrar_records_juego)
        ventana_records_abierta = True
        
        tk.Label(ventana_records, text="🏅 Mejores Movimientos (Medio)", 
                 font=FUENTE_TITULO_RECORDS, bg=COLOR_SUPERIOR, fg=COLOR_TEXTO_CLARO).pack(pady=10)
        
        if puntajes:
            for i, puntaje in enumerate(puntajes):
                 color_rank = "#f1c40f" if i == 0 else ("#bdc3c7" if i == 1 else "#cd7f32")
                 tk.Label(ventana_records, text=f"#{i+1}: {puntaje} movimientos", 
                          font=FUENTE_PUNTAJE_RECORDS, bg=color_rank, fg='black', width=20, relief=tk.RIDGE).pack(pady=2)
        else:
            tk.Label(ventana_records, text="No hay récords aún.", font=FUENTE_PUNTAJE_RECORDS, bg=COLOR_SUPERIOR, fg=COLOR_TEXTO_CLARO).pack(pady=5)


    ventana = tk.Toplevel()
    ventana.title('Juego de Memoria - Medio')
    ventana.geometry('550x580')
    ventana.resizable(False, False) 
    ventana.configure(bg=COLOR_FONDO)
    ventana.configure(bg=COLOR_SUPERIOR)
    
    ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

    contador_monvimientos_var = tk.IntVar()
    contador_monvimientos_var.set(0)
    
    frame_superior = tk.Frame(ventana, bg=COLOR_SUPERIOR)
    frame_superior.pack(fill='x', pady=0)
    
    tk.Label(frame_superior, text="Movimientos: ", 
             bg=COLOR_SUPERIOR, 
             fg=COLOR_TEXTO_CLARO, 
             font=('Arial', 16)).pack(side=tk.LEFT, padx=(20, 5), pady=10)
    
    etiqueta_movimientos = tk.Label(frame_superior, 
                                    textvariable=contador_monvimientos_var, 
                                    font=FUENTE_MOVIMIENTOS,
                                    bg=COLOR_SUPERIOR,
                                    fg=COLOR_BOTON_NORMAL)
    etiqueta_movimientos.pack(side=tk.LEFT, padx=(0, 20), pady=10)
    
    btn_records = tk.Button(frame_superior, text="🏆 Ver Récords", 
                            command=mostrar_records_juego,
                            bg=COLOR_BOTON_RECORDS,
                            fg=COLOR_TEXTO_CLARO,
                            font=('Helvetica', 10, 'bold'),
                            relief=tk.FLAT)
    btn_records.pack(side=tk.RIGHT, padx=20, pady=10)
    
    frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_botones.pack(pady=25)

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
    os.path.join(ruta_imagenes, "python.png"),
    os.path.join(ruta_imagenes, "django.png"),
    os.path.join(ruta_imagenes, "ts.png"),]

    imagen_reverso = tk.PhotoImage(file=os.path.join(ruta_imagenes, "reverso.png"))

    imagenes_seleccionadas = random.sample(Imagenes, 8)
    imagenes_tk = [tk.PhotoImage(file=img) for img in imagenes_seleccionadas]
    imagenes_duplicadas = imagenes_tk * 2
    random.shuffle(imagenes_duplicadas)

    botones = []
    seleccionados = []
    bloqueado = False
    pares_encontrados = 0

    for i in range(16):
        boton = tk.Button(frame_botones, 
                          image=imagen_reverso,
                          bd=4,
                          relief=tk.RAISED,
                          highlightthickness=2,
                          highlightbackground=COLOR_SUPERIOR,
                          command=lambda i=i: manejar_click(i))
        boton.grid(row=i//4, column=i%4, padx=12, pady=12)
        botones.append(boton)

    ventana.imagenes_tk = imagenes_duplicadas
    ventana.imagen_reverso = imagen_reverso

    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)