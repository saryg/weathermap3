import weathermap_builder
import time


if __name__ == "__main__":
    args = weathermap_builder.parse_args()

    args.radar = True
    args.forecast = True
    args.sidebar = True
    args.current_conditions = True
    args.weather_location = "Terenure"  # location = "Killinga"  # "Killinga", "Rathmines" or "Braunschweig"
    args.map_country = "Ireland"  # Country = Ireland, Germany
    args.subtle = True
    args.warnings=True

   # while True:
      #  weathermap_builder.run(args)
     #   print("Sleeping for 10 mins...")
    #    time.sleep(600)  # sleep 10 mins


    weathermap_builder.run(args)
