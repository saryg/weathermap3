# import argparse
import datetime
import json
import optparse

from dateutil import parser as prs

from PIL import Image, ImageOps, ImageDraw, ImageFont

# import pytz

import weathermap
import forecast
import settings

import sys


def addSidebar(image, forecast_data):
    sb_x = settings.map_display_width
    sb_y = 0

    sidebar = Image.new(
        "RGBA",
        (settings.sidebar_width, settings.sidebar_height),
        "black",
    )
    image.paste(sidebar, (sb_x, sb_y))

    draw = ImageDraw.Draw(image)

    current_hour = forecast_data["current_weather"]["time"].replace("T", ":").split(":")
    current_hour = int(current_hour[1])
    # print(current_hour)
    sidebar_forecast = []

    current_drawing_position = 5  # begin 5px down the sidebar
    position_offset = 40  # spacing between forecast blocks
    line_padding = 4

    for hour in range(current_hour + 2, current_hour + (15), 3):  # 5 times
        current_drawing_position = current_drawing_position + position_offset

        day_night_icon = isDayNight(hour, forecast_data)
        hour_24 = hour % 24
        hour_12 = 12 if hour_24 in [0, 12] else hour % 12
        am_pm_str = amPmDayNight(hour_24)
        weathercode = forecast_data["hourly"]["weathercode"][hour]
        sidebar_forecast.append(
            [hour_12, am_pm_str, forecast_data["hourly"]["weathercode"][hour]]
        )

        # add time
        text = str(hour_12) + "" + am_pm_str
        font = settings.SMALL_FONT
        new_x, text_width, text_height = centreTextHorizontally(
            draw, text, font, sb_x, settings.screen_width
        )
        draw.text(
            (new_x, current_drawing_position),
            text,
            fill="white",
            font=font,
        )
        current_drawing_position = current_drawing_position + text_height + line_padding

        # add icon image
        icons_path = settings.icon_path

        icon_size = settings.MED_ICON_SIZE
        forecast_icon_path = (
            icons_path + forecast.weather_codes[weathercode][day_night_icon]
        )
        _, forecast_icon = setup_icon_image(forecast_icon_path, icon_size)
        new_x = centreIconHorizontally(icon_size[0], sb_x, settings.screen_width)
        image.paste(
            forecast_icon,
            (new_x, current_drawing_position),
            forecast_icon,
        )
        current_drawing_position += icon_size[1] - 10

        # add temperature
        text = str(round(forecast_data["hourly"]["apparent_temperature"][hour])) + "°"
        text_font_size = settings.LARGE_FONT
        new_x, text_width, text_height = centreTextHorizontally(
            draw, text, text_font_size, sb_x, settings.screen_width
        )
        draw.text(
            (
                new_x,
                current_drawing_position,
            ),
            text,
            fill="white",
            font=text_font_size,
        )
        current_drawing_position += text_height + line_padding

        # add umbrella rain icon
        if round(forecast_data["hourly"]["precipitation_probability"][hour]) >= 0:
            umbrella_icon_path = icons_path + "umbrella.png"
            rain_probability_text = (
                str(round(forecast_data["hourly"]["precipitation_probability"][hour]))
                + "%"
            )
            # measure rain prob text
            font_size = settings.SMALLER_FONT
            new_text_x, text_width, text_height = centreTextHorizontally(
                draw,
                rain_probability_text,
                font_size,
                sb_x,
                settings.screen_width,
            )
            # rain prob icon
            section_width = settings.sidebar_width
            icon_size = settings.SMALLER_ICON_SIZE
            edge_padding_x = (section_width - icon_size[1] - text_width) / 2

            icon_start_x = round(sb_x + edge_padding_x)
            text_start_x = round(icon_start_x + icon_size[0])

            _, umbrella_icon = setup_icon_image(umbrella_icon_path, icon_size)
            image.paste(
                umbrella_icon,
                (
                    icon_start_x,
                    current_drawing_position,
                ),
                umbrella_icon,
            )

            # add rain probability text
            draw.text(
                (
                    text_start_x,
                    current_drawing_position,
                ),
                rain_probability_text,
                fill="white",
                font=font_size,
            )
            current_drawing_position += icon_size[1]

        # add uv level
        if (
            round(forecast_data["hourly"]["uv_index"][hour]) >= 0
        ):  # 2: #if uv index is 3+
            text = "UV " + str(round(forecast_data["hourly"]["uv_index"][hour]))
            text_font_size = settings.SMALLER_FONT
            new_x, text_width, text_height = centreTextHorizontally(
                draw, text, text_font_size, sb_x, settings.screen_width
            )
            draw.text(
                (
                    new_x,
                    current_drawing_position,
                ),
                text,
                fill="white",
                font=text_font_size,
            )

        current_drawing_position += text_height

    # print(sidebar_forecast)
    return image


