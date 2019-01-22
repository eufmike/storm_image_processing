# %%
import os
import sys
from tqdm import tqdm
import numpy as np
import pandas as pd
from skimage import io
from skimage.viewer import ImageViewer
from skimage.external import tifffile
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def filelistcreater(inputfilepath, ext): 
	inputfilelist = []
	inputfileabslist = []
	for directory, dir_names, file_names in os.walk(inputfilepath):
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(ext)):
				filepath_tmp =  os.path.join(directory, file_name)
				inputfilelist.append(file_name)
				inputfileabslist.append(filepath_tmp)
	return (inputfilelist, inputfileabslist)

# create input folder
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_012019'
image_dir = 'crop_img'
inputfilepath = os.path.join(path, analysis_dir,image_dir)

# %%
'''
inputfilelist = []
inputfileabslist = []
for directory, dir_names, file_names in os.walk(inputfilepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.tif')):
			filepath_tmp =  os.path.join(directory, file_name)
			inputfilelist.append(file_name)
			inputfileabslist.append(filepath_tmp)
'''
inputfilelist, inputfileabslist = filelistcreater(inputfilepath = inputfilepath, \
													ext = '.tif')
print(inputfilelist)
print(inputfileabslist)
print(len(inputfilelist))

error = []
for i in tqdm(range(len(inputfilelist))):
	im_skim = io.imread(inputfileabslist[i]) # faster
	# im_skim = tifffile.imread(inputfileabslist[i])
	zdim, xdim, ydim = im_skim.shape
	if zdim != 10000 | xdim != 30 | ydim != 30:
		error.append(str(i+1))
	'''
	imsliced = im_skim[0, :, :]
	print(imsliced.shape)
	'''
# %%
print('finish')
print(error)

# %%
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_012019'
image_dir = 'histogram_plot'
inputfilepath = os.path.join(path, analysis_dir,image_dir)

inputfilelist, inputfileabslist = filelistcreater(inputfilepath = inputfilepath, \
													ext = '.tif')
print(inputfilelist)
print(inputfileabslist)
print(len(inputfilelist))

# %%
error = []
for i in tqdm(range(len(inputfilelist))):
	im_skim = io.imread(inputfileabslist[i]) # faster
	# im_skim = tifffile.imread(inputfileabslist[i])
	xdim, ydim = im_skim.shape
	if xdim != 150 | ydim != 150:
		error.append(str(i+1))
	
	
	'''
	imsliced = im_skim[0, :, :]
	print(imsliced.shape)
	'''

# %%
print('finish')
print(error)