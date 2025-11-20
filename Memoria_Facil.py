import tkinter as tk
import random
import time
from tkinter import messagebox
import os
from PIL import Image, ImageTk 

# --- VARIABLES GLOBALES DEL JUEGO ---
cartas_seleccionadas = []
primer_click = None
segundo_click = None
pares_encontrados = 0
juego_terminado = False
contador_intentos = 0
tiempo_inicio = 0

# --- CONFIGURACIÓN DE APARIENCIA ---
# (Puedes usar estas constantes para darles estilo a los botones de las cartas si quieres)
COLOR_FONDO_CARTA = 'lightblue' 
COLOR_TEXTO_CARTA = 'black'
COLOR_FONDO_SELECCION = 'yellow'

# --- LÓGICA DEL JUEGO ---

def verificar_par(ventana, etiquetas_cartas, parent_window):
    global cartas_seleccionadas, primer_click, segundo_click, pares_encontrados, contador_intentos

    # Deshabilita temporalmente los botones para que el usuario no haga más clics
    for etiqueta in etiquetas_cartas:
        etiqueta.config(state=tk.DISABLED)
    
    # Pausa para que el usuario vea la segunda carta
    ventana.update()
    time.sleep(0.7)
    
    # Comprobar si son un par
    if cartas_seleccionadas[0] == cartas_seleccionadas[1]:
        # ¡Es un par!
        primer_click.config(text=cartas_seleccionadas[0], bg='green', fg='white', relief=tk.SUNKEN)
        segundo_click.config(text=cartas_seleccionadas[1], bg='green', fg='white', relief=tk.SUNKEN)
        
        # Deshabilita permanentemente los botones de las cartas encontradas
        primer_click.config(state=tk.DISABLED)
        segundo_click.config(state=tk.DISABLED)
        
        pares_encontrados += 1
        contador_intentos += 1
        
        if pares_encontrados == len(etiquetas_cartas) // 2:
            finalizar_juego(ventana, parent_window)
    else:
        # No es un par. Voltear las cartas
        primer_click.config(text="?", bg=COLOR_FONDO_CARTA, relief=tk.RAISED)
        segundo_click.config(text="?", bg=COLOR_FONDO_CARTA, relief=tk.RAISED)
        contador_intentos += 1

    # Restablece el estado del juego para el siguiente intento
    cartas_seleccionadas = []
    primer_click = None
    segundo_click = None
    
    # Vuelve a habilitar las cartas que no han sido encontradas
    for etiqueta in etiquetas_cartas:
        if etiqueta['text'] == '?':
            etiqueta.config(state=tk.NORMAL)
            
    # Actualizar contador de intentos (si tienes una etiqueta para ello)
    # Por simplicidad, no se incluye el widget de contador aquí, pero se puede añadir fácilmente.

def click_carta(etiqueta, ventana, etiquetas_cartas, parent_window):
    global cartas_seleccionadas, primer_click, segundo_click
    
    if etiqueta['text'] == '?' and len(cartas_seleccionadas) < 2:
        # Muestra el valor de la carta
        valor = etiqueta.carta_valor
        etiqueta.config(text=valor, bg=COLOR_FONDO_SELECCION)
        
        cartas_seleccionadas.append(valor)
        
        if primer_click is None:
            primer_click = etiqueta
        elif segundo_click is None:
            segundo_click = etiqueta
            # Es el segundo clic, verificar si hay par
            verificar_par(ventana, etiquetas_cartas, parent_window)


def finalizar_juego(ventana, parent_window):
    global tiempo_inicio, contador_intentos
    tiempo_fin = time.time()
    tiempo_total = round(tiempo_fin - tiempo_inicio)
    
    mensaje = (f"¡Felicidades! Has ganado.\n"
               f"Intentos: {contador_intentos}\n"
               f"Tiempo total: {tiempo_total} segundos")
               
    messagebox.showinfo("Juego Terminado", mensaje)
    
    ventana.destroy()
    parent_window.deiconify() # Muestra la ventana principal de nuevo


def on_closing(ventana, parent_window):
    if messagebox.askokcancel("Salir", "¿Estás seguro que quieres salir del juego?"):
        ventana.destroy()
        parent_window.deiconify() # Muestra la ventana principal de nuevo


