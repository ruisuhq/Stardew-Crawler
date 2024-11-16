import requests, json
from bs4 import BeautifulSoup

BASE_URL = "https://stardewvalleywiki.com"
START_URL = "/Crops"

def obtener_enlaces_cultivos(url):
    """
    Función para obtener desde la página base, todos los cultivos de Stardew Valley y su enlace a su página directa

    Resultado:
    - Melon: https://stardewvalleywiki.com/Melon

    """
    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.content, "html.parser")
    
    cultivos = []
    # Busca los elementos <h3> con clase "mw-headline"
    for h3 in soup.find_all("h3"):
        span = h3.find("span", {"class": "mw-headline"})
        if span:
            enlaces = span.find_all("a", href=True)
            if len(enlaces) > 1:
                nombre = enlaces[1].text.strip()  # Extraer el texto del segundo <a>
                enlace = enlaces[1]['href']  # Obtener el atributo href del segundo <a>
                cultivos.append({"nombre": nombre, "enlace": enlace})
    return cultivos

def obtener_datos_cultivo(url):
    """
    Función para entrar en cada página de cultivo individualmente y extraer información 
    (Nombre, descripción, temporada, tiempo para crecer, precio de venta base y precio de compra de semillas en Pierre)

    Formto JSON final:
        {
        "nombre": "Blue Jazz",
        "descripcion": "The flower grows in a sphere to invite as many butterflies as possible.",
        "temporada": "Spring",
        "tiempo_crecer": "7 days",
        "precio_venta": "Tiller",
        "precio_compra": "N/A"
        },

    NOTA: Hay error en el precio de venta base y precio de compra de semilla de Pierre, WIP    

    """
    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.content, "html.parser")
    datos = {}

    # Nombre del cultivo
    datos["nombre"] = soup.find("h1", {"id": "firstHeading"}).text.strip()

    # Descripción
    descripcion = soup.find("td", {"id": "infoboxdetail", "style": "text-align: center; font-style: italic; padding-right: 3px;"})
    datos["descripcion"] = descripcion.text.strip() if descripcion else "N/A"

    # Temporada
    temporada = soup.find_all("td", {"id": "infoboxdetail"})
    datos["temporada"] = next(
        (item.text.strip() for item in temporada if any(season in item.text for season in ["Summer", "Spring", "Fall", "Winter"])),
        "N/A"
    )

    # Tiempo para crecer
    tiempo_crecer = soup.find("td", {"id": "infoboxdetail"}, string=lambda t: t and "days" in t)
    datos["tiempo_crecer"] = tiempo_crecer.text.strip() if tiempo_crecer else "N/A"

    # INTENTO DE PRECIO VENTA Y PRECIO COMPRA SEMILLAS

    """
    # Precio de venta
    precio_venta_row = soup.find("td", {"id": "infoboxsection"}, string="Base")
    if precio_venta_row:
        precio_venta = precio_venta_row.find_next("td").text.strip()
        datos["precio_venta"] = precio_venta.split()[0]  # Captura solo el número y la unidad (por ejemplo, "250g")
    else:
        datos["precio_venta"] = "N/A"

    # Precio de compra (Enlace a las semillas)
    semilla_link = soup.find("td", {"id": "infoboxdetail"}).find("a", href=True)
    if semilla_link:
        datos.update(obtener_datos_semillas(semilla_link['href']))
    else:
        datos["precio_compra"] = "N/A"
    """

    return datos

def obtener_datos_semillas(url):
    """
    Extrae el precio de compra de las semillas desde su página específica.
    """
    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar todos los spans que contengan el precio dentro de la clase "no-wrap"
    precios = soup.find("span", "style", "display: none;")
    precio_compra = precios.text.strip() if precios else "N/A"

    # Retornar el primero si existe, o "N/A" si no se encuentra
    return precio_compra

def main():
    cultivos = obtener_enlaces_cultivos(START_URL)
    datos_cultivos = []
    
    print("Cultivos encontrados:")
    for cultivo in cultivos:
        print(f"- {cultivo['nombre']}: {BASE_URL}{cultivo['enlace']}")
        try:
            datos_cultivo = obtener_datos_cultivo(cultivo["enlace"])
            datos_cultivos.append(datos_cultivo)
        except Exception as e:
            print(f"Error procesando {cultivo['nombre']}: {e}")
            datos_cultivos.append({"nombre": cultivo['nombre'], "error": str(e)})
        
    # Exportar los datos como JSON
    with open("cultivos.json", "w", encoding="utf-8") as f:
        json.dump(datos_cultivos, f, ensure_ascii=False, indent=4)
    print("Datos exportados a cultivos.json")

if __name__ == "__main__":
    main()