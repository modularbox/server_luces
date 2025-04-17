import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from custom_logger import CustomLogger
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Custom
from fixture_model import FixtureModel
from custom_logger import CustomLogger
# Crear una instancia del logger
logger = CustomLogger()
# Cargar luces desde JSON
# ------------------ Todo el codigo de las luces ------------------
try:
    dmx = OpenDMXController()
    # Big square fixture model
    bsq_fixture_model = FixtureModel("DRGBWSEP")
    custom_fixture = dmx.add_fixture(Custom,name="CustomFixture", start_channel=1, channels=500)
    bsq_fixture_model.setup_fixture(custom_fixture)
except Exception as e:
    print('error', e)

# Ruta del archivo JSON con los canales
JSON_PATH = "config/canales_dmx.json"
logger = CustomLogger()
estado_actual = []  # Guardamos el estado actual para detectar cambios

# Guardar configuraciones anteriores
guardar_configuracion_programa_por_tiempo_canales = []
guardar_configuracion_programa_canales = []
luces_encendidas = False
# Funciones para el control de los canales
def encender_luz(channel):
    # print("Se encendieron las luces")
    custom_fixture.dim(255, 0, channel - 1)
def encender_con_value_luz(value, channel):
    # print("Se encendieron las luces")
    custom_fixture.dim(value, 0, channel - 1)
def off_all_channels():
    logger.log_info("Apagar todos los canales")
    for i in range(500):
        custom_fixture.dim(0, 0, i)
def ciclo_luces(channels):
    print("Ciclo de luces")
    print(channels)
    for channel in channels:
        if isinstance(channel, list):
            encender_con_value_luz(channel[1], channel[0])
        else:
            encender_luz(channel)

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
