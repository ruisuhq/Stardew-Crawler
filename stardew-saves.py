import os
import xml.etree.ElementTree as ET

APPDATA_DIR = os.getenv('APPDATA')
SAVES_DIR = fr"{APPDATA_DIR}\StardewValley\Saves"


def listSaves():
    folders = [folder for folder in os.listdir(SAVES_DIR) if os.path.isdir(os.path.join(SAVES_DIR, folder))]

    return folders;

def get_saves_name():
    values = [folder.split('_')[0] for folder in listSaves()]

    return values


def cargar_datos_archivo(ruta_archivo):
    """Carga y analiza un archivo XML."""
    try:
        tree = ET.parse(ruta_archivo)
        return tree.getroot()
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def obtener_datos_jugador(raiz):
    """Extrae información del jugador."""
    jugador = raiz.find("player")
    if jugador is None:
        return {}
    return {
        "nombre": jugador.findtext("name"),
        "dinero": jugador.findtext("money"),
        "género": jugador.findtext("Gender"),
        "granja": jugador.findtext("farmName"),
        "esposa": jugador.findtext("spouse"),
        "nivel_casa": jugador.findtext("houseUpgradeLevel"),
        "salud_maxima": jugador.findtext("maxHealth"),
        "nivel_mina": jugador.findtext("deepestMineLevel"),
    }

def obtener_fecha_juego(raiz):
    """Extrae la fecha actual en el juego."""
    return {
        "temporada_actual": raiz.findtext("currentSeason"),
        "día": raiz.findtext("dayOfMonth"),
        "año": raiz.findtext("year"),
    }

def main():
    ruta_archivo = "OT_378081712"  # Reemplaza con la ruta a tu archivo XML
    raiz = cargar_datos_archivo(fr"{SAVES_DIR}\{ruta_archivo}\{ruta_archivo}")
    if raiz is None:
        return
    
    # Extraer datos
    datos_jugador = obtener_datos_jugador(raiz)
    fecha_juego = obtener_fecha_juego(raiz)

    # Mostrar resultados
    print("Datos del jugador:")
    for clave, valor in datos_jugador.items():
        print(f"  {clave.capitalize()}: {valor}")

    print("\nFecha del juego:")
    for clave, valor in fecha_juego.items():
        print(f"  {clave.replace('_', ' ').capitalize()}: {valor}")
