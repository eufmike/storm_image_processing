# %%
import os, sys
from PIL import Image
from pylab import *

# create input folder
path = '/Users/michaelshih/Desktop/'
filename = 'IMG_4015.jpeg'
filepath = os.path.join(path, filename)
pil_im = Image.open(filepath)
pil_im.show()






