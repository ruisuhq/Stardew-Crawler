import json

def cargar_cultivos(ruta):
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

cultivos = cargar_cultivos('cultivos.json')

def filtrar_cultivos(temporada, dias_restantes):
    disponibles = []
    for cultivo in cultivos:
        tiempo_crecer_raw = cultivo["tiempo_crecer"]
        
        # Manejar casos donde tiempo_crecer es "N/A" u otros valores no numéricos
        if tiempo_crecer_raw.lower() == "n/a":
            continue  # Ignorar cultivos no válidos para sembrar
        
        tiempo_crecer = int(tiempo_crecer_raw.split()[0])  # Convertir "7 days" -> 7
        
        if cultivo["temporada"].lower() == temporada.lower() and tiempo_crecer <= dias_restantes:
            disponibles.append(cultivo)
    
    # Ordenar cultivos disponibles por precio de venta (de mayor a menor)
    cultivos_ordenados = sorted(
        disponibles,
        key=lambda x: int(x["precio_venta"].replace("g", "").strip()),
        reverse=True  # Orden descendente
    )
    
    return cultivos_ordenados

def mostrar_cultivos(disponibles):
    print("\nCultivos disponibles:")
    for i, cultivo in enumerate(disponibles, start=1):
        print(f"{i}. {cultivo['nombre']} - Precio Semillas: {cultivo['precio_semillas']} - Precio Venta: {cultivo['precio_venta']} - Días para crecer: {cultivo['tiempo_crecer']}")

def calcular_costos_y_ganancias(cultivo, casillas, dias_restantes):
    # Convertir los precios de texto a números
    precio_semillas = int(cultivo["precio_semillas"].replace("g", "").strip())
    precio_venta = int(cultivo["precio_venta"].replace("g", "").strip())
    
    # Obtener la cantidad cosechable
    cantidad_cosechable = int(cultivo["cantidad_cosechable"])
    
    #Días restantes después de la primera cosecha
    dias = dias_restantes - int(cultivo["tiempo_crecer"].split()[0])

    #Veces totales que volvió a crecer y cosecharse el cultivo
    Recrecimientos = 1 + (dias // int(cultivo["Recrecimiento"]))
    
    # Calcular los costos y ganancias
    costo_total = precio_semillas * casillas
    ganancia_total = (precio_venta * cantidad_cosechable * casillas * Recrecimientos)
    beneficio_neto = ganancia_total - costo_total

    return costo_total, ganancia_total, beneficio_neto

def calcular_dias_restantes(dia_actual):
    return 28 - dia_actual

def main():
    while True:
        print("\n--- Stardew Valley: Calculadora de Cultivos ---")
        temporada = input("Temporada (spring/summer/fall/winter): ").strip().lower()
        dia_actual = int(input("Día (1-28): "))
        año = int(input("Año: "))  # No se usa directamente ahora pero puede ser útil

        dias_restantes = calcular_dias_restantes(dia_actual)
        print(f"Días restantes en la temporada: {dias_restantes}")

        cultivos_disponibles = filtrar_cultivos(temporada, dias_restantes)

        if not cultivos_disponibles:
            print("No hay cultivos disponibles para plantar en los días restantes.")
            continue

        mostrar_cultivos(cultivos_disponibles)
        
        seleccion = int(input("\nSelecciona un cultivo por número: ")) - 1
        cultivo_seleccionado = cultivos_disponibles[seleccion]
        
        print(f"\nHas seleccionado: {cultivo_seleccionado['nombre']}")
        
        casillas = int(input("¿Cuántas casillas deseas plantar?: "))
        costo_total, ganancia_total, beneficio_neto = calcular_costos_y_ganancias(cultivo_seleccionado, casillas, dias_restantes)
        
        print(f"\nResultados:")
        print(f"Costo Total: {costo_total}g")
        print(f"Ganancia Total: {ganancia_total}g")
        print(f"Beneficio Neto: {beneficio_neto}g")

        repetir = input("\n¿Quieres calcular otro cultivo? (sí/no): ").strip().lower()
        if repetir != 'sí':
            break

if __name__ == "__main__":
    main()