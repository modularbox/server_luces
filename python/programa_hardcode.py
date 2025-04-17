from custom_logger import CustomLogger
from guardar_configuracion import GuardarConfiguracion
class ProgramaHardcode():
    def __init__(self, lugar):
        super().__init__()
        self.lugar = lugar

    def guardar_luces(self, request):
        GuardarConfiguracion(self.lugar).guardar_datos_en_json(request)

    def get_luces_lugar(self):
        # Crear una instancia del logger
        logger = CustomLogger()
        # Crear una instancia del logger
        guardar_configuracion = GuardarConfiguracion(lugar=self.lugar)
        logger.log_info('Configuracion {}'.format(self.lugar))
        return guardar_configuracion.crear_archivo()