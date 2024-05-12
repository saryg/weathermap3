import requests
import pprint

import ephem
import datetime

import settings


def getForecast(location_latlon, timezone="auto"):
    # timezone = "Europe/Dublin"
    killinga_lat_lon = [51.6148, -9.1544]
    rathmines_lat_lon = [53.3203, -6.2783]
    braunschweig_latlon = [52.2637, 10.52396]

    latitude, longitude = location_latlon

    # open_meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weathercode,cloudcover,evapotranspiration,windspeed_10m,winddirection_10m,windgusts_10m,uv_index,uv_index_clear_sky,is_day&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,et0_fao_evapotranspiration&current_weather=true&forecast_days=3&timezone={timezone}"
    open_meteo_url = settings.open_meteo_url.format(
        latitude=latitude, longitude=longitude, timezone=timezone
    )
    print(open_meteo_url)
    r = requests.get(open_meteo_url)
    myjson = r.json()
    pprint.pprint(myjson["current_weather"])
    return myjson


weather_warning_regions_FIPS = {
    "Carlow": "EI01",
    "Cavan": "EI02",
    "Clare": "EI03",
    "Cork": "EI04",
    "Donegal": "EI06",
    "Dublin": "EI07",
    "Galway": "EI10",
    "Kerry": "EI11",
    "Kildare": "EI12",
    "Kilkenny": "EI13",
    "Leitrim": "EI14",
    "Laois": "EI15",
    "Limerick": "EI16",
    "Longford": "EI18",
    "Louth": "EI19",
    "Mayo": "EI20",
    "Meath": "EI21",
    "Monaghan": "EI22",
    "Offaly": "EI23",
    "Roscommon": "EI24",
    "Sligo": "EI25",
    "Tipperary": "EI26",
    "Waterford": "EI27",
    "Westmeath": "EI29",
    "Wexford": "EI30",
    "Wicklow": "EI31",
}
weather_codes = {
    0: {
        "desc": "Clear sky",
        "day_icon": "day-sunny.png",
        "night_icon": "night-clear.png",
    },
    1: {
        "desc": "Mainly clear",
        "day_icon": "day-sunny.png",
        "night_icon": "night-clear.png",
    },
    2: {
        "desc": "Partly cloudy",
        "day_icon": "day-cloudy.png",
        "night_icon": "night-alt-cloudy.png",
    },
    3: {
        "desc": "Overcast",
        "day_icon": "cloudy.png",
        "night_icon": "cloudy.png",
    },
    45: {"desc": "Fog", "day_icon": "fog.png", "night_icon": "fog.png"},
    48: {
        "desc": "Depositing rime fog",
        "day_icon": "fog.png",
        "night_icon": "fog.png",
    },
    51: {
        "desc": "Light drizzle",
        "day_icon": "day-showers.png",
        "night_icon": "night-alt-showers.png",
    },
    53: {
        "desc": "Moderate drizzle",
        "day_icon": "day-showers.png",
        "night_icon": "night-alt-showers.png",
    },
    55: {
        "desc": "Dense drizzle",
        "day_icon": "day-showers.png",
        "night_icon": "night-alt-showers.png",
    },
    56: {
        "desc": "Light freezing drizzle",
        "day_icon": "day-sleet.png",
        "night_icon": "night-alt-sleet.png",
    },
    57: {
        "desc": "Dense freezing drizzle",
        "day_icon": "day-sleet.png",
        "night_icon": "night-alt-sleet.png",
    },
    61: {
        "desc": "Light rain",
        "day_icon": "day-rain.png",
        "night_icon": "night-alt-rain.png",
    },
    63: {"desc": "Moderate rain", "day_icon": "rain.png", "night_icon": "rain.png"},
    65: {"desc": "Heavy rain", "day_icon": "rain.png", "night_icon": "rain.png"},
    66: {
        "desc": "Light freezing rain",
        "day_icon": "hail.png",
        "night_icon": "hail.png",
    },
    67: {
        "desc": "Heavy freezing rain",
        "day_icon": "hail.png",
        "night_icon": "hail.png",
    },
    71: {
        "desc": "Light snow",
        "day_icon": "day-snow.png",
        "night_icon": "night-alt-snow.png",
    },
    73: {"desc": "Moderate snow", "day_icon": "snow.png", "night_icon": "snow.png"},
    75: {"desc": "Heavy snow", "day_icon": "snow.png", "night_icon": "snow.png"},
    77: {"desc": "Snow grains", "day_icon": "snow.png", "night_icon": "snow.png"},
    80: {
        "desc": "Light rain showers",
        "day_icon": "day-showers.png",
        "night_icon": "night-alt-showers.png",
    },
    81: {
        "desc": "Moderate rain showers",
        "day_icon": "showers.png",
        "night_icon": "showers.png",
    },
    82: {
        "desc": "Heavy rain showers",
        "day_icon": "showers.png",
        "night_icon": "showers.png",
    },
    85: {
        "desc": "Light snow showers",
        "day_icon": "day-snow.png",
        "night_icon": "night-alt-snow.png",
    },
    86: {
        "desc": "Heavy snow showers",
        "day_icon": "snow.png",
        "night_icon": "snow.png",
    },
    95: {
        "desc": "Thunderstorm",
        "day_icon": "thunderstorm.png",
        "night_icon": "thunderstorm.png",
    },
    96: {
        "desc": "Thunderstorm with light hail",
        "day_icon": "day-storm-showers.png",
        "night_icon": "night-alt-storm-showers.png",
    },
    99: {
        "desc": "Thunderstorm with heavy hail",
        "day_icon": "storm-showers.png",
        "night_icon": "storm-showers.png",
    },
}


def getWeatherWarnings(region):
    weather_warning_region = weather_warning_regions_FIPS[region]
    # weather_warnings_url = f"https://www.met.ie/Open_Data/json/warning_{weather_warning_region}.json"
    weather_warnings_url = settings.met_eireann_weather_warnings_url.format(
        weather_warning_region=weather_warning_region
    )
    r = requests.get(weather_warnings_url)
    weather_warning_data = r.json()
    pprint.pprint(weather_warning_data)
    return weather_warning_data


def get_moon_phase(date=None):
    """
    This function returns the moon phase for a given date.
    If no date is provided, the current date is used.

    :param date: The date for which the moon phase is fetched.
    :type date: datetime.date, optional
    :return: The moon phase (0: New Moon, 0.5: First Quarter, 1.0: Full Moon)
    :rtype: float
    """
    if date is None:
        date = datetime.datetime.now()

    moon = ephem.Moon(date)
    phase = moon.moon_phase

    next_full_moon = ephem.next_full_moon(date)
    return phase, next_full_moon


def main():
    forecast_data = getForecast([53.3203, -6.2783])

    is_day = forecast_data["current_weather"]["is_day"]

    hourly_fc = forecast_data["hourly"]["time"][1]
    weather_code = forecast_data["current_weather"]["weathercode"]
    temperature_2m = forecast_data["hourly"]["temperature_2m"][1]
    temperature_2m_units = forecast_data["hourly_units"]["temperature_2m"]
    print(is_day)
    print(hourly_fc, temperature_2m, temperature_2m_units)
    print(weather_codes[weather_code])

    moon_phase, next_full_moon = get_moon_phase()
    print(f"Today's moon phase is: {moon_phase:.2f}")
    print(next_full_moon)

    weather_warning_data = getWeatherWarnings("Cork")


if __name__ == "__main__":
    main()
