# %%
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid
from scipy.interpolate import griddata

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style as styl
import matplotlib.image as mpimg
styl.use('default')

from PIL import Image

from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs

# Functions Section Begins ----------------------------------------------------- #
def grid(x, y, z, resX=100, resY=100):
    "Convert 3 column data to matplotlib grid"
    grid_x, grid_y = np.mgrid[0:20480:512j, 0:20480:512j]
    
    x_array = np.array([x])
    y_array = np.array([y])
    points = np.concatenate((x_array.T, y_array.T), axis = 1)

    grid_Z = griddata(points, z, (grid_x, grid_y), method='linear', fill_value=0)
    return grid_Z
# Functions Section Ends ----------------------------------------------------- #

# %%
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
analysis_subdir = 'tstorm'
st_dir = 'spacial_test'
csv_scatter_dir = 'spacialdata_local_pad'
csv_grid_dir = 'spacialdata_local_pad_int'
nchannel = 2 
crop_region = 3
pad_pixel = 3
img_scatter_dir = 'plot_local_pad_scatter'
img_grid_dir = 'plot_local_pad_grid'
'''

path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
analysis_subdir = str(sys.argv[3])
st_dir = str(sys.argv[4])
csv_scatter_dir = str(sys.argv[5])
csv_grid_dir = str(sys.argv[6])
nchannel = int(sys.argv[7])
crop_region = int(sys.argv[8])
pad_pixel = int(sys.argv[9])
img_scatter_dir = str(sys.argv[10])
# print(img_scatter_dir)
img_grid_dir = str(sys.argv[11])
# print(img_grid_dir)

csv_scatter_path = os.path.join(path, analysis_dir, st_dir, csv_scatter_dir)
csv_grid_path = os.path.join(path, analysis_dir, st_dir, csv_grid_dir)

dir_check = []

img_scatter_path = os.path.join(path, analysis_dir, st_dir, img_scatter_dir)
img_grid_path = os.path.join(path, analysis_dir, st_dir, img_grid_dir)

for c in range(nchannel):
    dir_check.append(os.path.join(img_scatter_path, str(c+1)))
    dir_check.append(os.path.join(img_grid_path, str(c+1)))

# check dir
DirCheck(dir_check)

# %%
# create pending file list
pd_scatter_ip = []
pd_scatter_abs_ip = []
pd_scatter_op = []

src_ext = '.csv'
op_ext = '.png'

for c in range(nchannel):
    path_ip_tmp = os.path.join(csv_scatter_path, str(c+1))
    print(path_ip_tmp)
    path_op_tmp = os.path.join(img_scatter_path, str(c+1))
    print(path_op_tmp)
    pendingfllist_temp, pendingpathlist_ip_temp, pendingpathlist_op_temp = GetPendingList(path_ip_tmp, path_op_tmp, src_ext = src_ext, op_ext = op_ext)
    pd_scatter_ip = pd_scatter_ip + pendingfllist_temp
    pd_scatter_abs_ip = pd_scatter_abs_ip + pendingpathlist_ip_temp
    pd_scatter_op = pd_scatter_op + pendingpathlist_op_temp

print(pd_scatter_ip)
print(pd_scatter_abs_ip)
print(pd_scatter_op)

# %%
pd_grid_ip = []
pd_grid_abs_ip = []
pd_grid_op = []

src_ext = '.csv'
op_ext = '.tif'

for c in range(nchannel):
    path_ip_tmp = os.path.join(csv_grid_path, str(c+1))
    path_op_tmp = os.path.join(img_grid_path, str(c+1))
    pendingfllist_temp, pendingpathlist_ip_temp, pendingpathlist_op_temp = GetPendingList(path_ip_tmp, path_op_tmp, src_ext = src_ext, op_ext = op_ext)
    pd_grid_ip = pd_grid_ip + pendingfllist_temp
    pd_grid_abs_ip = pd_grid_abs_ip + pendingpathlist_ip_temp
    pd_grid_op = pd_grid_op + pendingpathlist_op_temp

print(pd_grid_ip)
print(pd_grid_abs_ip)
print(pd_grid_op)

# %%
for i in range(len(pd_scatter_ip)):
    # scatter plot
    filepath_tmp = pd_scatter_abs_ip[i]
    print(filepath_tmp)
    data = pd.read_csv(filepath_tmp, header=0)
    # display(data)
    
    fig = plt.figure(figsize = (10,10))
    
    plt.subplot(111)
    plt.scatter(data['x'], data['y'], c = data['z'], s = 1)
    
    opfilename_tmp = pd_scatter_op[i]
    print(opfilename_tmp)
    fig.savefig(opfilename_tmp)
    plt.close()

# %%
# plot grid image; save in grey scale
grid_size = 480
for i in range(len(pd_grid_abs_ip)):    
    # grid plot
    filepath_tmp = pd_grid_abs_ip[i]
    print(filepath_tmp)
    opfilename_tmp = pd_grid_op[i]
    print(opfilename_tmp)

    data = pd.read_csv(filepath_tmp, header=0)
    data = np.array(data)
    # print(data)

    data_sliced = data
    data_sliced[data_sliced < 0] = 0
    # data_sliced[data_sliced > 500] = 500
    print(data_sliced)
    print(data_sliced.shape)

    pixelsize = 160
    framesize = 30
    padsize = 3
    grid_stepfactor = 10

    x_start_idx = int(pixelsize * padsize/grid_stepfactor)
    x_end_idx = x_start_idx + int(pixelsize * framesize / grid_stepfactor)
    y_start_idx = int(pixelsize * padsize/grid_stepfactor)
    y_end_idx = y_start_idx + int(pixelsize * framesize / grid_stepfactor)
    print(x_start_idx, x_end_idx, y_start_idx, y_end_idx)

    data_sliced_padremove = data_sliced[x_start_idx:x_end_idx, y_start_idx:y_end_idx]
    print(data_sliced_padremove.shape)
    im = Image.fromarray(data_sliced_padremove)
    im.save(opfilename_tmp, "TIFF")
