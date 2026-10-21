USE open_meteo_db;

CREATE TABLE IF NOT EXISTS cities (
    city_id     INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    latitude    DECIMAL(8,5) NOT NULL,
    longitude   DECIMAL(8,5) NOT NULL,
    timezone    VARCHAR(50)  NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_daily (
    city_id           INT          NOT NULL,
    weather_date      DATE         NOT NULL,
    temp_max_c        DECIMAL(4,1),
    temp_min_c        DECIMAL(4,1),
    precipitation_mm  DECIMAL(5,1),
    wind_max_kmh      DECIMAL(5,1),
    loaded_at         TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id, weather_date),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);