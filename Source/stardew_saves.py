import os
import xml.etree.ElementTree as ET

APPDATA_DIR = os.getenv('APPDATA')
SAVES_DIR = fr"{APPDATA_DIR}\StardewValley\Saves"

def listSaves():
    folders = [folder for folder in os.listdir(SAVES_DIR) if os.path.isdir(os.path.join(SAVES_DIR, folder))]

    return folders;

def get_saves_data():
    values = []

    for saves in listSaves():
        raiz = cargar_datos_archivo(fr"{SAVES_DIR}\{saves}\{saves}")
        data = obtener_datos_jugador(raiz)
        values.append(data)

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
        "name": jugador.findtext("name"),
        "farm": jugador.findtext("farmName"),
        "current_season": raiz.findtext("currentSeason"),
        "day_month": raiz.findtext("dayOfMonth"),
        "year": raiz.findtext("year")
    }

def obtener_fecha_juego(raiz):
    return [raiz.findtext("currentSeason"), raiz.findtext("dayOfMonth"), raiz.findtext("year")]

def main():
    print(get_saves_data())

if __name__ == "__main__":
    main()