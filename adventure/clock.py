import timeit  # Importa el módulo 'timeit' para medir el tiempo
import time    # Importa el módulo 'time' para funciones relacionadas con el tiempo

# Clase GameClock para controlar el bucle de juego y el FPS.
class GameClock:

    # Inicializa el GameClock con el máximo FPS deseado.
    def __init__(self, max_fps):

        self.min_fps = 30  # Define el mínimo FPS aceptable (30 FPS)
        self.max_fps = max_fps if max_fps > self.min_fps else self.min_fps  # Ajusta el máximo FPS a 30 si es menor
        self.fps_cost_time = (1 / self.max_fps)  # Calcula el tiempo objetivo por frame
        self.start = 0  # Tiempo de inicio del último frame
        self.elapsed = 0  # Tiempo transcurrido desde el último frame
        self.delta_time = 0  # Tiempo transcurrido desde el último cálculo de FPS
        self.count_down = 0  # Contador de frames para calcular FPS
        self.fps = self.max_fps  # FPS actual

    # Actualiza el temporizador y ajusta la velocidad de frame.
    def tick(self):
        self.elapsed = (timeit.default_timer() - self.start)  # Calcula el tiempo transcurrido
        if self.elapsed >= self.fps_cost_time:  # Si el tiempo transcurrido es mayor o igual al tiempo objetivo
            sleep_time = 0  # No se necesita dormir
        else:
            sleep_time = self.fps_cost_time - self.elapsed  # Calcula el tiempo restante para dormir
        if sleep_time > 0:  # Si se necesita dormir
            GameClock.sleep(sleep_time)  # Llama al método estático 'sleep'
        self.elapsed += sleep_time  # Actualiza el tiempo transcurrido
        self.delta_time += self.elapsed  # Actualiza el tiempo total transcurrido
        if self.delta_time > 1.0:  # Si ha pasado un segundo o más
            self.delta_time = 0  # Reinicia el tiempo total transcurrido
            self.fps = self.count_down  # Actualiza los FPS
            self.count_down = 0  # Reinicia el contador de frames
        self.count_down += 1  # Incrementa el contador de frames
        self.start = timeit.default_timer()  # Actualiza el tiempo de inicio
        return self.elapsed  # Devuelve el tiempo transcurrido

    # Obtiene el FPS actual.
    def get_fps(self):
        return self.fps

    # Método estático para pausar la ejecución durante un tiempo específico.
    @staticmethod
    def sleep(delay_time):
        finish = time.perf_counter() + delay_time  # Calcula el tiempo de finalización
        while time.perf_counter() < finish:  # Espera hasta que llegue el tiempo de finalización
            pass