# --- FUNCIÓN PRINCIPAL DEL JUEGO ---

def main(parent_window, num_pares):
    global cartas_seleccionadas, pares_encontrados, primer_click, segundo_click, contador_intentos, tiempo_inicio
    
    # Restablecer variables globales
    cartas_seleccionadas = []
    pares_encontrados = 0
    primer_click = None
    segundo_click = None
    contador_intentos = 0
    tiempo_inicio = time.time()
    
    # 1. Configuración de la Ventana
    ventana = tk.Toplevel(parent_window)
    ventana.title("Juego de Memoria")
    ventana.protocol("WM_DELETE_WINDOW", lambda: on_closing(ventana, parent_window))
    
    # 2. Generar el Tablero
    
    # Definir valores de las cartas (letras o números)
    valores_cartas = [chr(65 + i) for i in range(num_pares)] * 2
    random.shuffle(valores_cartas)
    
    # Determinar el layout (ejemplo: si es 4 pares (8 cartas), será 2x4)
    if num_pares == 4:
        filas, cols = 2, 4
    elif num_pares == 8:
        filas, cols = 4, 4
    elif num_pares == 10:
        filas, cols = 4, 5
    else:
        filas, cols = 2, num_pares # Por si acaso
    
    etiquetas_cartas = []
    marco_tablero = tk.Frame(ventana, padx=10, pady=10)
    marco_tablero.pack(padx=10, pady=10)
    
    indice = 0
    for fila in range(filas):
        for col in range(cols):
            # Crea el botón/etiqueta de la carta
            etiqueta = tk.Button(marco_tablero, text="?", font=("Arial", 20), 
                                 width=4, height=2, bg=COLOR_FONDO_CARTA, 
                                 relief=tk.RAISED)
            
            # Asigna el valor real de la carta como un atributo personalizado
            etiqueta.carta_valor = valores_cartas[indice] 
            
            # Asigna la función de clic, pasándole la etiqueta actual
            etiqueta.config(command=lambda e=etiqueta: click_carta(e, ventana, etiquetas_cartas, parent_window))
            
            etiqueta.grid(row=fila, column=col, padx=5, pady=5)
            etiquetas_cartas.append(etiqueta)
            indice += 1

    # ⚠️ APLICACIÓN DE FONDO DE IMAGEN EN LA VENTANA DEL JUEGO ⚠️
    try:
        # 1. Forzamos a Tkinter a calcular el tamaño final de la ventana 
        #    (necesario para obtener el tamaño real del tablero)
        ventana.update_idletasks() 

        # Obtenemos las dimensiones actuales y dinámicas de la ventana
        ancho_juego = ventana.winfo_width()
        alto_juego = ventana.winfo_height()

        ruta_base = os.path.dirname(os.path.abspath(__file__))
        
        # Carga la imagen de fondo del juego (debe ser 'fondo_juego.png' en 'imagenes/')
        img_pil_juego = Image.open(os.path.join(ruta_base, "imagenes", "fondo_juego.png"))
        
        # Redimensionar la imagen al tamaño dinámico de la ventana
        img_redimensionada_juego = img_pil_juego.resize((ancho_juego, alto_juego), Image.LANCZOS)
        
        global img_fondo_juego 
        img_fondo_juego = ImageTk.PhotoImage(img_redimensionada_juego) 
        
        # 2. Crea el Canvas del mismo tamaño que la ventana del juego
        canvas_juego = tk.Canvas(ventana, width=ancho_juego, height=alto_juego)
        canvas_juego.place(x=0, y=0, relwidth=1, relheight=1) 

        # 3. Dibuja la imagen en el canvas
        canvas_juego.create_image(0, 0, image=img_fondo_juego, anchor="nw") 

        # 4. Eleva todos los widgets (marco_tablero, etc.) por encima del canvas
        #    para que el tablero sea visible sobre el fondo.
        for widget in ventana.winfo_children():
            if widget != canvas_juego:
                widget.lift() # tk.lift() eleva el widget a la parte superior de la pila
        
    except Exception as e:
        print(f"Error al aplicar fondo de juego: {e}. Usando color plano.")
        ventana.config(bg='darkgray')
        
    # 3. Iniciar el Loop de la Ventana
    ventana.mainloop()