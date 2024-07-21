import pygame
import adventure # Importa el módulo 'adventure'

# Define las direcciones de movimiento del personaje como listas de coordenadas
LEFT_BLOCK = [[1, 0]]  # Mover a la izquierda
RIGHT_BLOCK = [[-1, 0]] # Mover a la derecha
TOP_BLOCK = [[0, 1]]   # Mover hacia arriba
BOTTOM_BLOCK = [[0, -1]] # Mover hacia abajo

# Combina todas las direcciones en una sola lista
ALL_BLOCK = LEFT_BLOCK + RIGHT_BLOCK + TOP_BLOCK + BOTTOM_BLOCK

# Define los nombres de las animaciones del personaje
SPRITE_FALL = "fall"  # Animación de caída
SPRITE_JUMP = "jump"  # Animación de salto
SPRITE_DJUMP = "djump" # Animación de doble salto
SPRITE_IDLE = "idle"  # Animación de inactividad
SPRITE_RUN = "run"   # Animación de carrera

# Define las velocidades y la potencia de salto
MOV_SPEED = 320  # Velocidad de movimiento horizontal
JUMP_POWER = 380  # Potencia del salto normal
DJUMP_POWER = 280 # Potencia del doble salto


class Character:
    # Atributos del personaje
    w = 0  # Ancho del personaje
    h = 0  # Alto del personaje

    x = 0  # Posición x del personaje
    y = 0  # Posición y del personaje

    vx = 0  # Velocidad horizontal del personaje
    vy = 0  # Velocidad vertical del personaje

    status = None  # Estado actual del personaje (idle, run, jump, etc.)
    sprite = None  # Nombre del sprite actual del personaje
    delay  = 0  # Retardo para la animación del personaje

    target = None  # Bloque objetivo del personaje (para detectar colisiones)
    last_y = -99999999  # Última posición y del personaje (para detectar colisiones)
    last_blocks = None  # Últimos bloques que se comprobaron (para optimizar las colisiones)
    last_test   = None  # Última dirección de movimiento (para optimizar las colisiones)

    djump = True  # Indica si el personaje puede realizar un doble salto

    # Inicializa el personaje con las dimensiones y la posición iniciales
    def __init__(self, x, y, w, h):
        self.x = x  # Asigna la posición x inicial
        self.y = y  # Asigna la posición y inicial
        self.w = w  # Asigna el ancho del personaje
        self.h = h  # Asigna el alto del personaje
        #self.status = StatusIdle()  # Inicializa el estado del personaje como 'idle'
        self.sprite = SPRITE_IDLE  # Inicializa el sprite del personaje como 'idle'
        self.last_test = LEFT_BLOCK  # Inicializa la última dirección de movimiento como 'LEFT_BLOCK'