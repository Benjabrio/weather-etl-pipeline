import json
import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": -31.42,
    "longitude": -64.18,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
    "timezone": "America/Argentina/Cordoba",
    "forecast_days": 3,
}

respuesta = requests.get(url, params=params, timeout=10)

print("Código de estado:", respuesta.status_code)

datos = respuesta.json()
print(json.dumps(datos, indent=2, ensure_ascii=False))