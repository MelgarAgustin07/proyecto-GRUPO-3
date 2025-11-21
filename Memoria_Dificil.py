import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # <--- AGREGADO: Importación de PIL para imágenes de fondo
import random
import os

# --- CONSTANTES ---
COLOR_FONDO = "#34495e"
COLOR_SUPERIOR = "#2c3e50"
COLOR_BOTON_NORMAL = "#3498db"
COLOR_BOTON_RECORDS = "#e67e22"
COLOR_TEXTO_CLARO = "white"
FUENTE_MOVIMIENTOS = ('Courier New', 20, 'bold')
FUENTE_TITULO_RECORDS = ('Helvetica', 14, 'bold')
FUENTE_PUNTAJE_RECORDS = ('Helvetica', 12)

# Se mantienen tus dimensiones para la ventana
ANCHO_VENTANA = 550 
ALTO_VENTANA = 800

# Tu lógica de juego: 12 pares (24 cartas) en cuadrícula 4x6
TOTAL_PARES = 12
COLUMNAS = 4 # 4 columnas
FILAS = 6 # 6 filas

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
        if pares_encontrados == TOTAL_PARES: # <--- Usamos la constante TOTAL_PARES (12)
            mensaje_ganador()

    def mensaje_ganador():
        nonlocal contador_monvimientos_var
        movimientos = contador_monvimientos_var.get()
        
        if funcion_actualizar_records("dificil", movimientos):
            msg = f'¡Felicidades! ¡NUEVO RÉCORD con {movimientos} movimientos!'
        else:
            msg = f'¡Ganaste con {movimientos} movimientos!'
            
        messagebox.showinfo('🎉 Juego Terminado!', msg)
        ventana.destroy()
        ventana_principal.deiconify()
        
    def mostrar_records_juego():
        nonlocal ventana_records_abierta
        
        if ventana_records_abierta:
            messagebox.showwarning("Atención", "La ventana de récords ya está abierta.")
            return

        puntajes = ventana_principal.RECORDS_GLOBALES["dificil"] 
        
        ventana_records = tk.Toplevel(ventana)
        ventana_records.title('🏆 Top 3 Récords - Difícil')
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
        
        tk.Label(ventana_records, text="🏅 Mejores Movimientos (Difícil)", 
                 font=FUENTE_TITULO_RECORDS, bg=COLOR_SUPERIOR, fg=COLOR_TEXTO_CLARO).pack(pady=10)
        
        if puntajes:
            for i, puntaje in enumerate(puntajes):
                  color_rank = "#f1c40f" if i == 0 else ("#bdc3c7" if i == 1 else "#cd7f32")
                  tk.Label(ventana_records, text=f"#{i+1}: {puntaje} movimientos", 
                           font=FUENTE_PUNTAJE_RECORDS, bg=color_rank, fg='black', width=20, relief=tk.RIDGE).pack(pady=2)
        else:
            tk.Label(ventana_records, text="No hay récords aún.", font=FUENTE_PUNTAJE_RECORDS, bg=COLOR_SUPERIOR, fg=COLOR_TEXTO_CLARO).pack(pady=5)

    
    # --- CONFIGURACIÓN DE VENTANA Y FONDO ---
    
    # [1. INICIALIZACIÓN DE VARIABLES]
    canvas = None 
    
    # [2. CREACIÓN DE LA VENTANA]
    ventana = tk.Toplevel()
    ventana.title('Juego de Memoria - Difícil')
    ventana.geometry(f'{ANCHO_VENTANA}x{ALTO_VENTANA}') # <--- Usamos las constantes
    ventana.resizable(False, False) 
    
    # [3. INICIALIZACIÓN DE ATRIBUTO]
    ventana.img_fondo = None 
    
    ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")

    # LÓGICA DE IMAGEN DE FONDO
    try:
        # Usamos el nombre de imagen para el nivel Difícil
        ruta_fondo_dificil = os.path.join(ruta_imagenes, "imagen_dificil.png") 
        
        # Carga la imagen, redimensiona y guarda la referencia
        img_pil = Image.open(ruta_fondo_dificil)
        img_redimensionada = img_pil.resize((ANCHO_VENTANA, ALTO_VENTANA), Image.LANCZOS)
        ventana.img_fondo = ImageTk.PhotoImage(img_redimensionada) 

        # Creamos un Canvas y colocamos la imagen de fondo
        canvas = tk.Canvas(ventana, width=ANCHO_VENTANA, height=ALTO_VENTANA)
        canvas.pack(fill="both", expand=True) 
        canvas.create_image(0, 0, image=ventana.img_fondo, anchor="nw") 
        
        contenedor_widgets = canvas # Los frames irán sobre el Canvas
        
    except Exception as e:
        # Si la imagen falla, usamos el color de fondo y el contenedor normal
        print(f"Error cargando imagen de fondo: {e}. Usando color de fondo estático.")
        ventana.configure(bg=COLOR_FONDO)
        contenedor_widgets = ventana 
    # --- FIN DE CONFIGURACIÓN DE VENTANA Y FONDO ---

    # Posición para centrar los frames
    centro_x = ANCHO_VENTANA / 2
    # La posición Y se ajusta visualmente, ya que la ventana es de 800px de alto
    centro_y_botones_ajustado = 450 
    
    contador_monvimientos_var = tk.IntVar()
    contador_monvimientos_var.set(0)
    
    frame_superior = tk.Frame(contenedor_widgets, bg=COLOR_SUPERIOR)
    
    # Colocación del Frame Superior
    if contenedor_widgets == canvas:
        canvas.create_window(centro_x, 30, window=frame_superior) 
    else:
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

    frame_botones = tk.Frame(contenedor_widgets, bg=COLOR_FONDO)

    # Colocación del Frame de Botones
    if contenedor_widgets == canvas:
        canvas.create_window(centro_x, centro_y_botones_ajustado, window=frame_botones) 
    else:
        frame_botones.pack(pady=25)

    # La lista de Imágenes se mantiene igual
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

    # Seleccionamos 12 pares (TOTAL_PARES) de imágenes.
    imagenes_seleccionadas = random.sample(Imagenes, TOTAL_PARES)
    imagenes_tk = [tk.PhotoImage(file=img) for img in imagenes_seleccionadas]
    imagenes_duplicadas = imagenes_tk * 2
    random.shuffle(imagenes_duplicadas)

    botones = []
    seleccionados = []
    bloqueado = False
    pares_encontrados = 0

    # Recorremos 24 cartas (TOTAL_PARES * 2)
    for i in range(TOTAL_PARES * 2):
        boton = tk.Button(frame_botones, 
                          image=imagen_reverso,
                          bd=4,
                          relief=tk.RAISED,
                          highlightthickness=2,
                          highlightbackground=COLOR_SUPERIOR,
                          command=lambda i=i: manejar_click(i))
        # Usamos las constantes de COLUMNAS (4)
        boton.grid(row=i//COLUMNAS, column=i%COLUMNAS, padx=12, pady=12)
        botones.append(boton)

    ventana.imagenes_tk = imagenes_duplicadas
    ventana.imagen_reverso = imagen_reverso

    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)