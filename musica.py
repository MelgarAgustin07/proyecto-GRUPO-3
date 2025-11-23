
import pygame
import os

pygame.mixer.init()

ruta_base = os.path.join(os.path.dirname(__file__), "canciones")

def _cargar_y_reproducir(nombre_archivo):
    ruta = os.path.join(ruta_base, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"⚠️ No se encontró la canción: {ruta}")
        return
    pygame.mixer.music.load(ruta)
    pygame.mixer.music.set_volume(0.15)  
    pygame.mixer.music.play(-1) 

def reproducir_intro():
    _cargar_y_reproducir("intro.mp3")

def reproducir_facil():
    _cargar_y_reproducir("facil.mp3")

def reproducir_medio():
    _cargar_y_reproducir("medio.mp3")

def reproducir_dificil():
    _cargar_y_reproducir("dificil.mp3")

def detener_musica():
    pygame.mixer.music.stop()
