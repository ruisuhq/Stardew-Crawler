import requests, json
from bs4 import BeautifulSoup
from crop import Crop

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
        "cantidad_cosechable": "1",
        "Recrecimiento": "0",
        "precio_venta": "50g",
        "precio_semillas": "30g"
        },

    """

    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.content, "html.parser")
    data = {}

    crop = Crop()

    data["name"] = crop.get_name(soup)
    data["description"] = crop.get_description(soup)
    data["season"] = crop.get_season(soup)
    data["growth_time"] = crop.get_growth_time(soup)
    data["harvest_quantity"] = crop.get_harvest_quantity(soup)
    data["regrowth_days"] = crop.get_regrowth_days(soup)
    data["sell_price"] = crop.get_sell_price(soup)
    data["price_seed"] = crop.get_price_seed(get_link_seeds(soup))
    
    return data

def get_link_seeds(soup):
    seedrow = soup.find("td", {"id": "infoboxsection"}, string="Seed")
    if seedrow:
        seed_cell = seedrow.find_next_sibling("td", {"id": "infoboxdetail"})
        seed_link = seed_cell.find("a", href=True) if seed_cell else None
    else:
        return "N/A"

    return seed_link['href']

def exportJson(datos_cultivos):
    with open("cultivos.json", "w", encoding="utf-8") as f:
            json.dump(datos_cultivos, f, ensure_ascii=False, indent=4)
    print("Datos exportados a cultivos.json")

def StardewCrawler():
    cultivos = obtener_enlaces_cultivos(START_URL)
    datos_cultivos = []

    print("Cultivos encontrados:")
    for cultivo in cultivos:
        print(f"- {cultivo['nombre']}: {BASE_URL}{cultivo['enlace']}")
        try:
            datos_cultivo = obtener_datos_cultivo(cultivo["enlace"])
            datos_cultivos.append(datos_cultivo)
        except Exception as e:
            # Me da tok ver que hay errores q no son errores mb 
            # print(f"Error procesando {cultivo['nombre']}: {e}")
            datos_cultivos.append({"name": cultivo['nombre']})
        
    # Exportar los datos como JSON
    exportJson(datos_cultivos)