def addEmptySidebar(image):
    sb_x = settings.map_display_width
    sb_y = 0

    sidebar = Image.new(
        "RGBA",
        (settings.sidebar_width, settings.sidebar_height),
        "black",
    )
    image.paste(sidebar, (sb_x, sb_y))
    return image


def isDayNight(hour, forecast_data):
    day_night_icon = (
        "day_icon" if forecast_data["hourly"]["is_day"][hour] == 1 else "night_icon"
    )
    return day_night_icon


def addWeatherDescriptions(image, forecast_data, forecast_location):
    (x, y) = (100, 140)  # 80)  # starting position on screen
    current_y = y
    line_padding = 4

    draw = ImageDraw.Draw(image)
    # day of week

    this_year, this_month, todays_date, hhmm = (
        forecast_data["current_weather"]["time"].replace("T", "-").split("-")
    )
    this_year = str(this_year)
    this_month = str(this_month)
    todays_date = str(todays_date)

    location = forecast_location
    text_str = str(location) + str(", ") + str(todays_date) + "/" + str(this_month)

    # main weather icon setup
    day_night_icon = (
        "day_icon" if forecast_data["current_weather"]["is_day"] == 1 else "night_icon"
    )
    main_weather_icon_path = (
        settings.icon_path
        + forecast.weather_codes[forecast_data["current_weather"]["weathercode"]][
            day_night_icon
        ]
    )

    icon_size = settings.LARGE_ICON_SIZE
    font_size = settings.LARGE_FONT
    main_icon, _ = setup_icon_image(main_weather_icon_path, icon_size)

    # add main/current weather icon image to base image
    start_x = 0
    end_x = settings.map_display_width
    centered_text_x, text_w, text_h = centreTextHorizontally(
        draw, text_str, font_size, start_x, end_x
    )

    edge_padding_x = (end_x - icon_size[1] - text_w) / 2
    icon_start_x = round(start_x + edge_padding_x)
    text_start_x = round(icon_start_x + icon_size[0])

    image.paste(main_icon, (icon_start_x, y - 15), main_icon)

    # add day text
    draw.text(
        (text_start_x, current_y),
        text_str,
        fill="black",
        font=font_size,
    )

    current_y += text_h + line_padding
    text_str = forecast.weather_codes[forecast_data["current_weather"]["weathercode"]][
        "desc"
    ]

    font_size = settings.MED_FONT
    centered_text_x, text_w, text_h = centreTextHorizontally(
        draw, text_str, font_size, start_x, end_x
    )

    draw.text(
        (centered_text_x, current_y),  # + 60),
        text_str,
        fill="black",
        font=font_size,
    )
    current_y += text_h + line_padding

    # ADD CURRENT TEMP
    text_str = str(round(forecast_data["current_weather"]["temperature"])) + "°"

    font_size = settings.LARGE_FONT
    x_end = settings.map_display_width
    new_x, text_width, text_height = centreTextHorizontally(
        draw, text_str, font_size, 0, x_end
    )
    draw.text(
        (new_x, current_y),
        text_str,
        fill="black",
        font=font_size,
    )
    # current_y += text_height + line_padding
    current_y += 10
    # add sunrise/sunset
    sunrise_icon_path = settings.icon_path + "sunrise.png"
    sunrise_time = forecast_data["daily"]["sunrise"][0].replace("T", ":").split(":")
    hour, min = sunrise_time[1], sunrise_time[2]
    text_str = f"{hour}:{min}"
    icon_size = settings.SMALL_ICON_SIZE
    font_size = settings.SMALL_FONT
    x_start = 70  # 100
    x_end = settings.map_display_width / 2

    y_offset = placeIconAndData(
        draw,
        image,
        current_y,
        x_start,
        x_end,
        sunrise_icon_path,
        text_str,
        icon_size,
        font_size,
    )

    sunset_icon_path = settings.icon_path + "sunset.png"
    sunset_time = forecast_data["daily"]["sunset"][0].replace("T", ":").split(":")
    hour, min = sunset_time[1], sunset_time[2]
    text_str = f"{hour}:{min}"
    x_end = settings.map_display_width - x_start

    x_start = round(settings.map_display_width / 2)

    y_offset = placeIconAndData(
        draw,
        image,
        current_y,
        x_start,
        x_end,
        sunset_icon_path,
        text_str,
        icon_size,
        font_size,
    )

    return image


