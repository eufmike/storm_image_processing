# --------------------------------------------------------------- # 
# By Michael Shih
# Update: 01/16/2019

# This part of test code demostrates several basic methods to 
# load images, including:
# 1. PIL
# 2. OpenCV (load cv2)
# 3. skimage
# Note:
# They all get loaded as a numpy array so we can process images 
# under the scipy/numpy framework. 
# It is worthwhile to eplore into OpenCV.
# --------------------------------------------------------------- # 

# %%
# test: PIL
import os, sys
import numpy
from PIL import Image

# %%
# create input folder
path = '/Users/michaelshih/Desktop/'
filename = 'IMG_4015.jpeg'
filepath = os.path.join(path, filename)

# load the image
pil_im = Image.open(filepath)

# %%
# show the image
pil_im.show()

# %%
# use pylab to convert the image into an array
import pylab
im_pylab = pylab.array(pil_im) 

# pylab.array directly convert the image into numpy array
print(type(im_pylab))

# %%
# size of array
print(im_pylab.shape)

# %%
# test: OpenCV
import os, sys
import numpy
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

path = '/Users/michaelshih/Desktop/'
filename = 'IMG_4015.jpeg'
filepath = os.path.join(path, filename)

im_cv2 = cv2.imread(filepath)
print(type(im_cv2))

# %%
my_dpi = 96
plt.figure(figsize=(7, 7), dpi = my_dpi)
plt.imshow(cv2.cvtColor(im_cv2, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()

# %%
# test: matplotlib 
import os, sys
import numpy
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

path = '/Users/michaelshih/Desktop/'
filename = 'IMG_4015.jpeg'
filepath = os.path.join(path, filename)

im_mpimg = mpimg.imread(filepath)
print(type(im_mpimg))

# %%
my_dpi = 96
plt.figure(figsize=(7, 7), dpi = my_dpi)
plt.imshow(im_mpimg)
plt.axis("off")
plt.show()


# --------------------------------------------------------------- # 
# By Michael Shih
# Update: 01/16/2019

# This part of test code demostrates how to load our STORM 
# multidimensional tiff as a numpy array
# 1. load through skimage
# 2. show by ImageViewer
# 
# Ongoing
# 1. it still can not display multiple tiff
# 2. not histogram adjustment
# note: potential solution can be to us the plugin framework provided
# by skimage. 

# --------------------------------------------------------------- # 
# %%
import os
import sys
import numpy as np
import cv2
from skimage import io
from skimage.viewer import ImageViewer
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.viewer.plugins.lineprofile import LineProfile
# from PIL import Image
# import imageio

# create input folder
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_012019'
image_dir = 'crop_img'
inputfilepath = os.path.join(path, analysis_dir,image_dir)

# %%
inputfilelist = []
inputfileabslist = []
for directory, dir_names, file_names in os.walk(inputfilepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.tif')):
			filepath_tmp =  os.path.join(directory, file_name)
			inputfilelist.append(file_name)
			inputfileabslist.append(filepath_tmp)
print(inputfilelist)
print(inputfileabslist)
print(len(inputfilelist))

# %%
i = 1
testfilepath = inputfileabslist[i]

# test on skimage
# work well on loading the stack tiff
im_skim = io.imread(testfilepath)
print(im_skim.shape)
imsliced = im_skim[0, :, :]
print(imsliced.shape)



# %%
# use tifffile under skimage
from skimage.external import tifffile
import re
im_skim_tf = tifffile.imread(testfilepath, key= 0)
print(im_skim_tf.shape)

# %%
with tifffile.TiffFile(testfilepath) as tif: 
	imagej_hyperstack = tif.asarray()
	imagej_metadata = tif.is_imagej
	
# print(imagej_hyperstack)
# %%
imagej_metadata = str(imagej_metadata)
m = re.search("'(.+?)'", imagej_metadata)
if m:
	metadata = m.group(1)
metadata = metadata.split('\\n')

# %%
metadata_tmp = []
for i in metadata:
	if len(i) > 0 :
		metadata_tmp.append(i)
metadata = metadata_tmp

# %%
imgmetadata = {}
for i in metadata:
	a, b = i.split('=')
	imgmetadata[a] = b
print(imgmetadata)	
	
# %%

tif.close




# %%
# ImageViewer from skimage
# sliced (working)
viewer1 = ImageViewer(imsliced) 
# add on
viewer1 += LineProfile(viewer1)
overlay, data = viewer1.show()[0]

# %%
# whole stack
# This one has failed with unkown reason
# viewer2 = ImageViewer(im_skim)
# viewer2.show()
# %%
# test: Bioformats
import javabridge as jv
import bioformats as bf
jv.start_vm(class_path=bf.JARS)


# md = bf.get_omexml_metadata()



# %%
'''
for i in range(len(inputfilelist)):
	
	# test on OpenCV
	im_cv2 = cv2.imread(inputfileabslist[i])
	print(type(im_cv2))
	print(im_cv2.shape)

	# test on PIL
	im_PIL = Image.open(inputfileabslist[i])
	im_array = np.asarray(im_PIL)
	print(im_array.shape)

	# test on skimage
	# work well on loading the stack tiff
	im_skim = io.imread(inputfileabslist[i])
	print(im_skim.shape)
	imsliced = im_skim[0, :, :]
	print(imsliced.shape)
	
	# print(imsliced)

	
	# ImageViewer from skimage
	# sliced 
	viewer = ImageViewer(imsliced) 
	viewer.show()
	

	
	break
'''