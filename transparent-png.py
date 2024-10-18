from PIL import Image, ImageOps
import numpy as np
import os
from os import listdir

# get the path/directory
folder_dir = "icons-transparent"
for image in os.listdir(folder_dir):
    # check if the image ends with png
    if image.endswith(".jpg"):
        fn = folder_dir + "/" + image
        print(fn)

        img = Image.open(fn)
        img = img.convert("RGBA")

        imgnp = np.array(img)

        white = np.sum(imgnp[:, :, :3], axis=2)
        white_mask = np.where(white == 255 * 3, 1, 0)

        alpha = np.where(white_mask, 0, imgnp[:, :, -1])

        imgnp[:, :, -1] = alpha

        img = Image.fromarray(np.uint8(imgnp))
       
        img.save(fn, "PNG")
