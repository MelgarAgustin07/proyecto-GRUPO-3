import tkinter as tk
from tkinter import messagebox
import Memoria_Facil 
import os 
from PIL import Image, ImageTk 

# --- CONFIGURACIÓN DE ESTILO ---
# Colores usados en la interfaz para el diseño Neón/Futurista
COLOR_BOTON_NEON = '#00FFFF'     # Azul Cian Brillante
COLOR_TEXTO_BTN = '#000000'      # Texto Negro para alto contraste en botones
COLOR_FONDO_LABEL = '#000000'    # Fondo Negro para la etiqueta de título
COLOR_TEXTO_LABEL = 'white'      # Texto Blanco para la etiqueta de título

# --- FUNCIONES DE DIFICULTAD ---

def abrir_seleccion_memoria():
    global ventana_principal 
    # Oculta la ventana principal
    ventana_principal.withdraw() 
    abrir_seleccion_dificultad()

def abrir_seleccion_dificultad():
    seleccion = tk.Toplevel()
    seleccion.title('Selecciona Dificultad')
    
    # Medidas fijas para el menú de dificultad
    ANCHO_SELECCION = 300 
    ALTO_SELECCION = 400
    seleccion.geometry(f'{ANCHO_SELECCION}x{ALTO_SELECCION}')
    seleccion.resizable(False, False) 

    # LÓGICA DE IMAGEN DE FONDO PARA ESTA VENTANA (DIFICULTAD)
    try:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        
        # Carga y redimensiona la imagen de fondo_dificultad.png
        img_pil = Image.open(os.path.join(ruta_base, "imagenes", "fondo_dificultad.png"))
        img_redimensionada = img_pil.resize((ANCHO_SELECCION, ALTO_SELECCION), Image.LANCZOS)
        
        global img_fondo_dificultad 
        img_fondo_dificultad = ImageTk.PhotoImage(img_redimensionada) 
        
        # 1. Crea el Canvas y dibuja la imagen
        canvas = tk.Canvas(seleccion, width=ANCHO_SELECCION, height=ALTO_SELECCION)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=img_fondo_dificultad, anchor="nw")

        # 2. Coloca los widgets EN el canvas (usando la mitad del ancho, 150)
        
        # Etiqueta de Título con fuente Consolas
        etiqueta = tk.Label(canvas, text='Elige una dificultad', font=('Consolas', 18, 'bold'), 
                            bg=COLOR_FONDO_LABEL, fg=COLOR_TEXTO_LABEL)
        canvas.create_window(150, 40, window=etiqueta) 

        # Botones de dificultad con estilo Neón Cian y fuente Consolas
        
        # Botón Fácil
        btn_facil = tk.Button(canvas, 
                              text='Fácil (4 pares)', 
                              font=('Consolas', 14, 'bold'), 
                              width=15, 
                              command=lambda: [seleccion.destroy(), Memoria_Facil.main(ventana_principal, num_pares=4)],
                              bg=COLOR_BOTON_NEON,          
                              fg=COLOR_TEXTO_BTN,         
                              relief='flat',          
                              bd=0,                   
                              activebackground='#00CCCC', 
                              highlightthickness=0)
        canvas.create_window(150, 100, window=btn_facil) 
        
        # Botón Normal
        btn_normal = tk.Button(canvas, 
                               text='Normal (8 pares)', 
                               font=('Consolas', 14, 'bold'), 
                               width=15,
                               command=lambda: [seleccion.destroy(), Memoria_Facil.main(ventana_principal, num_pares=8)],
                               bg=COLOR_BOTON_NEON,          
                               fg=COLOR_TEXTO_BTN,         
                               relief='flat',          
                               bd=0,                   
                               activebackground='#00CCCC', 
                               highlightthickness=0)
        canvas.create_window(150, 160, window=btn_normal) 
        
        # Botón Difícil
        btn_dificil = tk.Button(canvas, 
                                text='Difícil (10 pares)', 
                                font=('Consolas', 14, 'bold'), 
                                width=15,
                                command=lambda: [seleccion.destroy(), Memoria_Facil.main(ventana_principal, num_pares=10)],
                                bg=COLOR_BOTON_NEON,          
                                fg=COLOR_TEXTO_BTN,         
                                relief='flat',          
                                bd=0,                   
                                activebackground='#00CCCC', 
                                highlightthickness=0)
        canvas.create_window(150, 220, window=btn_dificil) 

    except Exception as e:
        # Fallback si la imagen no carga
        print(f"Error cargando fondo de dificultad: {e}. Usando color de fondo.")
        seleccion.config(bg='lightgray') 
        # Fallback de botones (usando pack)
        etiqueta = tk.Label(seleccion, text='Elige una dificultad', font=('Times New Roman', 16), bg='lightgray')
        etiqueta.pack(pady=20)
        btn_facil = tk.Button(seleccion, text='Fácil (4 pares)', font=('Arial', 14),
                              command=lambda: [seleccion.destroy(), Memoria_Facil.main(ventana_principal, num_pares=4)])
        btn_facil.pack(pady=10)
        btn_normal = tk.Button(seleccion, text='Normal (8 pares)', font=('Arial', 14),
                               command=lambda: [seleccion.destroy(), Memoria_Facil.main(ventana_principal, num_pares=8)])
        btn_normal.pack()


