import os # Importa el módulo 'os' para funciones relacionadas con el sistema operativo
import pygame

# Clase Texture para cargar y gestionar las texturas del juego.
class Texture:
    texture_dict = {}  # Diccionario para almacenar las texturas cargadas
    path = None  # Ruta del directorio de las texturas

    # Inicializa la clase Texture con la ruta del directorio de las texturas.
    def __init__(self, path):
        self.path = path

    # Obtiene la textura con la clave especificada.
    def get_texture(self, key, reverse=False):
        # Si la textura no está en el diccionario
        if (key, reverse) not in self.texture_dict:
            image_path = self.path + "/" + key + ".png"  # Construye la ruta completa del archivo de imagen
            # Si el archivo de imagen existe
            if os.path.isfile(self.path + "/" + key + ".png"):
                p = pygame.image.load(image_path)  # Carga la imagen
                s = p if not reverse else pygame.transform.flip(p, True, False)  # Invierte la imagen si se especifica
                self.texture_dict[(key, reverse)] = s  # Almacena la textura en el diccionario
            else:
                return None  # Devuelve None si no se encontró la imagen
        # Si la textura ya está en el diccionario, devuélvela
        return self.texture_dict[(key, reverse)]
