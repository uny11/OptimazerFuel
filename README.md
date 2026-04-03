# 🏎️ OptimazerFuel

**OptimazerFuel** es una herramienta desarrollada en Python que buscan optimizar el coste de repostaje de su vehículo..

A diferencia de otros buscadores, este script no solo busca el precio más bajo, sino que calcula el **Coste Real** del desplazamiento (ida y vuelta) para determinar si realmente sale a cuenta desviarse a una gasolinera más barata.

![Cupra Formentor](https://images.unsplash.com/photo-1630514197420-569d20f18835?q=80&w=1000&auto=format&fit=crop) 
*(Puedes sustituir esta URL por una foto propia de tu coche subida a GitHub)*

---

## ✨ Características

- ⛽ **Datos Oficiales:** Conexión en tiempo real con la API del **Ministerio para la Transición Ecológica** (Geoportal Gasolineras).
- 🧠 **Algoritmo de Ahorro Real:** Calcula: `(Litros × Precio) + (Consumo × Distancia × 2 × Precio)`.
- 📍 **Geolocalización:** Cálculo de distancia ortodrómica mediante la librería `geopy`.
- 🛡️ **Privacidad:** Uso de variables de entorno (`.env`) para proteger tu ubicación base.
- 🐧 **Arch Linux Ready:** Optimizado para entornos limpios mediante `venv`.

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/uny11/OptimazerFuel.git](https://github.com/uny11/OptimazerFuel.git)
   cd OptimazerFuel
