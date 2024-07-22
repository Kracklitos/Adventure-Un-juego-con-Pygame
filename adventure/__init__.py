import json  # Importa el módulo 'json' para trabajar con archivos JSON
import random  # Importa el módulo 'random' para generar números aleatorios
import pygame  # Importa el módulo 'pygame' para funciones relacionadas con el juego
import os  # Importa el módulo 'os' para funciones relacionadas con el sistema operativo
from adventure import clock  # Importa la clase 'GameClock' del módulo 'adventure'
from adventure import camera  # Importa la clase 'Camera' del módulo 'adventure'
from adventure import texture  # Importa la clase 'Texture' del módulo 'adventure'
from adventure import character  # Importa la clase 'Character' del módulo 'adventure'
from bintrees import rbtree  # Importa el módulo 'rbtree' para trabajar con árboles binarios

# Define la bandera para el modo de pantalla completa
FULL_SCREEN_FLAG = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF

# Define el color de fondo
BGCOLOR = (54, 143, 203)  # Azul claro

# Define la gravedad
GRAVITY = 800  # Valor de la gravedad

class Adventure:
    """
    Clase principal para gestionar el juego.
    """

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

    def init(self, config_obj):
        """
        Inicializa el juego con las configuraciones del archivo JSON.

        Args:
            config_obj: Diccionario con las configuraciones del juego.
        """

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

    # Inicia el bucle principal del juego
    def start(self):
        self.clock.tick()  # Actualiza el reloj del juego
        while not self.done:  # Bucle principal del juego
            for event in pygame.event.get():  # Maneja los eventos del juego
                if event.type == pygame.QUIT:  # Si se presiona la tecla "X" de la ventana
                    self.done = True  # Marca el juego como terminado
                    continue  # Continúa con el bucle principal

                if event.type == pygame.KEYDOWN: # Si se presiona una tecla
                    if event.key == pygame.K_F8:  # Si se presiona F8
                        self.debug = not self.debug  # Activa/desactiva el modo de depuración
                        if self.debug:  # Si se activa el modo de depuración
                            self.camera = self.debug_camera  # Cambia a la cámara de depuración
                            self.camera.pos = self.default_camera.pos  # Restablece la posición de la cámara
                            self.camera.update_camera_rect()  # Actualiza el rectángulo de la cámara
                        else:
                            self.camera = self.default_camera  # Cambia a la cámara por defecto
                    if event.key == pygame.K_r:  # Si se presiona R
                        self.restart()  # Reinicia el juego
                        break  # Sale del bucle de eventos

                if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic en el ratón
                    if self.debug:  # Si se está en modo de depuración
                        if event.button == 4 or event.button == 5:  # Si se hace clic en la rueda del ratón
                            delta = -0.01 if event.button == 4 else 0.01  # Define el delta de escala
                            self.debug_camera.set_scale(self.debug_camera.scale + delta)  # Ajusta la escala de la cámara de depuración
                            self.screen.fill((0, 0, 0))  # Limpia la pantalla

            if not self.ready:  # Si el juego no está listo
                continue  # Continúa con el bucle principal
  

            vx = self.lerp(self.default_camera.pos['x'], self.ch.x, 10 * self.delay)  # Interpola la posición x de la cámara
            vy = self.lerp(self.default_camera.pos['y'], self.ch.y, 10 * self.delay)  # Interpola la posición y de la cámara

            self.default_camera.pos["x"] = vx  # Actualiza la posición x de la cámara
            self.default_camera.pos["y"] = vy  # Actualiza la posición y de la cámara
            self.default_camera.update_camera_rect()
            self.draw_camera_background()  # Dibuja el fondo de la cámara
            self.draw_blocks()  # Dibuja los bloques del nivel
            self.draw_background()  # Dibuja el fondo del juego
            self.ch.handle(pygame.key.get_pressed())  # Maneja las entradas del jugador
            self.ch.update(self.delay)  # Actualiza el personaje
            self.ch.draw(self.canvas)   # Dibuja el personaje en el canvas

            # ------ debug ------ #
            if self.debug:
                self.default_camera.draw_camera_gird(self.canvas)
                px, py = self.debug_camera.get_mouse_hover_point();
                pygame.draw.rect(self.canvas, (255, 0, 0),
                                 (px * self.block_size, py * self.block_size, self.block_size, self.block_size), 2)
                pygame.draw.rect(self.canvas, (0, 255, 0), self.default_camera.rect, 2)

            self.camera.surface.blit(self.canvas.subsurface(self.camera.rect), (0, 0))

            self.screen.blit(pygame.transform.smoothscale(self.camera.surface, (self.window_width, self.window_height)),
                             (self.camera.offset_x, self.camera.offset_y)) # Dibuja la superficie de la cámara en la pantalla, redimensionándola al tamaño de la ventana

            self.screen.blit(self.font.render(str(self.clock.get_fps()), True, (255, 0, 0)), (0, 0)) # Dibuja el FPS en la pantalla
            pygame.display.update()  # Actualiza la pantalla
            if self.camera.offset_x > 0 or self.camera.offset_y > 0:  # Si la cámara tiene un desplazamiento
                self.screen.fill((0, 0, 0))  # Limpia la pantalla
            pygame.draw.rect(self.canvas, BGCOLOR, self.default_camera.rect, 0)  # Dibuja el fondo del canvas
            self.delay = self.clock.tick()   # Actualiza el reloj del juego y obtiene el tiempo transcurrido

    # Carga el nivel del juego
    def load_level(self, level):
        level_file_name = "./level/" + level  # Construye la ruta del archivo del nivel
        level_file = open(level_file_name, "r")  # Abre el archivo del nivel en modo lectura
        level_obj = json.load(level_file)  # Carga el archivo JSON del nivel

        # Obtiene las propiedades del nivel desde el archivo JSON
        self.world_row = level_obj['worldRow']  # Número de filas del mundo
        self.world_col = level_obj['worldCol']  # Número de columnas del mundo
        self.block_size = level_obj['blockSize']  # Tamaño de los bloques
        self.scale = level_obj['scale']  # Escala del canvas

        # Crea la superficie del canvas con las dimensiones del mundo
        self.canvas = pygame.Surface(((self.world_col * self.block_size) + 1, (self.world_row * self.block_size) + 1))
        self.canvas_width, self.canvas_height = self.canvas.get_size()  # Obtiene el ancho y alto del canvas

        # Crea las cámaras por defecto y para debug
        self.default_camera = camera.Camera(self.scale,  # Crea la cámara por defecto
                                        (self.canvas_width, self.canvas_height),  # Tamaño del canvas
                                        (self.window_width, self.window_height),  # Tamaño de la ventana
                                        (self.canvas_width, self.canvas_height),  # Área visible del canvas
                                        self.block_size)  # Tamaño de los bloques
        self.debug_camera = camera.Camera(1,  # Crea la cámara para debug
                                      (self.canvas_width / 2, self.canvas_height),  # Tamaño del canvas para debug (mitad del ancho)
                                      (self.window_width, self.window_height),  # Tamaño de la ventana
                                      (self.canvas_width, self.canvas_height),  # Área visible del canvas
                                      self.block_size)  # Tamaño de los bloques

        # Inicializa la cámara actual con la cámara por defecto
        self.camera = self.default_camera
        self.camera.update_camera_rect()  # Actualiza el rectángulo de la cámara

        # Obtiene el punto de inicio del personaje
        self.start_point = level_obj["start"]
        # Crea el personaje en el punto de inicio
        self.ch = character.Character(self.start_point["x"], self.start_point["y"], 32, 32)

        # Posiciona la cámara en el punto de inicio del personaje
        self.default_camera.pos['x'] = self.ch.x
        self.default_camera.pos['y'] = self.ch.y

        # Inicializa las listas de elementos de fondo y el árbol binario para los bloques
        self.background = []
        self.camera_background = []
        self.world = rbtree.RBTree()  # Crea un árbol binario para almacenar los bloques del mundo
        self.blocks = level_obj["blocks"]  # Obtiene la información de los bloques del archivo JSON

        # Recorre los bloques y crea los objetos correspondientes
        index = 0
        for block in self.blocks:
            self.new_block(block, index)  # Crea un nuevo bloque
            index += 1

        # Marca el juego como listo
        self.ready = True

        # Carga el fondo de la cámara
        for bg in level_obj["camera_background"]:
            x = self.default_camera.rect.w * bg["x"]  # Calcula la posición x del elemento de fondo
            y = self.default_camera.rect.h * bg["y"]  # Calcula la posición y del elemento de fondo
            key = bg["key"]  # Obtiene la clave del elemento de fondo
            self.camera_background.append((x, y, key))  # Agrega el elemento de fondo a la lista

    # Crea un nuevo bloque en el mundo del juego.
    def new_block(self, block, block_id):

        x = block['x']  # Posición x del bloque
        y = block['y']  # Posición y del bloque
        w = block['w']  # Ancho del bloque
        h = block['h']  # Alto del bloque
        
        # Recorre las filas y columnas del bloque
        for row in range(0, h):
            for col in range(0, w):
                pos_y = y + row  # Posición y de la celda actual
                # Si la fila no existe en el árbol, crea una nueva fila
                if pos_y not in self.world:
                    self.world.insert(pos_y, rbtree.RBTree())  # Crea un nuevo árbol binario para la fila
                row_tree = self.world[pos_y]  # Obtiene el árbol de la fila actual
                pos_x = x + col  # Posición x de la celda actual
                row_tree.insert(pos_x, block_id)  # Inserta el ID del bloque en el árbol de la fila
                # Si el bloque tiene una configuración para generar objetos
                if "gen" in block:
                    obj = block["gen"]  # Obtiene la configuración de generación
                    prob = 0 if "prob" not in block else block["prob"]  # Obtiene la probabilidad de generación (0 si no está definida)
                    # Si se cumple la probabilidad de generación
                    if random.randint(0, 100) < prob:
                        index = random.randint(0, len(obj) - 1)  # Genera un índice aleatorio dentro de la lista de objetos
                        self.background.append((pos_x + obj[index]["x"], pos_y + obj[index]["y"], obj[index]["key"]))  # Agrega el objeto a la lista de elementos de fondo

    # Obtiene el ID del bloque en la posición especificada
    def get_block_id(self, x, y):
        result = None  # Inicializa el resultado a None
        if y in self.world:  # Si la fila existe en el árbol binario
            if x in self.world[y]:  # Si la columna existe en el árbol de la fila
                result = self.world[y][x]  # Obtiene el ID del bloque
        return result  # Devuelve el resultado

    # Dibuja los bloques del nivel en el canvas
    def draw_blocks(self):
        camera_block = pygame.Rect(self.default_camera.get_camere_block())
        for block in self.blocks:  # Recorre los bloques del nivel
            x = block['x']
            y = block['y']
            w = block['w']
            h = block['h']
            init_x = x * self.block_size
            init_y = y * self.block_size
            t = self.texture.get_texture(block["name"])  # Obtiene la textura del bloque
            if camera_block.colliderect((x, y, w, h)):  # Si el bloque está dentro del área visible de la cámara
                if block['draw'] == "fill":   # Si el bloque se dibuja completo
                    self.canvas.blit(t, (init_x, init_y))  # Dibuja la textura completa en el canvas
                elif block['draw'] == "repeat":   # Si el bloque se dibuja repetido
                    offset_y = 0  # Inicializa el desplazamiento vertical
                    while offset_y < h:  # Recorre las filas del bloque
                        offset_x = 0  # Inicializa el desplazamiento horizontal
                        while offset_x < w:  # Recorre las columnas del bloque
                            if camera_block.collidepoint(x + offset_x, y + offset_y):  # Si la celda actual está dentro del área visible de la cámara
                                pos_x = init_x + offset_x * self.block_size  # Calcula la posición x de la celda en el canvas
                                pos_y = init_y + offset_y * self.block_size  # Calcula la posición y de la celda en el canvas
                                self.canvas.blit(t, (pos_x, pos_y))  # Dibuja la textura en la celda actual
                            offset_x += 1  # Incrementa el desplazamiento horizontal
                        offset_y += 1  # Incrementa el desplazamiento vertical

    # Dibuja el fondo del juego en el canvas
    def draw_background(self):
        camera_block = pygame.Rect(self.default_camera.get_camere_block())  # Obtiene el rectángulo del área visible de la cámara
        for shit in self.background:  # Recorre los elementos de fondo
            x, y, key = shit  # Desempaqueta las coordenadas y la clave del elemento de fondo
            t = self.texture.get_texture(key)  # Obtiene la textura del elemento de fondo
            if camera_block.collidepoint(x, y):  # Si el elemento de fondo está dentro del área visible de la cámara
                self.canvas.blit(t, (x * self.block_size, (y * self.block_size)))  # Dibuja la textura en el canvas

    # Dibuja el fondo de la cámara en el canvas
    def draw_camera_background(self):
        for bg in self.camera_background:  # Recorre los elementos de fondo de la cámara
            x, y, key = bg  # Desempaqueta las coordenadas y la clave del elemento de fondo
            t = self.texture.get_texture(key)  # Obtiene la textura del elemento de fondo
            self.canvas.blit(t, (self.default_camera.rect.x + x, self.default_camera.rect.y + y))  # Dibuja la textura en el canvas

    # Calcula la interpolación lineal entre dos valores
    @staticmethod
    def lerp(v1, v2, f):
        return v1 + ((v2 - v1) * f)  # Fórmula de interpolación lineal

    # Reinicia el juego
    def restart(self):
        self.ch.x = self.start_point["x"]  # Restablece la posición x del personaje
        self.ch.y = self.start_point["y"]  # Restablece la posición y del personaje
        self.ch.vx = 0  # Restablece la velocidad x del personaje
        self.ch.vy = 0  # Restablece la velocidad y del personaje

# Crea un objeto de la clase Adventure
default = Adventure()
