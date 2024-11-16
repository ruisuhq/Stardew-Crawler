import requests, json, re
from bs4 import BeautifulSoup

BASE_URL = "https://stardewvalleywiki.com"

class Crop:
    def __init__(self, name="n/a", description="n/a", season="n/a", growth_time="n/a", sell_price="n/a", seed_price="n/a"):
        self.name = name
        self.description = description
        self.season = season
        self.growth_time = growth_time
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
        return f"Cultivo: {self.name}\nDescripción: {self.description}\nTemporada: {self.season}\n" \
               f"Tiempo para crecer: {self.growth_time}\nPrecio de venta: {self.sell_price}\n" \
               f"Precio de semillas: {self.seed_price}"
