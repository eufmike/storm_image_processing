# %%
import os, sys
import re
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from numpy import linspace, meshgrid
from scipy.interpolate import griddata
import matplotlib.image as mpimg
import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')
from PIL import Image

# Functions Section Begins ----------------------------------------------------- #
def dircheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if isinstance(targetpaths, str): 
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif isinstance(targetpaths, list): 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def listfiles(path, extension = None):
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(path):
		# print(file_names)
		
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(extension)):
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name)
				fileabslist.append(filepath_tmp)
	
	return {'filelist': filelist,
			'fileabslist': fileabslist}               
# Functions Section Ends ----------------------------------------------------- #

# %%
nchannels = 2
dir_check = []

# %%
# input folder
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
spacialtestdir = 'spacial_test'
intcsv_dir = 'spacialdata_local_pad_grid'
intcsv_path = os.path.join(path, analysis_dir, spacialtestdir, intcsv_dir)
print(intcsv_path)

# output folder
nnd_dir = 'nnd'
intcsv_histo_dir = 'int_grid_histo'
intcsv_histo_summary_dir = 'int_grid_histo_summary'
intcsv_bw = 'int_grid_bw'
intcsv_histo_path = os.path.join(path, analysis_dir, spacialtestdir, nnd_dir, intcsv_histo_dir)
intcsv_histo_summary_path = os.path.join(path, analysis_dir, spacialtestdir, nnd_dir, intcsv_histo_summary_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(intcsv_histo_path, str(c+1)))
    dir_check.append(os.path.join(intcsv_bw, str(c+1)))

dir_check.append(intcsv_histo_summary_path)
dircheck(dir_check)

# %%
# Grouped by the channels and treatment ------------------------------------------ #
filelist = {}

filenamelist = listfiles(os.path.join(intcsv_path, '1'), '.tif')['filelist']
filedir = ['ip_filename', 'ip_path', 'op_hist', 'op_bw']
treatment = ['wildtype', 'knockout']
channel = list(range(2))
print(channel)

# group the data by the treatment 
for c in channel:
    filelist[str(c+1)] = {}
    for group in treatment:
        filelist[str(c+1)][group] = {}    
        
        # create list
        filelist_temp = []
        for l in filenamelist: 
            if group == 'wildtype':
                x = re.search('(.*)_w{1}[0-9]{1}_(.*)', l)
            else: 
                x = re.search('(.*)_k{1}[0-9]{1}_(.*)', l) 
            try: 
                found = x.group(0)
                filelist_temp.append(found)
            except AttributeError:
                found = ''

        ip_filepath = []
        op_hist_filepath = []
        op_bw_filepath = []

        for f in filelist_temp: 
            filepath_tmp =  os.path.join(intcsv_path, str(c+1), f)
            ip_filepath.append(filepath_tmp)

            filename_tmp_png = f.replace('.tif', '.png')
            op_hist_filepath_temp = os.path.join(intcsv_histo_path, str(c+1), filename_tmp_png)
            op_hist_filepath.append(op_hist_filepath_temp)
            op_bw_filepath_temp = os.path.join(intcsv_bw, str(c+2), filepath_tmp)
            op_bw_filepath.append(op_bw_filepath_temp)
            
        filelist[str(c+1)][group][filedir[0]] = filelist_temp
        filelist[str(c+1)][group][filedir[1]] = ip_filepath
        filelist[str(c+1)][group][filedir[2]] = op_hist_filepath
        filelist[str(c+1)][group][filedir[3]] = op_bw_filepath

print(filelist)


# %%
# create binary by thresholding
for c in channel:
    print('channel: {}'.format(c))
    for group in treatment:
        for i in range(len(filelist[str(c+1)][group][filedir[0]])):
            filepath = filelist[str(c+1)][group][filedir[1]][i]
            print(filepath)
            im = np.array(Image.open(filepath))
            print(type(im))
            cv2.imshow('image', im)
            break
        break
    break
        