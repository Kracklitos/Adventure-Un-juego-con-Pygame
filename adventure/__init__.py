import json  # Importa el módulo 'json' para trabajar con archivos JSON
import random  # Importa el módulo 'random' para generar números aleatorios
import pygame  
import os  
from adventure import clock  
from adventure import camera  
from adventure import texture  
from adventure import character  
from bintrees import rbtree  # Importa el módulo 'rbtree' para trabajar con árboles binarios

# Define la bandera para el modo de pantalla completa
FULL_SCREEN_FLAG = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

# Define el color de fondo
BGCOLOR = (54, 143, 203)  # Azul claro

# Define la gravedad
GRAVITY = 800  # Valor de la gravedad

# Clase principal para gestionar el juego
class Adventure:

    initialized = False  # Bandera para indicar si el juego se ha inicializado
    ready = False  # Bandera para indicar si el juego está listo para comenzar

    window_width = 0  # Ancho de la ventana
    window_height = 0  # Alto de la ventana
    canvas_width = 0  # Ancho del canvas
    canvas_height = 0  # Alto del canvas

    screen = None  # Superficie de la pantalla
    font = None  # Fuente del texto
    clock = None  # Objeto 'GameClock' para controlar el tiempo
    level = None  # Nivel actual del juego
    canvas = None  # Superficie del canvas
    ui = None  # Superficie de la interfaz de usuario
    draw_ui = False  # Bandera para indicar si se debe dibujar la interfaz de usuario

    delay = 0  # Retardo para la animación

    done = False  # Bandera para indicar si el juego ha terminado

    scale = 1  # Escala del canvas
    camera = None  # Objeto 'Camera' actual
    default_camera = None  # Objeto 'Camera' por defecto
    debug_camera = None  # Objeto 'Camera' para debug

    world_col = 64  # Número de columnas del mundo
    world_row = 64  # Número de filas del mundo
    block_size = 32  # Tamaño de cada bloque

    debug = False  # Bandera para indicar si se está en modo debug

    world = None  # Matriz que representa el mundo
    blocks = None  # Diccionario que almacena los tipos de bloques

    texture = texture.Texture("res/texture")  # Objeto 'Texture' para cargar las texturas

    start_point = None  # Punto de inicio del personaje

    # Variables temporales para pruebas
    # ------------------------------
    dir = 0  # Dirección del personaje
    background = []  # Lista de elementos de fondo
    camera_background = []  # Lista de elementos de fondo para la cámara

    ch = None  # Objeto 'Character' del personaje

    # Inicializa el juego con las configuraciones del archivo JSON.
    def init(self, config_obj):

        # Si el juego no se ha inicializado
        if not self.initialized:
            # Si el sistema operativo es Windows, ajusta el DPI
            if os.name == 'nt':
                import ctypes  # Importa el módulo 'ctypes' para funciones relacionadas con la API de Windows
                ctypes.windll.user32.SetProcessDPIAware()  # Ajusta el DPI para que coincida con la configuración del sistema

            # Configuraciones de la ventana
            # ---------------------------------------------------------------------
            window_config = config_obj["window"]  # Obtiene la configuración de la ventana
            full_screen = window_config["fullScreen"]  # Obtiene la configuración de pantalla completa
            window_width = window_config["width"] if full_screen else window_config["width"]  # Obtiene el ancho de la ventana
            window_height = window_config["height"] if full_screen else window_config["height"]  # Obtiene el alto de la ventana
            window_flag = FULL_SCREEN_FLAG if full_screen else 0  # Define la bandera para la ventana

            # Configuraciones de la fuente
            # ---------------------------------------------------------------------
            font_config = config_obj["font"]  # Obtiene la configuración de la fuente
            font_family = font_config["family"]  # Obtiene la familia de la fuente
            font_size = font_config["size"]  # Obtiene el tamaño de la fuente

            # Configuraciones del reloj
            # ---------------------------------------------------------------------
            max_fps = config_obj['fps']  # Obtiene el máximo FPS
            self.clock = clock.GameClock(max_fps)  # Crea un objeto 'GameClock'

            # Interfaz de usuario
            # ---------------------------------------------------------------------
            self.ui = pygame.Surface((window_width, window_height))  # Crea la superficie para la interfaz de usuario

            # Nivel
            # ---------------------------------------------------------------------
            self.level = config_obj['mainLevel']  # Obtiene el nivel principal

            # Inicializa Pygame
            pygame.init()

            # Inicializa el módulo de fuentes
            pygame.font.init()

            # Crea la ventana
            self.screen = pygame.display.set_mode((window_width, window_height), window_flag)
            self.window_width, self.window_height = self.screen.get_size()  # Obtiene el ancho y alto de la ventana

            # Inicializa la fuente
            self.font = pygame.font.SysFont(font_family, font_size)

            # Carga el nivel
            self.load_level(self.level)
            self.initialized = True  # Marca el juego como inicializado
            self.dir = 4  # Inicializa la dirección del personaje