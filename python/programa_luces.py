from datetime import datetime
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
def ciclo_luces():
    global guardar_configuracion_programa_canales
    luces = guardar_configuracion_programa_canales
    for channel in luces:
        if isinstance(channel, list):
            encender_con_value_luz(channel[1], channel[0])
        else:
            encender_luz(channel)
# ------------------ Aqui termina el codigo ------------------
# ------------------ Codigo para la programacion de las luces en horas ------------------
        
# Programa para ejecutar el programa por tiempo
def programa_por_tiempo(request):
    global guardar_configuracion_programa_por_tiempo_canales
    canales = request.get('canales')
    ejecutar_cliclo = False
    # Verificamos si la peticion es igual para que no se esten seteando los valores
    if canales != guardar_configuracion_programa_por_tiempo_canales:
        guardar_configuracion_programa_por_tiempo_canales = canales
        ejecutar_cliclo = True
    if ejecutar_cliclo:    
        ciclo_luces(canales)

# Función que comprueba si la hora actual está dentro del rango especificado
def verificar_hora(hora_inicio, hora_fin):
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()

    # Convertir la hora específica a un objeto datetime
    fecha_hora_inicio = datetime.strptime(hora_inicio, "%H:%M:%S")
    fecha_hora_fin = datetime.strptime(hora_fin, "%H:%M:%S")

    # Asignar una hora específica (por ejemplo, 15:30:00)
    fecha_inicio = fecha_hora_inicio.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    fecha_fin = fecha_hora_fin.replace(year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    
    logger.log_info(fecha_inicio <= fecha_actual <= fecha_fin)
    logger.log_info(f"fecha_inicio: {fecha_inicio}, fecha_actual: {fecha_actual}, fecha_fin: {fecha_fin}")
    logger.log_info(f"¿fecha_actual está entre fecha_inicio y fecha_fin?: {fecha_inicio <= fecha_actual <= fecha_fin}")
    # Esto es para que no se apage un minuto y se vuelva a encender
    if fecha_actual.hour == 23 and fecha_actual.minute == 59:
        return True
    if fecha_inicio <= fecha_actual <= fecha_fin: 
        return True
    return False
    
def verificar_horarios(horarios):
    if isinstance(horarios, list):
        for horario in horarios:
            if verificar_hora(horario.get('horario_inicio'), horario.get('horario_fin')):
                logger.log_info("Esta en horario")
                return True
        return False
# ------------------ Termina la programacion de las luces en horas ------------------

def get_light_state_from_api(data):
    global guardar_configuracion_programa_canales
    global luces_encendidas
    canales = data.get('canales')
    # Verificar el horario para encender las luces o apagarlas
    if verificar_horarios(data.get('horarios')):
        luces_encendidas = True 
    else:
        if luces_encendidas:
            guardar_configuracion_programa_canales = []
            luces_encendidas = False
            off_all_channels()
    if luces_encendidas:
        # Guardamos la configuracion anterior, para que los datos no se esten seteando una y otra vez
        if guardar_configuracion_programa_canales != canales:
            off_all_channels()
            guardar_configuracion_programa_canales = canales
            # Guardar las luces
            return True
        
    return False
    
# Iniciar el programa
def init_luces(request):
    logger.log_info("LLega a iniciar el programa")
    logger.log_info(f"Request: {request}")
    encender = get_light_state_from_api(request)
    if encender: 
        logger.log_info("---------------------- Encender luces -------------------")
        ciclo_luces()