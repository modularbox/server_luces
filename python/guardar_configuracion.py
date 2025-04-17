import json
import os
from custom_logger import CustomLogger
# Crear una instancia del logger
logger = CustomLogger()
inicioProgram = False
# Colores
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
orange = [255, 170, 0]
purple = [170, 0, 255]
apagar = [0, 0, 0]
white = [255, 255, 255]

# Configuracion
class GuardarConfiguracion:
    def __init__(self, lugar):
        logger.log_info("La configuracion esta en color white cruzbendita 1")
        # channels = self.ermita(white)
        channels = self.ermita(red)
        logger.log_info(channels)
        self.lugar = lugar
        self.nombre_archivo = 'datos_guardados.json'
        self.hardcode_luces = {
            "ermita": {
                "horarios": [
                    {"horario_inicio": "12:00:00", "horario_fin": "23:59:00"},
                    {"horario_inicio": "00:00:00", "horario_fin": "05:00:00"}
                ],
                "modo": "automatico",
                "canales": channels
            }
        }

    def get_off_on_rgb(self, rgb, canal):
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        new_list = []
        new_canal = canal + 1
        
        if red == 255:
            new_list.append(new_canal)
        elif red != 0:
            new_list.append([new_canal, red])
        
        new_canal += 1
        if green == 255:
            new_list.append(new_canal)
        elif green != 0:
            new_list.append([new_canal, green])
        
        new_canal += 1
        if blue == 255:
            new_list.append(new_canal)
        elif blue != 0:
            new_list.append([new_canal, blue])
        
        return new_list


    def desaguadero(self, rgb):
        cont = 4
        new_list = [1, 2, 3, 4]
        for _ in range(4):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 5
        return new_list

    def ermita(self, rgb):
        cont = 10
        new_list = []
        for _ in range(4):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 10
        return new_list

    def cruz_bendita(self, rgb):
        cont = 1
        new_list = []
        for _ in range(5):
            new_list.append(cont)
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 8
        
        cont = 40
        for _ in range(4):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 4
        return new_list
    
    def campanario(self, rgb):
        return self.campanarioluces(rgb) + self.espiritusanto(rgb)

    def campanarioluces(self, rgb):
        cont = 0
        new_list = []
        for _ in range(3):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 8
        
        cont = 24
        for _ in range(5):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 5
        return new_list

    def espiritusanto(self, rgb):
        cont = 49
        new_list = []
        for _ in range(7):
            new_list.extend(self.get_off_on_rgb(rgb, cont))
            cont += 8
        return new_list

    def crear_archivo(self):
        try:
            print("Entro aqui")
            if inicioProgram:
                if os.path.exists(self.nombre_archivo):
                    with open(self.nombre_archivo, 'r') as archivo:
                        datos = json.load(archivo)
                        return datos
                else:
                    with open(self.nombre_archivo, 'w') as archivo:
                        json.dump(self.hardcode_luces.get(self.lugar), archivo)
                        return self.hardcode_luces.get(self.lugar)
            else:
                return self.hardcode_luces.get(self.lugar)
        except:
            return None

    def guardar_datos_en_json(self, nuevos_datos):
        try:
            with open(self.nombre_archivo, 'w') as archivoWrite:
                json.dump(nuevos_datos, archivoWrite)
        except Exception as e:
            print("Error al guardar datos en JSON:", e)