def centreTextHorizontally(draw, text, font, x_start, x_end):
    text_length = draw.textlength(text, font=font)

    section_width = x_end - x_start
    new_start_pos_x = (section_width / 2) - (text_length / 2) + x_start
    centered_text_x = round(new_start_pos_x)

    _, _, w, h = draw.textbbox((0, 0), text, font=font)

    return centered_text_x, w, h


def centreIconHorizontally(icon_width, x_start, x_end):
    section_pos = x_end - x_start
    new_start_pos_x = (section_pos / 2) - (icon_width / 2) + x_start
    centered_icon_x = round(new_start_pos_x)
    return centered_icon_x


def addErrorMessage(image):
    x, y = (20, 40)  # starting position on screen

    draw = ImageDraw.Draw(image)
    # day of week

    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    except:
        current_time = ""
    error_message = f"{current_time} Error retrieving forecast!"
    text_str = str(error_message)

    draw.text(
        (x, y),
        text_str,
        fill="black",
        font=settings.SMALLER_FONT,
    )

    return image


def addRadarErrorMessage(image):
    (x, y) = (20, 10)  # starting position on screen
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    except:
        current_time = ""
    draw = ImageDraw.Draw(image)
    error_message = f"{current_time} Error retrieving radar images!"
    text_str = str(error_message)

    draw.text(
        (x, y),
        text_str,
        fill="black",
        font=settings.SMALLER_FONT,
    )
    return image


def addWeatherWarnings(image, weather_warning_data):
    draw = ImageDraw.Draw(image)

    y = 950 if len(weather_warning_data) == 1 else 920
    x = 0
    current_y = y
    icon_path = settings.icon_path + "warning.png"  # "warning_no_transparency.png"

    small_font_size = settings.SMALL_FONT
    smaller_font_size = settings.SMALLER_FONT
    icon_size = settings.SMALL_ICON_SIZE

    for warning in range(len(weather_warning_data)):
        text_str = f"{weather_warning_data[warning]['level']} {weather_warning_data[warning]['type']} {weather_warning_data[warning]['status']}"
        y_offset = placeIconAndData(
            draw,
            image,
            current_y,
            0,
            settings.map_display_width,
            icon_path,
            text_str,
            icon_size,
            small_font_size,
        )

        current_y += y_offset

        onset = prs.parse(weather_warning_data[warning]["onset"])
        onset_str = f"{onset:%H:%M} {onset:%d/%m}"

        expiry = prs.parse(weather_warning_data[warning]["expiry"])
        expiry_str = f"{expiry:%H:%M} {expiry:%d/%m}"

        text_str = f"{onset_str} - {expiry_str}"
        centred_x, w, h = centreTextHorizontally(
            draw=draw,
            font=smaller_font_size,
            text=text_str,
            x_start=0,
            x_end=settings.map_display_width,
        )
        draw.text(
            (centred_x, current_y),
            text_str,
            fill="black",
            font=smaller_font_size,
        )

        current_y += y_offset

    return image


