from PIL import Image, ImageDraw, ImageFont
from time import sleep
import argparse


from pathlib import Path
import sys

sys.path.insert(0, '/home/sara/IT8951')

from IT8951 import constants #display

def parse_args():
    p = argparse.ArgumentParser(description='Test EPD functionality')
    p.add_argument('-v', '--virtual', action='store_true',
                   help='display using a Tkinter window instead of the '
                        'actual e-paper device (for testing without a '
                        'physical device)')
    p.add_argument('-r', '--rotate', default=None, choices=['CW', 'CCW', 'flip'],
                   help='run the tests with the display rotated by the specified value')
    p.add_argument('-m', '--mirror', action='store_true',
                   help='Mirror the display (use this if text appears backwards)')

    p.add_argument('-i', '--image', default = None, help="Image file to be displayed")

    return p.parse_args()

def main():

    args = parse_args()

    tests = []

    if not args.virtual:
        from IT8951.display import AutoEPDDisplay

        print('Initializing EPD...')

        # here, spi_hz controls the rate of data transfer to the device, so a higher
        # value means faster display refreshes. the documentation for the IT8951 device
        # says the max is 24 MHz (24000000), but my device seems to still work as high as
        # 80 MHz (80000000)
        display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=args.mirror, spi_hz=24000000)

        print('VCOM set to', display.epd.get_vcom())

        #display.clear()

        
        display_image_8bpp(display, args.image)
       # partial_update(display, args.image)


    else:
        from IT8951.display import VirtualEPDDisplay
        display = VirtualEPDDisplay(dims=(1200, 800), rotate=args.rotate, mirror=args.mirror)


def send_weathermap_to_epd(img_path):

     from IT8951.display import AutoEPDDisplay

     print('Initializing EPD...')

     # here, spi_hz controls the rate of data transfer to the device, so a higher
     # value means faster display refreshes. the documentation for the IT8951 device
     # says the max is 24 MHz (24000000), but my device seems to still work as high as
     # 80 MHz (80000000)
     display = AutoEPDDisplay(vcom=-2.15, rotate="CCW",  spi_hz=24000000)

     print('VCOM set to', display.epd.get_vcom())

     #display.clear()


     display_image_8bpp(display, img_path)

     print("Image sent")

def display_image_8bpp(display, img_path):
    #img_path = 'images/sleeping_penguin.png'
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = Image.open(img_path)

    # TODO: this should be built-in
    dims = (display.width, display.height)

    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)



def partial_update(display, img_path):
    print('Starting partial update...')


   # display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = Image.open(img_path)

    # TODO: this should be built-in
    dims = (display.width, display.height)

    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)


    display.draw_partial(constants.DisplayModes.DU)


if __name__ == '__main__':
    main()
