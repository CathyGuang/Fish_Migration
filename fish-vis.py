import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib import ticker
import dataparse as dp
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import grid as g

fig = plt.figure(figsize=(7, 7))

ax = fig.add_subplot()

plt.xlabel("Longitude")
plt.ylabel("Latitude")

arr = g.build_vis_arr(60)

arr = np.array(arr)
print(arr[10])

im = plt.imshow(arr[0], animated=True, cmap=plt.cm.get_cmap('BuPu'))
cb = fig.colorbar(im)
tick_locator = ticker.MaxNLocator(nbins = 5)
cb.locator = tick_locator
cb.update_ticks()
i = 0

def updatefig(*args):
    global i
    if (i<61):
        i += 1
    else:
        i=0
    vmin = np.nanmin(arr[i])
    vmax = np.nanmax(arr[i])

    im.set_array(arr[i])
    if i % 6 == 0:
        im.set_clim(vmin, vmax)
    
    #norm = mpl.colors.Normalize(vmin = np.min(arr[i]), vmax = np.max(arr[i]))
    if i > 12:
        if i % 12 == 0:
            plt.title(f'Year: {int(i/12)}, Month: 12')
        else:
            plt.title(f'Year: {int(i/12)}, Month: {i%12}')
    else:
        plt.title(f'Month: {i}')
    #cb = plt.colorbar(mpl.cm.ScalarMappable(norm = norm))
    return im,

anim = animation.FuncAnimation(fig, updatefig,  blit=True)
plt.show()

