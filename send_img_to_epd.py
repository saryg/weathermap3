from time import sleep
import argparse

import sys

from IT8951.display import AutoEPDDisplay
from IT8951.functions import display_image, clear_display


def parse_args():
    p = argparse.ArgumentParser(description='EPD Display BMP image')

    p.add_argument('-f', '--file', default='', help='BMP file to be displayed')
    p.add_argument('-r', '--rotate', default='CCW', choices=['CW', 'CCW', 'flip'],
                   help='Send a BMP image to the display')
    p.add_argument("-c", "--clear", help="Clear and reset the EPD display.",
                    action="store_true")
    return p.parse_args()


def main():
    args = parse_args()

    if args.clear:
        display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=False, spi_hz=24000000)
        clear_display(display)


    if args.file: 
        img_path = args.file

        display = AutoEPDDisplay(vcom=-2.15, rotate=args.rotate, mirror=False, spi_hz=24000000)
        print('VCOM set to', display.epd.get_vcom())
        display_image(img_path, display)
 
    else:
        print("Error: No file name")

if __name__ == '__main__':
    main()
