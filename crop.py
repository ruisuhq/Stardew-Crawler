import requests, json, re
from bs4 import BeautifulSoup

BASE_URL = "https://stardewvalleywiki.com"

class Crop:
    def __init__(self, name="n/a", description="n/a", season="n/a", growth_time="n/a", harvest_quantity="1", regrowth_days="0", sell_price="n/a", seed_price="n/a"):
        self.name = name
        self.description = description
        self.season = season
        self.growth_time = growth_time
        self.harvest_quantity = harvest_quantity 
        self.regrowth_days = regrowth_days
        self.sell_price = sell_price
        self.seed_price = seed_price

    def get_name(self, soup):
        """Obtiene el nombre del cultivo desde un objeto BeautifulSoup."""
        self.name = soup.find("h1", {"id": "firstHeading"}).text.strip()  # Suponiendo que el nombre esté en h1 con id 'firstHeading'

        return self.name
    
    def get_description(self, soup):
        data = soup.find("td", {"id": "infoboxdetail", "style": "text-align: center; font-style: italic; padding-right: 3px;"})
        self.description = data.text.strip()

        return self.description
    
    def get_season(self, soup):
        temporada = soup.find_all("td", {"id": "infoboxdetail"})
        
        # Usamos next con un valor por defecto "N/A" si no se encuentra la temporada
        self.season = next(
            (item.text.strip() for item in temporada if item and any(season in item.text for season in ["Summer", "Spring", "Fall", "Winter"])),
            "N/A"
        )
        
        return self.season

    def get_growth_time(self, soup):
        data = soup.find("td", {"id": "infoboxdetail"}, string=lambda t: t and "days" in t)
        self.growth_time = data.text.strip()

        return self.growth_time;
    
    def get_harvest_quantity(self, soup):
        """
        Extrae la cantidad cosechable de un cultivo buscando en la sección con el ID "Stages".
        Si el número extraído supera 5, se asigna un valor predeterminado de "1".
        """
        # Busca el elemento con ID "Stages"
        stages_span = soup.find("span", {"id": "Stages"})

        # Verifica si existe la sección "Stages"
        if not stages_span:
            self.harvest_quantity = "1"  # Valor por defecto si no existe la sección
            return self.harvest_quantity

        # Encuentra el elemento <h2> que contiene el <span> y luego el siguiente <p>
        stages_h2 = stages_span.find_parent("h2")
        if stages_h2:
            next_paragraph = stages_h2.find_next_sibling("p")  # Encuentra el siguiente <p>
            if next_paragraph and next_paragraph.text:
                text = next_paragraph.text.strip()
                # Busca el primer número entero en el texto
                match = re.search(r"\b\d+\b", text)
                if match:
                    quantity = int(match.group())  # Convierte a entero
                    # Si el número es mayor a 5, asigna el valor predeterminado de "1"
                    self.harvest_quantity = str(quantity if quantity <= 5 else 1)
                    return self.harvest_quantity

        self.harvest_quantity = "1"  # Valor por defecto si no se encuentra un número
        return self.harvest_quantity
    
    def get_regrowth_days(self, soup):
        """
        Extrae el tiempo de recrecimiento desde la tabla que está después de la sección con el ID "Stages".
        Busca el tercer <tr> para localizar el valor de Regrowth: X Days.
        """
        # Busca el elemento con ID "Stages"
        stages_span = soup.find("span", {"id": "Stages"})

        # Verifica si existe la sección "Stages"
        if not stages_span:
            self.regrowth_days = "0"  # Valor por defecto si no existe la sección
            return self.regrowth_days

        # Encuentra el elemento <h2> que contiene el <span> y luego busca la siguiente tabla
        stages_h2 = stages_span.find_parent("h2")
        if stages_h2:
            # Busca la tabla con el estilo y clase especificados
            table = stages_h2.find_next("table", class_="wikitable roundedborder", style="text-align:center;")
            if table:
                # Busca el <td> que contiene "Regrowth"
                regrowth_cell = table.find("td", string=lambda text: text and "Regrowth:" in text)
                
                # Debug
                # print(regrowth_cell)
                
                if regrowth_cell:
                    # Extrae el número de días del texto
                    match = re.search(r"\b\d+\b", regrowth_cell.text)
                    if match:
                        self.regrowth_days = match.group()
                        return self.regrowth_days

        self.regrowth_days = "0"  # Valor por defecto si no se encuentra el dato
        return self.regrowth_days

    def get_sell_price(self, soup):
        precio_venta_row = soup.find("td", {"style": "padding: 0; border: 0;", "colspan": "2"})
        if precio_venta_row:
            table_info = precio_venta_row.find("table", {"class": "no-wrap", "style": "text-align: left; margin: 0; padding: 0; border-spacing: 0; border: 0;"})
            
            if table_info:
                # Intentamos extraer el precio de la tabla
                precio_venta = table_info.find_next("tbody")
                if precio_venta:
                    # Si encontramos el cuerpo, extraemos y asignamos el precio
                    self.sell_price = precio_venta.text.strip().split()[0]
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
                                self.sell_price = td_elements[1].get_text(strip=True)
            return "N/A"
        
        return self.sell_price
    
    def get_price_seed(self, url):
        response = requests.get(f"{BASE_URL}{url}")
        soup = BeautifulSoup(response.content, "html.parser")
        precios = soup.find_all("span", class_="no-wrap")
        if len(precios) > 1:  # Verificar si hay al menos dos precios
            precio = precios[1].text.strip()

            if re.match(r"^\d+g$", precio):
                self.seed_price = precio
            else: 
                self.seed_price = "N/A"
        elif precios:
            # Validar el primero si no hay suficientes elementos
            precio = precios[0].text.strip()
            if re.match(r"^\d+g$", precio):
                self.seed_price = precio
            else:
                self.seed_price = "N/A"

            return "N/A"

        return self.seed_price

    def __str__(self):
        return (
            f"Cultivo: {self.name}\n"
            f"Descripción: {self.description}\n"
            f"Temporada: {self.season}\n"
            f"Tiempo para crecer: {self.growth_time}\n"
            f"Cantidad cosechable: {self.harvest_quantity}\n"
            f"Recrecimiento: {self.regrowth_days} días\n"
            f"Precio de venta: {self.sell_price}\n"
            f"Precio de semillas: {self.seed_price}"
        )

