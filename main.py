
import requests 
from geopy.distance import geodesic
import os
import argparse
import json 
from dotenv import load_dotenv

load_dotenv()

# Configuración desde .env
POS= os.getenv("POSICION")
MY_POS = (float(os.getenv("MY_LAT")), float(os.getenv("MY_LON")))
CONSUMO = float(os.getenv("COCHE_CONSUMO"))
LITROS = float(os.getenv("LITROS_REPOSTAJE"))
PRODUCTO = os.getenv("PRODUCTO_OFICIAL")  #Etiqueta oficial de la API, por ejemplo 'Gasolina 95 E5'
RADIO_MAX = 20 #km
NUM_RESULTADOS = 5 #numero de gasolineras
TELEGRAMTOKEN= os.getenv("TELEGRAM_TOKEN")
TELEGRAMCHAT= os.getenv("TELEGRAM_CHAT")


def configurar_argumentos():
    """Configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Buscador de gasolineras baratas en España.")
    
    # Añadimos los argumentos con sus valores por defecto del .env
    parser.add_argument("--radio", type=int, default=RADIO_MAX, help="Radio de búsqueda en km")
    parser.add_argument("--num", type=int, default=NUM_RESULTADOS, help="Número de resultados a mostrar")
    parser.add_argument("--litros", type=float, default=LITROS, help="Litros a repostar")
    parser.add_argument("--consumo", type=float, default=CONSUMO, help="Consumo del coche l/100km")
    parser.add_argument("--prod", type=str, default=PRODUCTO, help="Tipo de Gasolina")
    
    return parser.parse_args()

def obtener_gps_termux():
    """Llama a la API de Termux para obtener la ubicación real del GPS."""
    try:
        print("📡 Obteniendo ubicación GPS del móvil...")
        # Ejecutamos el comando de Termux: -s es para 'single' (una lectura)
        result = subprocess.run(['termux-location', '-s', 'gps'], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return float(data['latitude']), float(data['longitude'])
    except Exception as e:
        print(f"⚠️ No se pudo obtener el GPS: {e}")
    return None

def get_gasolineras():
    url = "https://energia.serviciosmin.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['ListaEESSPrecio']
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return []

def enviar_telegram(mensaje):
    token = TELEGRAMTOKEN
    chat_id = TELEGRAMCHAT
    if not token or not chat_id:
        print("⚠️ Configuración de Telegram incompleta.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("📩 Notificación enviada a Telegram.")
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

def calcular_ahorro(args):
    
    pos_actual = obtener_gps_termux()
    
    if pos_actual:
        lat, lon = pos_actual
        origen_nombre = "GPS Móvil"
    else:
        lat = float(os.getenv("MY_LAT"))
        lon = float(os.getenv("MY_LON"))
        origen_nombre = os.getenv("POSICION")

    my_pos = (lat, lon)
    
    print(f"📍 Ubicación detectada: {origen_nombre} ({lat}, {lon})")
    
    data = get_gasolineras()
    if not data: return

    resultados = []

    for g in data:
        # Extraer precio 95
        p_str = g[args.prod].replace(',', '.')
        
        if not p_str or p_str == "": 
            continue
            
        precio = float(p_str)

        # Coordenadas de la gasolinera
        try:
            lat = float(g['Latitud'].replace(',', '.'))
            lon = float(g['Longitud (WGS84)'].replace(',', '.'))
            g_pos = (lat, lon)
        except ValueError:
            continue

        # Calcular distancia real
        distancia_km = geodesic(MY_POS, g_pos).km

        # Filtramos por un radio razonable (20km)
        if distancia_km > args.radio: continue

        # --- CÁLCULO DEL COSTE REAL ---
        # 1. Lo que pagas en el surtidor
        coste_repostaje = precio * args.litros
        
        # 2. Lo que gastas en llegar (Ida + Vuelta)
        # consumo/100 * km_totales * precio_litro
        coste_desplazamiento = (distancia_km * 2) * (args.consumo / 100) * precio
        
        coste_total_operacion = coste_repostaje + coste_desplazamiento

        resultados.append({
            'nombre': g['Rótulo'],
            'direccion': g['Dirección'],
            'municipio': g['Municipio'],
            'distancia': distancia_km,
            'precio_litro': precio,
            'coste_total': coste_total_operacion
        })

    # Ordenamos por el coste TOTAL (Gasolina + Viaje)
    resultados.sort(key=lambda x: x['coste_total'])

    print(f"\n✅ ANÁLISIS PARA {args.prod} ({args.litros}L)")
    print(f"📍 Ubicación base: {POS}")
    print("-" * 50)

    for i, res in enumerate(resultados[:args.num], 1):
        print(f"{i}. {res['nombre']} - {res['municipio']}")
        print(f"   📍 {res['direccion']}")
        print(f"   🛣️  Distancia: {res['distancia']:.2f} km")
        print(f"   💰 Precio Surtidor: {res['precio_litro']:.3f} €/L")
        print(f"   ⛽ COSTE TOTAL REAL: {res['coste_total']:.2f} €")
        print("-" * 50)

    #Preparar mensaje para Telegram con la mejor opción
    mejor = resultados[0]
    mensaje = (
        f"⛽ *¡Gasolinera más económica hoy!*\n\n"
        f"🏢 *{mejor['nombre']}*\n"
        f"📍 {mejor['municipio']}\n"
        f"🛣️ Distancia: {mejor['distancia']:.2f} km\n"
        f"💰 Precio: {mejor['precio_litro']:.3f} €/L\n"
        f"⛽ *COSTE TOTAL: {mejor['coste_total']:.2f} €* (Inc. viaje)"
    )
    
    enviar_telegram(mensaje)


if __name__ == "__main__":
    mis_args = configurar_argumentos()
    calcular_ahorro(mis_args)

