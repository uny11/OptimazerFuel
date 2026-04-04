
import requests
from geopy.distance import geodesic
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración desde .env
MY_POS = (float(os.getenv("MY_LAT")), float(os.getenv("MY_LON")))
CONSUMO = float(os.getenv("CUPRA_CONSUMO"))
LITROS = float(os.getenv("LITROS_REPOSTAJE"))

# Etiqueta oficial de la API para Gasolina 95 E5
PRODUCTO_95 = 'Precio Gasolina 95 E5'

def get_gasolineras():
    url = "https://energia.serviciosmin.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()['ListaEESSPrecio']
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return []

def calcular_ahorro():
    data = get_gasolineras()
    if not data: return

    resultados = []

    for g in data:
        # Extraer precio 95
        p_str = g[PRODUCTO_95].replace(',', '.')
        
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
        if distancia_km > 30: continue

        # --- CÁLCULO DEL COSTE REAL ---
        # 1. Lo que pagas en el surtidor
        coste_repostaje = precio * LITROS
        
        # 2. Lo que gastas en llegar (Ida + Vuelta)
        # consumo/100 * km_totales * precio_litro
        coste_desplazamiento = (distancia_km * 2) * (CONSUMO / 100) * precio
        
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

    print(f"\n✅ ANÁLISIS PARA GASOLINA 95 E5 ({LITROS}L)")
    print(f"📍 Ubicación base: {MY_POS}")
    print("-" * 50)

    for i, res in enumerate(resultados[:20], 1):
        print(f"{i}. {res['nombre']} - {res['municipio']}")
        print(f"   📍 {res['direccion']}")
        print(f"   🛣️  Distancia: {res['distancia']:.2f} km")
        print(f"   💰 Precio Surtidor: {res['precio_litro']:.3f} €/L")
        print(f"   ⛽ COSTE TOTAL REAL: {res['coste_total']:.2f} €")
        print("-" * 50)

if __name__ == "__main__":
    calcular_ahorro()