# For ImageJ/Fiji
from ij import IJ, ImagePlus, 'plugin.frame'
import inspect
import pprint as pp

imp = IJ.getImage()

a = inspect.getmembers(imp)
print(a)


## test
from ij import WindowManager as wm
wm.closeAllWindows("Others")

import inspect
from ij import IJ, ImagePlus
from ij import WindowManager as wm
IJ.selectWindow('ThunderSTORM: results')
a = wm.getCurrentWindow()

b = inspect.getmembers(a)
print(b)


'''
a = wm.getWindow('ThunderSTORM: results')
a.close()
'''

# %%
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('kodim23.png')
print(img.shape)

lum_img = img[:, :, 0]
imgplot = plt.imshow(lum_img, cmap="gray")
plt.colorbar()

# %%
plt.hist(lum_img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')

# %%
imgplot = plt.imshow(lum_img, cmap="gray", clim= (0.2, 0.7))
plt.colorbar()

