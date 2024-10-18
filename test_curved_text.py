import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import text as mtext
import numpy as np
import settings
import cartopy.crs as ccrs
import matplotlib as mpl

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredAuxTransformBox
from matplotlib.patheffects import withStroke

# Sample coordinates
coords = [53.3203, -6.2783]

# Plotting
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

ax.plot(
    [coords[1]],  # reverse lat, lon order
    [coords[0]],
    markeredgecolor="black",
    markerfacecolor="darkgray",
    marker="o",
    markersize=7,
    fillstyle="full",
    transform=ccrs.PlateCarree(),
)

# Adding curved text label
N = 100
curve_x = -np.cos(np.linspace(0, 2 * np.pi, N))
curve_y = np.sin(np.linspace(0, 2 * np.pi, N))
text = "Your Label"

# Create a curved path
path = ax.transData.transform(np.vstack([curve_x, curve_y]).T)
path = path[:, :2]

# Calculate the rotation angle for the labels
angles = np.arctan2(path[1:, 1] - path[:-1, 1], path[1:, 0] - path[:-1, 0])
angles = np.degrees(angles)

# Create a TextPath for the labels
tp = mpl.textpath.TextPath((0, 0), text, size=8)

# Add labels along the curved path
for i, angle in enumerate(angles):
    text = mpl.text.TextPath((0, 0), text, size=8, path_effects=[withStroke(foreground="w", linewidth=3)])
    trans = mpl.transforms.Affine2D().rotate_deg(angle)
    text.set_transform(trans + ax.transData)

    # Create an AnchoredAuxTransformBox for positioning the label
    bbox = mpl.transforms.Bbox.from_bounds(path[i, 0], path[i, 1], 0.1, 0.1)
    ab = AnchoredAuxTransformBox(ax.transData, bbox, loc='center')
    ab.add_artist(text)
    ax.add_artist(ab)

plt.show()


plt.savefig("curved_text.png")
