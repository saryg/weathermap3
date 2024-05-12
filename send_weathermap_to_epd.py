import send_image_to_epd
import settings
import time
import os 

while True:

    os.system('python /home/sara/Weathermap3/weathermap_builder.py')



    img_path = settings.weathermap_bmp_path
    send_image_to_epd.send_weathermap_to_epd(img_path)
    print("Next update in 10 mins...")
    time.sleep(600)