# --- INICIO DEL PROGRAMA PRINCIPAL ---

ventana_principal = tk.Tk()
ventana_principal.title('Juegos')

# Medidas fijas para la ventana principal
ANCHO_VENTANA = 400
ALTO_VENTANA = 450
ventana_principal.geometry(f'{ANCHO_VENTANA}x{ALTO_VENTANA}') 
ventana_principal.resizable(False, False)

# LÓGICA DE IMAGEN DE FONDO PRINCIPAL Y ESCALAMIENTO
try:
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Cargar la imagen usando PIL
    img_pil = Image.open(os.path.join(ruta_base, "imagenes", "fondo_principal.png"))
    
    # 2. Redimensionar la imagen al tamaño de la ventana (400x450)
    img_redimensionada = img_pil.resize((ANCHO_VENTANA, ALTO_VENTANA), Image.LANCZOS)
    
    global img_fondo_principal
    img_fondo_principal = ImageTk.PhotoImage(img_redimensionada) 
    
    # 3. Crea el Canvas y dibuja la imagen
    canvas = tk.Canvas(ventana_principal, width=ANCHO_VENTANA, height=ALTO_VENTANA)
    canvas.pack(fill="both", expand=True) 
    canvas.create_image(0, 0, image=img_fondo_principal, anchor="nw") 

    # 4. Coloca los widgets EN el canvas, CENTRADOS (X=200)

    # Título (CON TIPOGRAFÍA FUTURISTA Y MAYOR TAMAÑO)
    titulo = tk.Label(canvas, text='Selecciona un juego', font=('Consolas', 22, 'bold'), 
                      bg=COLOR_FONDO_LABEL, fg=COLOR_TEXTO_LABEL) 
    canvas.create_window(ANCHO_VENTANA / 2, 40, window=titulo) 

    # Botón Juego de Memoria (CON ESTILO NEÓN CIAN)
    btn_memoria = tk.Button(canvas, 
                            text='Juego de Memoria', 
                            font=('Arial', 14, 'bold'), 
                            width=20, 
                            command=abrir_seleccion_memoria,
                            # --- ESTILO MODERNO NEÓN ---
                            bg=COLOR_BOTON_NEON,          
                            fg=COLOR_TEXTO_BTN,         
                            relief='flat',          
                            bd=0,                   
                            activebackground='#00CCCC', 
                            highlightthickness=0)   
    canvas.create_window(ANCHO_VENTANA / 2, 100, window=btn_memoria) 

    # Botón Juego 2 (CON ESTILO NEÓN CIAN)
    btn_otro_juego1 = tk.Button(canvas, 
                                text='Juego 2 (futuro)', 
                                state='disabled', 
                                font=('Arial', 14), 
                                width=20,
                                # --- ESTILO MODERNO NEÓN ---
                                bg=COLOR_BOTON_NEON,          
                                fg=COLOR_TEXTO_BTN,         
                                relief='flat',          
                                bd=0,                   
                                activebackground='#00CCCC', 
                                highlightthickness=0)
    canvas.create_window(ANCHO_VENTANA / 2, 160, window=btn_otro_juego1) 

    # Botón Juego 3 (CON ESTILO NEÓN CIAN)
    btn_otro_juego2 = tk.Button(canvas, 
                                text='Juego 3 (futuro)', 
                                state='disabled', 
                                font=('Arial', 14), 
                                width=20,
                                # --- ESTILO MODERNO NEÓN ---
                                bg=COLOR_BOTON_NEON,          
                                fg=COLOR_TEXTO_BTN,         
                                relief='flat',          
                                bd=0,                   
                                activebackground='#00CCCC', 
                                highlightthickness=0)
    canvas.create_window(ANCHO_VENTANA / 2, 220, window=btn_otro_juego2) 

except Exception as e:
    # Fallback si la imagen de fondo no carga (usa el color por defecto)
    print(f"Error cargando imagen de fondo: {e}. Usando diseño básico.")
    ventana_principal.config(bg='lightblue') 
    
    # Estilo básico para Fallback
    titulo = tk.Label(ventana_principal, text='Selecciona un juego', font=('Times New Roman', 18), bg='lightblue')
    titulo.pack(pady=10)
    btn_memoria = tk.Button(ventana_principal, text='Juego de Memoria', font=('Times New Roman', 14),
                            width=20, command=abrir_seleccion_memoria)
    btn_memoria.pack(pady=10)
    btn_otro_juego1 = tk.Button(ventana_principal, text='Juego 2 (futuro)', state='disabled', width=20)
    btn_otro_juego1.pack(pady=5)
    btn_otro_juego2 = tk.Button(ventana_principal, text='Juego 3 (futuro)', state='disabled', width=20)
    btn_otro_juego2.pack(pady=5)


ventana_principal.mainloop()