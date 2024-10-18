from PIL import ImageFont

# Screen and sidebar width and heights
screen_width = 825
screen_height = 1200
dpi = 150
sidebar_width = 80
sidebar_height = screen_height
map_display_width = screen_width - sidebar_width

# Paths
path = "/home/sara/Weathermap3.2/"
font_path = path + "fonts/BebasNeue-Regular.ttf"  # "fonts/WalterTurncoat-Regular.ttf"
icon_path = path + "icons-transparent/"
base_map_path = path + "images/{country}_base_map.png"
weathermap_bmp_path = path + "images/weathermap.bmp"

map_unit_shapefile_path = path + "ne_10m_map_units/ne_10m_admin_0_map_units.shp"

radar_map_path = path + "images/radar_map.png"
pickle_path = path + "plots/{country}.axes.pickle"

# URLS
met_eireann_weather_warnings_url = (
    "https://www.met.ie/Open_Data/json/warning_{weather_warning_region}.json"
)
open_meteo_url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,weathercode,cloudcover,evapotranspiration,windspeed_10m,winddirection_10m,windgusts_10m,uv_index,uv_index_clear_sky,is_day&daily=weathercode,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,uv_index_max,uv_index_clear_sky_max,precipitation_sum,rain_sum,showers_sum,snowfall_sum,precipitation_hours,precipitation_probability_max,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant,et0_fao_evapotranspiration&current_weather=true&forecast_days=3&timezone={timezone}"

rainviewer_timestamp_url = "https://api.rainviewer.com/public/weather-maps.json"
rainviewer_radar_tile_url = "https://tilecache.rainviewer.com/v2/radar/{timestamp}/256/{z}/{x}/{y}/8/1_1.png"  # /colourscheme/smooth_snow 0=b2

# Locations for forecast and current conditions
forecast_locations = {
    "Braunschweig": {
        "coords": [52.2637, 10.5239],
        "country": "Germany",
        "region": "",
    },
    "Rathmines": {
        "coords": [53.3203, -6.2783],
        "country": "Ireland",
        "region": "Dublin",
    },
    "Terenure": {
        "coords": [53.3203, -6.2783],
        "country": "Ireland",
        "region": "Dublin",
    },

    "Killinga": {
        "coords": [51.6148, -9.1544],
        "country": "Ireland",
        "region": "Cork",
    },
    "Galway": {"coords": [53.2791, -9.0573], "country": "Ireland", "region": "Galway"},
}

# Country map tile settings
map_settings = {
    "Ireland": {
        "centre_lon": -8,
        "centre_lat": 53,
        "zoom": 5,  # 4 to 8. see tiles
        "extent": [-12.8, -2.4, 49, 58],  # [-14, -2, 49, 58],
        "focus_country_codes": ["IRL", "NIR"],
        "non_focus_country_codes": ["WLS", "ENG", "SCT", "IMN"],
        "points_of_interest": {
            "Killinga": [51.6148, -9.1544],
            "Terenure": [53.3203, -6.2783],
            #"Dunmore East": [52.1526, -6.9954],
            #"Sligo": [54.2771, -8.4743]
            # "Dublin": [53.3203, -6.2783], # ==rathmines
        },
        "forecast_location": "Rathmines",
        "tiles": {
            8: {"xrange": range(119, 125), "yrange": range(79, 87)},
            7: {"xrange": range(59, 63), "yrange": range(39, 43)},
            6: {"xrange": range(29, 32), "yrange": range(19, 22)},
            5: {"xrange": range(14, 16), "yrange": range(9, 11)},
            4: {"xrange": range(7, 8), "yrange": range(4, 6)},
        },
    },
    "Germany": {
        "centre_lon": 10,
        "zoom": 5,  # only 6
        "extent": [
            3.2,
            19.4,
            43.75,
            58.45,
        ], 
        # [3.2, 19.4, 43.75, 58.45],  # [3, 17.5, 44, 58],
        "focus_country_codes": ["DEU"],
        "non_focus_country_codes": [
            "FRA",
            "HUN",
            "DNK",
            "AUT",
            "CZE",
            "POL",
            "CHE",
            "BEL",
            "LUX",
            "NLD",
            "ITA",
            "HRV",
            "BIH",
            "SWE",
            "SVK",
            "SVN",
        ],  # ["DNK", "POL", "SWE", "NLD"]#
        "points_of_interest": {
            "Braunschweig": [52.2637, 10.5239],
            "Bad Gandersheim": [51.8700, 10.0252],
            "Bad Waldsee": [47.9203, 9.7533],
            "Halle": [51.4938, 11.9657],
            "Göttingen": [51.5405, 9.9168],
            "Berlin": [52.5180, 13.4027],
            "München": [48.1428, 11.5706],
            "Selingstadt": [49.13001, 11.1497],
        },
        "forecast_location": "Braunschweig",
        "tiles": {
            6: {"xrange": range(32, 36), "yrange": range(19, 24)},
            5: {"xrange": range(16, 18), "yrange": range(9, 12)},
        },
    },
}


# Icon and Font Sizes
SMALLER_ICON_SIZE = (30, 30)
ALMOST_SMALL_ICON_SIZE = (35, 35)
SMALL_ICON_SIZE = (40, 40)
ALMOST_MED_ICON_SIZE = (55, 55)
MED_ICON_SIZE = (60, 60)
LARGE_ICON_SIZE = (80, 80)


SMALLER_FONT = ImageFont.truetype(
    font_path,
    size=20,
)

SMALL_FONT = ImageFont.truetype(
    font_path,
    size=25,
)
MED_FONT = ImageFont.truetype(
    font_path,
    size=35,
)
LARGE_FONT = ImageFont.truetype(
    font_path,
    size=45,
)
LARGER_FONT = ImageFont.truetype(
    font_path,
    size=50,
)
EXTRA_LARGE_FONT = ImageFont.truetype(
    font_path,
    size=65,
)
