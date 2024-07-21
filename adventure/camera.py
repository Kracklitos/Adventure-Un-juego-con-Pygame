import pygame


CAMERA_GIRD_COLOR = (0, 0, 150) # Define el color de la cuadrícula de la cámara


class Camera:
    # Inicialización de variables de la clase
    pos = None  # Posición actual de la cámara (x, y)
    scale = 1  # Escala de la cámara (1 es tamaño normal, 2 es el doble de tamaño, etc.)
    window = None  # Superficie de la ventana del juego (ancho, alto)
    canvas = None  # Superficie principal donde se dibuja el juego (ancho, alto)
    width = 0  # Ancho de la cámara en píxeles
    height = 0  # Alto de la cámara en píxeles
    surface = None  # Superficie de la cámara (se usa para dibujar el contenido del juego)

    rect = None  # Rectángulo que representa el área visible de la cámara
    offset_x = 0  # Desplazamiento horizontal de la cámara
    offset_y = 0  # Desplazamiento vertical de la cámara
    block_size = 0  # Tamaño de cada bloque en la cuadrícula del juego


    # Inicializa la cámara con la escala, posición, tamaño de ventana, canvas y tamaño de bloque.
    def __init__(self, scale, pos, window, canvas, block_size):
        self.scale = scale  # Asigna la escala a la cámara
        px, py = pos  # Desempaqueta las coordenadas de la posición
        self.pos = {'x': px, 'y': py}  # Asigna las coordenadas x e y a la posición
        self.window = window  # Asigna la superficie de la ventana
        self.canvas = canvas  # Asigna la superficie del canvas
        self.block_size = block_size  # Asigna el tamaño de bloque
        self.set_scale(scale)   # Configura la escala inicial de la cámara

    # Establece la escala de la cámara.
    def set_scale(self, scale):
        if scale < 0.01:
            return
        w, h = self.window # Obtiene el ancho y alto de la ventana
        self.width  = (w * scale);  # Calcula el ancho de la cámara
        self.height = (h * scale);  # Calcula el alto de la cámara
        self.scale = scale  # Asigna la escala a la cámara
        self.surface = pygame.Surface((self.width, self.height))
        self.update_camera_rect()  # Actualiza el rectángulo de la cámara
        self.update_offset()  # Actualiza el desplazamiento de la cámara

    # Actualiza el desplazamiento de la cámara.
    def update_offset(self):
        cw, ch = self.canvas  # Obtiene el ancho y alto del canvas
        ww, wh = self.window  # Obtiene el ancho y alto de la ventana
        rect = self.rect;  # Obtiene el rectángulo de la cámara

        # Calcula el desplazamiento horizontal
        if rect.w > ww or rect.w >= cw:
            self.offset_x = round(max((ww - (rect.w / self.scale)) / 2, 0))
        else:
            self.offset_x = 0

        # Calcula el desplazamiento vertical
        if rect.h > wh or rect.h >= ch:
            self.offset_y = round(max((wh - (rect.h / self.scale)) / 2, 0))
        else:
            self.offset_y = 0

    # Actualiza el rectángulo de la cámara.
    def update_camera_rect(self):
        pos = self.pos  # Obtiene la posición actual de la cámara
        w, h = self.canvas  # Obtiene el ancho y alto del canvas
        temp_x = (pos['x'] - (self.width / 2))  # Calcula la posición x del rectángulo
        temp_y = (pos['y'] - (self.height / 2)) # Calcula la posición y del rectángulo
        rect_x = temp_x
        rect_y = temp_y

        # Ajusta las posiciones para que la cámara no se salga del canvas
        if temp_x < 0 or temp_x > (w - self.width):
            rect_x = 0 if temp_x < 0 else max(w - self.width, 0)

        if temp_y < 0 or temp_y > (h - self.height):
            rect_y = 0 if temp_y < 0 else max(h - self.height, 0)

        # Calcula el ancho y alto del rectángulo
        rect_w = w if self.width > w else self.width
        rect_h = h if self.height > h else self.height

        self.rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)

    # Obtiene las coordenadas del punto donde se encuentra el ratón.
    def get_mouse_hover_point(self):
        block_size = self.block_size
        mx, my = pygame.mouse.get_pos();
        scaled_size = block_size / self.scale
        bx = int(((mx - self.offset_x) + self.rect.x / self.scale) / scaled_size)
        by = int(((my - self.offset_y) + self.rect.y / self.scale) / scaled_size)
        return bx, by

    # Obtiene el bloque de la cámara.
    def get_camere_block(self):
        block_size = self.block_size
        x = int(self.rect.x / block_size)
        y = int(self.rect.y / block_size)
        c_w = (self.rect.x + self.rect.w)
        c_h = (self.rect.y + self.rect.h)
        c_w1 = int(c_w / block_size) - x
        c_h1 = int(c_h / block_size) - y
        w = c_w1 + 1 if ((c_w1 % block_size) != 0) else c_w1
        h = c_h1 + 1 if ((c_h1 % block_size) != 0) else c_h1
        return x - 1, y - 1, w + 1, h + 1

    # Dibuja la cuadrícula de la cámara en el canvas.
    def draw_camera_gird(self, canvas):
        block_size = self.block_size
        x, y, w, h = self.get_camere_block()
        for i in range(0, w + 1):  # Itera sobre el ancho del bloque de la cámara
            offset = x + i  # Calcula la coordenada x de la línea
            pygame.draw.line(canvas, CAMERA_GIRD_COLOR, (offset * block_size, y * block_size),
                             (offset * block_size, (y + h) * block_size), 1)  # Dibuja una línea vertical
        for i in range(0, h + 1):  # Itera sobre el alto del bloque de la cámara
            offset = y + i  # Calcula la coordenada y de la línea
            pygame.draw.line(canvas, CAMERA_GIRD_COLOR, (x * block_size, offset * block_size),
                             ((x + w) * block_size, offset * block_size), 1)  # Dibuja una línea horizontal
