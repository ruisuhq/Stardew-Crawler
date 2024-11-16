import requests, json, re
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

    # Precio de venta
    precio_venta_row = soup.find("td", {"style": "padding: 0; border: 0;", "colspan": "2"})
    if precio_venta_row:
        # Si encontramos el precio en el primer caso, buscamos la tabla interna
        table_info = precio_venta_row.find("table", {"class": "no-wrap", "style": "text-align: left; margin: 0; padding: 0; border-spacing: 0; border: 0;"})
        
        if table_info:
            # Intentamos extraer el precio de la tabla
            precio_venta = table_info.find_next("tbody")
            if precio_venta:
                # Si encontramos el cuerpo, extraemos y asignamos el precio
                datos["precio_venta"] = precio_venta.text.strip().split()[0]
            else:
                datos["precio_venta"] = "N/A"
        else:
            datos["precio_venta"] = "N/A"
    else:
        # Si no encontramos el precio de la primera forma, intentamos buscarlo en otro lugar
        sell_price_td = soup.find("td", string="Sell Price")
        if sell_price_td:
            price_table = sell_price_td.find_next("td")
            
            if price_table:
                # Buscamos la tabla donde puede estar el precio
                body = price_table.find("tbody")
                if body:
                    # Obtenemos la primera fila de la tabla
                    first_tr = body.find("tr")
                    if first_tr:
                        td_elements = first_tr.find_all("td")
                        if len(td_elements) > 1:
                            price = td_elements[1].get_text(strip=True)
                            datos["precio_venta"] = price
        else:
            datos["precio_venta"] = "N/A"

 
    # Precio de compra (Enlace a las semillas)
    seedrow = soup.find("td", {"id": "infoboxsection"}, string="Seed")
    if seedrow:
        seed_cell = seedrow.find_next_sibling("td", {"id": "infoboxdetail"})
        seed_link = seed_cell.find("a", href=True) if seed_cell else None
        if seed_link:
            datos["precio_semillas"] = obtener_datos_semillas(seed_link['href'])
        else:
            datos["precio_semillas"] = "N/A"
    else:
        datos["precio_semillas"] = "N/A"
    return datos

def obtener_datos_semillas(url):
    """
    Extrae el precio de compra de las semillas desde su página específica.
    Valida que el precio sea un número seguido de 'g' para evitar errores.
    """
    response = requests.get(f"{BASE_URL}{url}")
    soup = BeautifulSoup(response.content, "html.parser")

    # Buscar todas las celdas con clase "no-wrap"
    precios = soup.find_all("span", class_="no-wrap")
    if len(precios) > 1:  # Verificar si hay al menos dos precios
        precio = precios[1].text.strip()

        # Validar formato del precio (número seguido de 'g')
        if re.match(r"^\d+g$", precio):
            return precio
        else:
            return "N/A"
    elif precios:
        # Validar el primero si no hay suficientes elementos
        precio = precios[0].text.strip()
        if re.match(r"^\d+g$", precio):
            return precio
        else:
            return "N/A"
    return "N/A"

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