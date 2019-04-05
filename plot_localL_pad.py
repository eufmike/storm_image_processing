# %%
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def getpendinglist(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv'):
	"""
	getpendinglist compares the files from src_dir and the accomplisjed file in op_dir, 
	then creates a pending list of unprocessed image. 
	"""
	
	srclist = listfiles(src_dir, src_ext)
	srclist = srclist['fileabslist']
	oplist = listfiles(op_dir, op_ext)
	oplist = oplist['fileabslist']

	oplist_basename = []
	for i in oplist:
		name = os.path.basename(i)
		print('name: {}'.format(name))
		basename = os.path.splitext(name)[0]
		print('basename: {}'.format(basename))
		oplist_basename.append(basename)
	
	pendingfllist = []
	pendingpathlist_input = []
	pendingpathlist_output = []
	
	for i in range(len(srclist)):
		srcflname = os.path.basename(srclist[i])
		srcflbasename = os.path.splitext(srcflname)[0]
		
		if not srcflbasename in oplist_basename:
			pendingfllist.append(srcflbasename)
			pendingpathlist_input.append(srclist[i])			
			pendingpathlist_output.append(os.path.join(op_dir, srcflbasename + op_ext))
			
	return (pendingfllist, pendingpathlist_input, pendingpathlist_output)

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
nchannels = 2

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
st_dir = 'spacial_test'
csv_scatter_dir = 'spacialdata_local_pad'
csv_scatter_path = os.path.join(path, analysis_dir, st_dir, csv_scatter_dir)
csv_grid_dir = 'spacialdata_local_pad_int'
csv_grid_path = os.path.join(path, analysis_dir, st_dir, csv_grid_dir)

dir_check = []

img_scatter_dir = 'spacialdata_local_pad_scatter'
img_scatter_path = os.path.join(path, analysis_dir, st_dir, img_scatter_dir)
img_grid_dir = 'spacialdata_local_pad_grid'
img_grid_path = os.path.join(path, analysis_dir, st_dir, img_grid_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(img_scatter_path, str(c+1)))
    dir_check.append(os.path.join(img_grid_path, str(c+1)))

# check dir
dircheck(dir_check)

# %%
# create pending file list
pd_scatter_ip = []
pd_scatter_abs_ip = []
pd_scatter_op = []

src_ext = '.csv'
op_ext = '.png'

for c in range(nchannels):
    path_ip_tmp = os.path.join(csv_scatter_path, str(c+1))
    path_op_tmp = os.path.join(img_scatter_path, str(c+1))
    pendingfllist_temp, pendingpathlist_ip_temp, pendingpathlist_op_temp = getpendinglist(path_ip_tmp, path_op_tmp, src_ext = src_ext, op_ext = op_ext)
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

for c in range(nchannels):
    path_ip_tmp = os.path.join(csv_grid_path, str(c+1))
    path_op_tmp = os.path.join(img_grid_path, str(c+1))
    pendingfllist_temp, pendingpathlist_ip_temp, pendingpathlist_op_temp = getpendinglist(path_ip_tmp, path_op_tmp, src_ext = src_ext, op_ext = op_ext)
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
    data_sliced[data_sliced > 500] = 500
    print(data_sliced)
    print(data_sliced.shape)
    '''
    mydpi = 100
    fig = plt.figure(dpi=mydpi, figsize=(grid_size/mydpi, grid_size/mydpi))
    # img = plt.imshow(data_2, origin="low", cmap = 'jet', clim= (0, 500))
    plt.contourf(data_2, list(range(0, 600, 10)), cmap = 'jet')
    
    ax = plt.gca()
    plt.axis('off')
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0)
    plt.savefig(opfilename_tmp)
    plt.show
    plt.close()
    '''
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
    