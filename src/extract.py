import requests

API_URL = "https://api.open-meteo.com/v1/forecast"

DAILY_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]


def extract_weather(latitude, longitude, timezone, forecast_days=7):
    """Consulta la API y da como resultado un JSON como diccionario."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": timezone,
        "forecast_days": forecast_days,
    }

    respuesta = requests.get(API_URL, params=params, timeout=10)
    respuesta.raise_for_status()

    return respuesta.json()


if __name__ == "__main__":
    datos = extract_weather(-31.42, -64.18, "America/Argentina/Cordoba", forecast_days=3)
    print(datos["daily"])