def addCurrentConditions(image, forecast_data):
    draw = ImageDraw.Draw(image)
    # starting position on screen
    y = 1130
    line_padding = 4
    padding = 25
    icon_offset = 3

    font = settings.MED_FONT
    icon_size = settings.ALMOST_MED_ICON_SIZE

    current_hour = forecast_data["current_weather"]["time"].replace("T", ":").split(":")
    current_hour = int(current_hour[1])

    icon_path = settings.icon_path + "umbrella.png"
    icon, _ = setup_icon_image(icon_path, icon_size)
    precip_str = (
        str(forecast_data["hourly"]["precipitation_probability"][current_hour])
        + forecast_data["hourly_units"]["precipitation_probability"]
    )
    humidity_str = (
        str(forecast_data["hourly"]["relativehumidity_2m"][current_hour])
        + forecast_data["hourly_units"]["relativehumidity_2m"]
    )
    cloudy_str = (
        str(forecast_data["hourly"]["cloudcover"][current_hour])
        + forecast_data["hourly_units"]["cloudcover"]
    )
    uv_str = "UV " + str(round(forecast_data["hourly"]["uv_index"][current_hour]))
    wind_str = (
        str(round(forecast_data["current_weather"]["windspeed"]))
        + forecast_data["hourly_units"]["windspeed_10m"]
    )
    wind_deg = forecast_data["current_weather"]["winddirection"]

    """ #test data
    precip_str = "100%"
    humidity_str = "100%"
    cloudy_str = "100%"
    uv_str = "UV 0"
    wind_str = "250km/h"
    """

    conditions = {
        0: {
            "condition_type": "precipitation_probability",
            "condition_icon": "umbrella.png",
            "condition_string": precip_str,
            "condition_str_len": 0,
        },
        1: {
            "condition_type": "humidity",
            "condition_icon": "humidity.png",
            "condition_string": humidity_str,
            "condition_str_len": 0,
        },
        2: {
            "condition_type": "cloud_cover",
            "condition_icon": "cloudy.png",
            "condition_string": cloudy_str,
            "condition_str_len": 0,
        },
        3: {
            "condition_type": "uv",
            "condition_string": uv_str,
            "condition_str_len": 0,
        },
        4: {
            "condition_type": "wind",
            "condition_icon": "wind-deg-crop.png",
            "condition_string": wind_str,
            "wind_deg": wind_deg,
            "condition_str_len": 0,
        },
    }

    total_text_length = 0
    for condition in range(len(conditions)):
        _, _, w, h = draw.textbbox(
            (0, 0), conditions[condition]["condition_string"], font=font
        )
        total_text_length += int(w)
        conditions[condition]["condition_str_len"] = w

    n = (
        len(conditions) - 1
    )  # only 4 icons, only 4 padding spaces in between data blocks
    total_text_length += icon_size[1] * n
    while total_text_length + padding * n > settings.map_display_width:
        padding = padding - 2

    total_text_length += padding * n
    current_x = round((settings.map_display_width - total_text_length) / 2)

    for condition in range(len(conditions)):
        # print icon
        if conditions[condition]["condition_type"] == "wind":
            icon_path = settings.icon_path + conditions[condition]["condition_icon"]
            icon_size = settings.ALMOST_SMALL_ICON_SIZE
            icon, _ = setup_icon_image(icon_path, icon_size)
            icon = icon.convert("RGBA")
            icon = icon.rotate(
                conditions[condition]["wind_deg"], resample=Image.BICUBIC, expand=False
            )
            image.paste(icon, (current_x, y + 5), icon)
            current_x += icon_size[1] + line_padding

        elif conditions[condition]["condition_type"] != "uv":
            icon_path = settings.icon_path + conditions[condition]["condition_icon"]
            icon, _ = setup_icon_image(icon_path, icon_size)
            image.paste(icon, (current_x, y - icon_offset), icon)
            current_x += icon_size[1]

        if conditions[condition]["condition_type"] == "uv":
            current_x += line_padding

        if conditions[condition]["condition_type"] == "humidity":
            current_x = current_x - 6

        # print text
        draw.text(
            (current_x, y),
            conditions[condition]["condition_string"],
            fill="black",
            font=font,
        )
        if conditions[condition]["condition_type"] == "uv":
            current_x += line_padding

        current_x += conditions[condition]["condition_str_len"] + padding

    return image


