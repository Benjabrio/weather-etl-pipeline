import pandas as pd

COLUMN_MAP = {
    "time": "weather_date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "precipitation_mm",
    "wind_speed_10m_max": "wind_max_kmh",
}

MEASURE_COLUMNS = ["temp_max_c", "temp_min_c", "precipitation_mm", "wind_max_kmh"]


def out_of_range(series, low, high):
    """True donde el valor existe pero está fuera del rango permitido."""
    return series.notna() & ~series.between(low, high)


def transform_weather(raw, city_name):
    """Convierte el JSON de la API en dos DataFrames: válidos y rechazados."""
    df = pd.DataFrame(raw["daily"]).rename(columns=COLUMN_MAP)

    df["weather_date"] = pd.to_datetime(df["weather_date"], errors="coerce").dt.date
    for col in MEASURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["city_name"] = city_name
    df = df.drop_duplicates(subset=["city_name", "weather_date"])

    reglas = pd.DataFrame({
        "fecha_invalida": df["weather_date"].isna(),
        "temp_max_fuera_de_rango": out_of_range(df["temp_max_c"], -60, 60),
        "temp_min_fuera_de_rango": out_of_range(df["temp_min_c"], -60, 60),
        "temp_min_mayor_que_max": df["temp_min_c"] > df["temp_max_c"],
        "precipitacion_fuera_de_rango": out_of_range(df["precipitation_mm"], 0, 1000),
        "viento_fuera_de_rango": out_of_range(df["wind_max_kmh"], 0, 400),
    })

    es_invalida = reglas.any(axis=1)

    df_validos = df[~es_invalida].copy()
    df_rechazados = df[es_invalida].copy()

    if not df_rechazados.empty:
        df_rechazados["motivo"] = reglas[es_invalida].apply(
            lambda fila: ", ".join(fila.index[fila]), axis=1
        )

    return df_validos, df_rechazados


if __name__ == "__main__":
    from src.extract import extract_weather

    raw = extract_weather(-31.42, -64.18, "America/Argentina/Cordoba", forecast_days=3)

    # Simulamos un dato inválido para ver cómo reacciona la validación
    raw["daily"]["precipitation_sum"][1] = -5

    validos, rechazados = transform_weather(raw, "Córdoba")

    print("VÁLIDOS:")
    print(validos)
    print("\nRECHAZADOS:")
    print(rechazados)