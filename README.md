# 🌾 Stardew Crawler

![Stardew Valley Logo](https://stardewvalleywiki.com/mediawiki/images/6/68/Main_Logo.png) <!-- Sustituir por el enlace real del logo -->

Un proyecto diseñado para **Seguridad de la Información** y **Programación para Internet**, que permite a los jugadores de _Stardew Valley_ optimizar su experiencia. Nuestro objetivo principal fue desarrollar un pequeño _web crawler_ que extrae datos clave sobre cultivos desde el [Stardew Valley Wiki](https://stardewvalleywiki.com) para ayudar a identificar los cultivos más rentables según la temporada de forma personalizada para el usuario.

[Video DEMO](https://www.youtube.com/watch?v=u_0nsRo5s4E&authuser=0&hl=es)

## Información del equipo

- **Briceño Caguado, Luis Gerardo**: 219473333
- **Castañeda Serrano, Oscar**: 218623986 
- **Pinto Soriano, Emiliano Ramón**: 219617335

## 🚀 Funcionalidades

- **Extracción de cultivos**: Obtiene enlaces y datos relevantes de cultivos de [Stardew Valley Wiki](https://stardewvalleywiki.com)
- **Optimización de granjas**: Filtra cultivos según días restantes de la temporada y maximiza el beneficio tomando en consideración los cultivos que pueden ser cosechados varias veces sin ser plantados de nuevo.
- **Interfaz gráfica**: Creada con Tkinter, sencilla y fácil de usar con ventanas para cargar partidas y seleccionar cultivos.

---

## 🛠️ Instalación

- **Ejecutable .exe**: Se compiló un ejecutable .exe utilizando la librería _pyinstaller_ para hacer más fácil el uso de la aplicación, este ejecutable se actualizará con cada versión.

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/ruisuhq/Stardew-Crawler.git
   cd stardew-valley-webcrawler/Source Code
   ```

2. **Instalar dependencias y fuentes**:
   Asegúrate de tener Python instalado. Luego, ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

   Además, si quieres utilizar la fuente utilizada para el ejecutable, puedes conseguirla aquí [Stardew Valley Font](https://www.fontbolt.com/font/stardew-valley-font/) (redditor Cowsplay)

3. **Ejecutar el programa**:

   ```bash
   python main.py
   ```

---

## 🌟 Características

### 1. **Interfaz Gráfica de Usuario (GUI)**

La aplicación incluye una GUI intuitiva, permitiendo a los jugadores interactuar fácilmente con sus datos de cultivo:

- **Ventana de selección de partidas guardadas**:
  Selecciona tu partida desde una lista e ingresa al análisis personalizado.

- **Visualización de cultivos disponibles**:
  Explora cultivos recomendados según la temporada y días restantes.

- **Cálculo de beneficios**:
  Calcula costos, ingresos totales y beneficios netos.

### 2. **Rastreo Web**

- Limita su búsqueda a páginas que contienen `crops` o `season`.
- Extrae datos como:
  - Temporada ideal
  - Tiempo de crecimiento
  - Precio de venta
  - Precio de semillas en la tienda de Pierre.

### 3. **Datos Exportables**

- Exporta resultados como archivos JSON para un análisis más detallado.

---

## 📖 Uso

### 1. **Carga de Partidas**

Selecciona una partida guardada para analizar la temporada actual y días restantes.

### 2. **Rastreo y Filtrado**

El _web crawler_ analizará los cultivos más rentables basados en:

- Temporada actual
- Días restantes para cosechar

### 3. **Resultados y Beneficios**

Se mostrarán los cultivos disponibles, permitiéndote seleccionar uno y calcular sus beneficios potenciales.