def placeIconAndData(
    draw, image, ypos, start_x, end_x, icon_path, text_str, icon_size, font_size
):
    weather_icon_path = icon_path
    icon, _ = setup_icon_image(weather_icon_path, icon_size)

    centered_text_x, text_w, text_h = centreTextHorizontally(
        draw, text_str, font_size, start_x, end_x
    )

    edge_padding_x = (end_x - start_x - icon_size[1] - text_w) / 2
    icon_start_x = round(start_x + edge_padding_x)
    text_start_x = round(icon_start_x + icon_size[0])

    image.paste(icon, (icon_start_x, ypos), icon)
    draw.text(
        (text_start_x, ypos + 5),
        text_str,
        fill="black",
        font=font_size,
    )
    return icon_size[1]  # text_h # offset for icon height


def amPmDayNight(hour):
    am_pm = "pm" if hour > 11 else "am"
    return am_pm


def setup_icon_image(icon_path, icon_size):
    icon = Image.open(icon_path)
    icon = icon.convert("RGBA")
    icon = icon.resize(icon_size)

    # invert b&w to make transparent image to overlay on white or black background
    icon_mask = icon
    r, g, b, a = icon_mask.split()
    rgb_image = Image.merge("RGB", (r, g, b))
    inverted_image = ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    icon_mask = Image.merge("RGBA", (r2, g2, b2, a))

    return icon, icon_mask


def run(location):
    # location = "Rathmines"  # "Killinga", "Rathmines" or "Braunschweig"

    country = settings.forecast_locations[location]["country"]
    radar_error = False
    try:
        radar_img_fn = weathermap.makeRadarMap(country)

    except Exception as e:
        print("error retrieving radar images")
        # print(e)
        radar_img_fn = settings.base_map_path.format(country=country)
        radar_error = True
    # trace_back = sys.exc_info()[2]
    # line = trace_back.tb_lineno
    # raise Exception("Exception", e)

    image = Image.open(radar_img_fn)

    if radar_error:
        image = addRadarErrorMessage(image)

    try:
        "Weather warnings"
        if country == "Ireland":
            weather_warnings = forecast.getWeatherWarnings(
                settings.forecast_locations[location]["region"]
            )
            # print(f"Weather warnings: {weather_warnings}")

            if weather_warnings != []:
                image = addWeatherWarnings(image, weather_warnings)

    except Exception as e:
        print("error getting weather warnings")
    # trace_back = sys.exc_info()[2]
    # line = trace_back.tb_lineno
    # raise Exception("Process Exception in line {}".format(line), e)

    try:
        # print(settings.forecast_locations[location]["coords"])
        forecast_data = forecast.getForecast(
            settings.forecast_locations[location]["coords"]
        )

        image = addSidebar(image, forecast_data)
        image = addWeatherDescriptions(image, forecast_data, forecast_location=location)
        image = addCurrentConditions(image, forecast_data)

    except Exception as e:
        image = addEmptySidebar(image)
        image = addErrorMessage(image)

        # trace_back = sys.exc_info()[2]
        # line = trace_back.tb_lineno
        # raise Exception("Process Exception in line {}".format(line), e)

    # image.save("sidebar_img", "BMP")
    image.save(settings.weathermap_bmp_path, "BMP")


if __name__ == "__main__":
    # location = "Killinga"  # "Killinga", "Rathmines" or "Braunschweig"
    parser = optparse.OptionParser()  # argparse.ArgumentParser()
    parser.add_option(
        "--weather-location",
        help="Give one of the preset locations: Rathmines, Killinga, Braunschweig",
        default="Terenure",
    )
    (opts, args) = parser.parse_args()
    location = opts.weather_location
    # location = "Braunschweig"
    run(location)
