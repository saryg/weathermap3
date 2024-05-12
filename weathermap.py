import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import mercantile
import shapefile
from shapely.geometry import shape
import requests
import pickle
from PIL import Image
from io import BytesIO

import settings

# RADAR_MAP_FN = "radar_map.png"


def createBaseMap(country):
    focus_countries, non_focus_countries = countryMapShape(country)

    # Create a Mercator projection centered on Country
    proj = ccrs.Mercator(central_longitude=settings.map_settings[country]["centre_lon"])

    my_dpi = settings.dpi  # 150
    width = settings.screen_width
    height = settings.screen_height

    fig, ax = plt.subplots(
        figsize=(width / my_dpi, height / my_dpi),
        dpi=my_dpi,
        subplot_kw={"projection": proj},
    )

    ax.set_extent(settings.map_settings[country]["extent"])

    # Plot focus countries ([IE, NIR] or [DEU]),  and non focus countries
    ax.add_geometries(
        non_focus_countries,
        ccrs.PlateCarree(),
        edgecolor="grey",
        facecolor="#f9f9f9",
        linewidth=0.25,
    )
    # Focus countries
    ax.add_geometries(
        focus_countries,
        ccrs.PlateCarree(),
        edgecolor="black",
        facecolor="none",
        linewidth=1,
    )

    # ax.coastlines(resolution='10m', color='red', linewidth=0.25)
    # ax.add_feature(cfeature.BORDERS, color='blue', linewidth=0.25)

    for place, coords in settings.map_settings[country]["points_of_interest"].items():
        print(f"{place}:  [{coords[0]}, {coords[1]}]")
        marker_style = "o"
        if settings.map_settings[country]["forecast_location"] == place:
            marker_style = "o"
        ax.plot(
            [coords[1]],  # reverse lat, lon order
            [coords[0]],
            markeredgecolor="black",
            markerfacecolor="darkgray",
            marker=marker_style,
            markersize=7,
            fillstyle="full",
            transform=ccrs.PlateCarree(),
        )

    plt.gca().set_position([0, 0, 1, 1])  # keeps px size and fills all space

    # Save a pickle to use when adding radar
    pickle_fn = settings.pickle_path.format(country=country)
    with open(pickle_fn, "wb") as f:
        pickle.dump(ax, f)
    print(f"Saved pickle of base map of {country}.")
    plt.savefig(settings.base_map_path.format(country=country))
    return ax


def loadOrCreateBaseMapPickle(country):
    pickle_fn = settings.pickle_path.format(country=country)

    try:
        with open(pickle_fn, "rb") as f:
            ax = pickle.load(f)
    except:
        print("Base map pickle not found. Creating...")
        ax = createBaseMap(country)

    return ax


def makeRadarMap(country):
    # Load pickle base map with point of interest
    ax = loadOrCreateBaseMapPickle(country)

    # Get zoom and tile range for radar coverage
    z = settings.map_settings[country]["zoom"]
    tile_resolution = settings.map_settings[country]["tiles"][z]
    gmt_tile_range_x = tile_resolution["xrange"]
    gmt_tile_range_y = tile_resolution["yrange"]

    tile_bounds = []
    timestamp = getTileTimestamp()
    print(timestamp)

    for i in range(len(gmt_tile_range_x)):
        x = gmt_tile_range_x[i]
        for j in range(len(gmt_tile_range_y)):
            y = gmt_tile_range_y[j]

            print(x, y, z)
            tiles = mercantile.Tile(x, y, z)
            tile_bounds = mercantile.bounds(tiles)

            # Read in the radar image
            radar_img = getTile(x, y, z, timestamp)

            # Add the radar image to the map
            ax.imshow(
                radar_img,
                extent=(tile_bounds[0], tile_bounds[2], tile_bounds[1], tile_bounds[3]),
                transform=ccrs.PlateCarree(),
            )
    plt.gca().set_position([0, 0, 1, 1])
    plt.savefig(settings.radar_map_path)
    return settings.radar_map_path


def getTileTimestamp():
    # Get the most recent radar timestamp
    try:
        response = requests.get(settings.rainviewer_timestamp_url)
        timestamp = response.json()["radar"]["past"][-1]["time"]

        return timestamp

    except Exception as e:
        print(e)


def getTile(x, y, z, timestamp):
    try:
        # Get the radar tile image
        url = settings.rainviewer_radar_tile_url.format(
            timestamp=timestamp, x=x, y=y, z=z
        )

        response = requests.get(url)

        # Open the radar tile image
        radar_img = Image.open(BytesIO(response.content)).convert("RGBA")
        return radar_img

    except Exception as e:
        print(e)


def countryMapShape(country):
    # Load the shapefile
    sf = shapefile.Reader(settings.map_unit_shapefile_path)

    # Get the shapes and records for each feature
    shapes = sf.shapes()
    records = sf.records()

    focus_countries = []
    non_focus_countries = []
    focus_country_codes = []
    non_focus_country_codes = []

    focus_country_codes = settings.map_settings[country]["focus_country_codes"]
    non_focus_country_codes = settings.map_settings[country]["non_focus_country_codes"]

    for country_code in focus_country_codes:
        country_idx = [i for i in range(len(records)) if records[i][16] == country_code]

        for idx in country_idx:
            country_shape = shapes[idx]
            acountry = shape(country_shape)
            focus_countries.append(acountry)

    for country_code in non_focus_country_codes:
        country_idx = [i for i in range(len(records)) if records[i][16] == country_code]
        if country_idx == []:
            country_idx = [
                i for i in range(len(records)) if records[i][10] == country_code
            ]

        for idx in country_idx:
            country_shape = shapes[idx]  # country_idx[0]]
            acountry = shape(country_shape)
            non_focus_countries.append(acountry)

    return focus_countries, non_focus_countries


def main():

    country = "Ireland"  # "Ireland" or "Germany"
    createBaseMap(country)
    base_radar_map_image = makeRadarMap(country)
   

if __name__ == "__main__":
    main()
