import tkinter as tk
from tkinter import messagebox
import random
import os


def main(ventana_principal):
   


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
        seleccionados.clear()
        bloqueado = False

    def contar_par():
        nonlocal pares_encontrados
        pares_encontrados += 1
        if pares_encontrados == 12:
            mensaje_ganador()

    def mensaje_ganador():
        messagebox.showinfo('¡Felicidades!', '¡Ganaste el nivel difícil!')
        ventana.destroy()
        ventana_principal.deiconify() 


    ventana = tk.Toplevel()
    ventana.title('Juego de Memoria')
    ventana.geometry('700x700')
    ventana.resizable(False, False) 
    ruta_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")



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
    os.path.join(ruta_imagenes, "python.png"),
    os.path.join(ruta_imagenes, "django.png"),
    os.path.join(ruta_imagenes, "ts.png"),]

    imagen_reverso = tk.PhotoImage(file=os.path.join(ruta_imagenes, "reverso.png"))

    imagenes_seleccionadas = random.sample(Imagenes, 12)
    imagenes_tk = [tk.PhotoImage(file=img) for img in imagenes_seleccionadas]
    imagenes_duplicadas = imagenes_tk * 2
    random.shuffle(imagenes_duplicadas)

    botones = []
    seleccionados = []
    bloqueado = False
    pares_encontrados = 0

    for i in range(24):
        boton = tk.Button(frame_botones, image=imagen_reverso,
                        command=lambda i=i: manejar_click(i))
        boton.grid(row=i//4, column=i%4, padx=10, pady=10)
        botones.append(boton)

    ventana.imagenes_tk = imagenes_duplicadas
    ventana.imagen_reverso = imagen_reverso

    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    ventana.mainloop()

if __name__ == "__main__":
    main()
