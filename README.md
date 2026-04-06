# 🏎️ OptimazerFuel

**OptimazerFuel** es una herramienta desarrollada en Python que buscan optimizar el coste de repostaje de su vehículo en España.

A diferencia de otros buscadores, este script no solo busca el precio más bajo, sino que calcula el **Coste Real** del desplazamiento (ida y vuelta) respecto a una posicion para determinar si realmente sale a cuenta desviarse a una gasolinera más barata.


---

## ✨ Características

- ⛽ **Datos Oficiales:** Conexión en tiempo real con la API del **Ministerio para la Transición Ecológica** (Geoportal Gasolineras).
- 🧠 **Algoritmo de Ahorro Real:** Calcula: `(Litros × Precio) + (Consumo × Distancia × 2 × Precio)`.
- 📍 **Geolocalización:** Cálculo de distancia ortodrómica mediante la librería `geopy`.
- 🛡️ **Privacidad:** Uso de variables de entorno (`.env`) para proteger tu ubicación base.
- 🐧 **Linux Ready:** Optimizado para entornos limpios mediante `venv`.
- 🌍 **SMS Telegram:** Envia un sms al chat de Telegram para compartir resultados.

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/uny11/OptimazerFuel.git
   cd OptimazerFuel
   ```

2. **Lanzar el script con variables por defecto**
   ```bash
   python main.py 
   ```

## 🚀 Ayuda

1. El script permite argumentos, se puede ver una descripcion con:
   ```bash
   python main.py --help
   
   usage: main.py [-h] [--radio RADIO] [--num NUM] [--litros LITROS] [--consumo CONSUMO] [--prod PROD]

   Buscador de gasolineras baratas en España.

   options:
      -h, --help         show this help message and exit
      --radio RADIO      Radio de búsqueda en km
      --num NUM          Número de resultados a mostrar
      --litros LITROS    Litros a repostar
      --consumo CONSUMO  Consumo del coche l/100km
      --prod PROD        'Precio Gasolina 95 E5' o 'Gasóleo A'
   ```


2. Se puede lanzar el script main.py desde un terminal de un movil Android, como Termux, el script buscara la posicion GPS del movil para hacer los calculos, si no encuentra nada usa las variables del archivo .env

3. Ejemplo de archivo `.env`:
   ```bash
   POSICION=Casa
   MY_LAT=39.449211
   MY_LON=1.44565

   COCHE_CONSUMO=7.2 
   LITROS_REPOSTAJE=40
   PRODUCTO_OFICIAL=Precio Gasolina 95 E5
   
   TELEGRAM_TOKEN= escribe el token de tu bot de telegram
   TELEGRAM_CHAT= escribe tu id de chat
   ```
