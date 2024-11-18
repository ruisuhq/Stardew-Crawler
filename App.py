import json
from stardew_saves import *

APPDATA_DIR = os.getenv('APPDATA')
SAVES_DIR = fr"{APPDATA_DIR}\StardewValley\Saves"


def load_crops(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def filter_crops(crops, season, remaining_days):
    available = []
    for crop in crops:
        # Usa .get para manejar claves faltantes con un valor predeterminado
        regrowth_days = crop.get("regrowth_days", "0")  # Predeterminado a "0"
        
        # Manejar casos donde regrowth_days no es un número válido
        if regrowth_days.lower() == "n/a":
            continue  # Ignorar cultivos no válidos para plantar
        
        regrowth_time = int(regrowth_days) if regrowth_days.isdigit() else 0  # Convertir a entero
        
        if crop.get("season", "").lower() == season.lower() and regrowth_time <= remaining_days:
            available.append(crop)
    
    # Ordenar cultivos disponibles por precio de venta (de mayor a menor)
    sorted_crops = sorted(
        available,
        key=lambda x: int(x.get("sell_price", "0").replace("g", "").strip()),
        reverse=True  # Orden descendente
    )
    
    return sorted_crops

def display_crops(available):
    print("\nAvailable crops:")
    for i, crop in enumerate(available, start=1):
        print(f"{i}. {crop['name']} - Seed Price: {crop['price_seed']} - Sell Price: {crop['sell_price']} - Growth Time: {crop['growth_time']}")

def calculate_costs_and_profits(crop, tiles, remaining_days):
    # Convert prices from text to numbers
    seed_price = int(crop["price_seed"].replace("g", "").strip()) if crop["price_seed"] != "N/A" else 0
    sell_price = int(crop["sell_price"].replace("g", "").strip())
    
    # Get harvest quantity
    harvest_quantity = int(crop["harvest_quantity"])
    
    # Days remaining after the first harvest
    days = remaining_days - int(crop["growth_time"].split()[0])

    # Total times the crop regrows and is harvested
    regrowths = 1 + (days // int(crop["regrowth_days"])) if crop["regrowth_days"] != "0" else 1
    
    # Calculate costs and profits
    total_cost = seed_price * tiles
    total_profit = sell_price * harvest_quantity * tiles * regrowths
    net_profit = total_profit - total_cost

    return total_cost, total_profit, net_profit

def calculate_remaining_days(current_day):
    return 28 - current_day

#Main de prueba para testeos de algoritmos
def main():
    ruta_archivo = "OT_378081712"
    raiz = cargar_datos_archivo(fr"{SAVES_DIR}\{ruta_archivo}\{ruta_archivo}")

    date = obtener_fecha_juego(raiz)
    while True:
        season = date[0]
        current_day = int(date[1])
        year = int(date[2])

        remaining_days = calculate_remaining_days(current_day)
        print(f"Days remaining in the season: {remaining_days}")

        available_crops = filter_crops(season, remaining_days)

        if not available_crops:
            print("No crops are available to plant within the remaining days.")
            continue

        display_crops(available_crops)
        
        selection = int(input("\nSelect a crop by number: ")) - 1
        selected_crop = available_crops[selection]
        
        print(f"\nYou selected: {selected_crop['name']}")
        
        tiles = int(input("How many tiles do you want to plant?: "))
        total_cost, total_profit, net_profit = calculate_costs_and_profits(selected_crop, tiles, remaining_days)
        
        print(f"\nResults:")
        print(f"Total Cost: {total_cost}g")
        print(f"Total Profit: {total_profit}g")
        print(f"Net Profit: {net_profit}g")

        repeat = input("\nDo you want to calculate another crop? (yes/no): ").strip().lower()
        if repeat != 'yes':
            break

if __name__ == "__main__":
    main()
