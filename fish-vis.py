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

arr = g.build_vis_arr(601)

arr = np.array(arr)

im = plt.imshow(arr[0], animated=True, cmap=plt.cm.get_cmap('BuPu'))

im.set_clim(0, 800)
cb = fig.colorbar(im)

i = 0

def updatefig(*args):
    global i
    # print(i)
    if (i<601):
        i += 1
    else:
        i=0

    im.set_array(arr[i])
  
    im.set_clim(0, 800)
    
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

