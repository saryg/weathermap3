import streamlit as st
import folium
import sys, os

from streamlit_folium import st_folium

sys.path.append(os.path.abspath("../"))
import settings


def main():
    country = "Ireland"
    lon = settings.map_settings[country]["centre_lon"]
    lat = settings.map_settings[country]["centre_lat"]
    center = [lat, lon]

    # State variables
    if "center" not in st.session_state:
        st.session_state.center = center # [45.503032, -73.566424]

    if "zoom" not in st.session_state:
        st.session_state.zoom = 6

#    if "location" not in st.session_state:
#        st.session_state.location = folium.Marker(st.session_state.center)

    # Map creation
    
    m = folium.Map(location=st.session_state.center, zoom_start=st.session_state.zoom)
    #fg = folium.FeatureGroup(name="Markers")
    for place, coords in settings.map_settings[country]["points_of_interest"].items():
            # print(place)
        location_info = f"{place}\n{coords}".format(place=place, coords=coords)
        folium.Marker(
            [coords[0], coords[1]], popup=location_info, tooltip=location_info
        ).add_to(m)

    
        #fg.add_child(st.session_state.location)


    # When the user interacts with the map
    map_state_change = st_folium(
        m,
       # feature_group_to_add=fg,
        height=800,
        width="100%",
        returned_objects=["last_clicked", "zoom", "bounds", "center"],
    )

    # If the interaction includes a click
    if map_state_change["last_clicked"]:
        loc = map_state_change["last_clicked"]
        st.session_state.location = folium.Marker([loc["lat"], loc["lng"]])
        print(loc)
        bounds = map_state_change["bounds"]

        #st.experimental_rerun()
        folium.Marker([loc["lat"], loc["lng"]], popup="Camp Muir").add_to(m)
        #m.add_child(folium.ClickForMarker(popup="Waypoint"))
       
        st.experimental_rerun()

# print("Bounds", bounds)

if __name__ == "__main__":
    main()
