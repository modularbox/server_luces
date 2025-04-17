import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from custom_logger import CustomLogger
from your_dmx_control_module import ciclo_luces, off_all_channels  # importa tus funciones

# Ruta del archivo JSON con los canales
JSON_PATH = "config/canales_dmx.json"
logger = CustomLogger()
estado_actual = []  # Guardamos el estado actual para detectar cambios


def cargar_configuracion():
    try:
        with open(JSON_PATH, 'r') as file:
            data = json.load(file)
            return data.get("canales", [])
    except Exception as e:
        logger.log_error(f"Error al leer el archivo JSON: {e}")
        return []


def actualizar_luces_si_hay_cambios():
    global estado_actual
    nuevos_canales = cargar_configuracion()
    if nuevos_canales != estado_actual:
        logger.log_info("Cambio detectado en la configuración de canales DMX")
        estado_actual = nuevos_canales
        off_all_channels()
        ciclo_luces(nuevos_canales)
    else:
        logger.log_info("No hay cambios en los canales. No se actualiza nada.")


class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("canales_dmx.json"):
            actualizar_luces_si_hay_cambios()


def iniciar_watcher():
    event_handler = ConfigFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path="config", recursive=False)
    observer.start()
    logger.log_info("🔍 Watcher iniciado. Esperando cambios en el JSON de canales...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    # Cargar configuración inicial
    actualizar_luces_si_hay_cambios()
    iniciar_watcher()
