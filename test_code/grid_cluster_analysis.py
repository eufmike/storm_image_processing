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
        op_th_filepath = []
        for f in filelist_temp: 
            filepath_tmp =  os.path.join(intcsv_path, str(c+1), f)
            ip_filepath.append(filepath_tmp)

            filename_tmp_png = f.replace('.tif', '.png')
            op_hist_filepath_temp = os.path.join(intcsv_histo_path, str(c+1), filename_tmp_png)
            op_hist_filepath.append(op_hist_filepath_temp)

            # f_csv_tmp = os.path.join(csv_threshold_path, str(c+1), f)
            # op_th_filepath.append(f_csv_tmp)

        filelist[str(c+1)][group][filedir[0]] = filelist_temp
        filelist[str(c+1)][group][filedir[1]] = ip_filepath
        filelist[str(c+1)][group][filedir[2]] = op_hist_filepath

print(filelist)
# ----------------------------------------------------- #

# %%
data_list = []
for c in channel:
    for group in treatment:
        for i in range(len(filelist[str(c+1)][group][filedir[0]])):
            filepath = filelist[str(c+1)][group][filedir[1]][i]
            im = np.array(Image.open(filepath))
            fig = plt.figure()
            plt.yscale('log')
            plt.hist(im.ravel(), bins=256, range=(0, 1000))
            opfilename = filelist[str(c+1)][group][filedir[2]][i]
            fig.savefig(opfilename)
            plt.close()

            data_tmp = pd.DataFrame({'density':im.ravel()})
            data_tmp['filename'] = filelist[str(c+1)][group][filedir[0]][i]
            data_tmp['group'] = group
            data_tmp['channel'] = str(c+1)
            data_list.append(data_tmp)

data_total = pd.concat(data_list, axis = 0)

# %%
for c in channel:
    print(c)
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    max_value = max(data_temp['density'])
    print(max_value)
    binsize = 25
    bin_max_value = max_value//binsize
    print(bin_max_value)
    bin_list = list(range(0, (int(bin_max_value) + 2) * binsize, binsize))
    print(bin_list)
    fig, axes = plt.subplots()
    colors = ['red', 'blue']
    
    for m in range(len(treatment)):
        for i in range(len(filelist[str(c+1)][treatment[m]][filedir[0]])):
        # for i in range(10):
            filename_tmp = filelist[str(c+1)][treatment[m]][filedir[0]][i]
            # print(filename_tmp)
            data_plot = data_temp[data_temp['filename'] == filename_tmp]
            # print(data_plot)
            plt.hist(data_plot['density'], bins= bin_list, histtype = 'step', color = colors[m], alpha = 0.2)
            plt.yscale('log')
            #plt.xscale('log')
        
    fig.savefig(os.path.join(intcsv_histo_summary_path, 'density' + '_c' +  str(c+1) + '.png'))
    axes.set_xlim(0, max_value)
    plt.close()

# %%
# mergeed plot, grouped by channel and treatment, average and errorbar
for c in channel:
    
    print('channel: {}'.format(c))
    # load data
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    
    # prepare binning (bin_list)
    max_value = max(data_temp['density'])
    print('max_value: {}'.format(max_value))
    binsize = 25
    bin_max_value = max_value//binsize
    print('bin_max_value: {}'.format(bin_max_value))
    bin_list = list(range(0, (int(bin_max_value) + 2) * binsize, binsize))
    print(bin_list)
    
    # prepare binned data
    data_total_tmp = data_total
    data_total_tmp['bins'] = pd.cut(data_total['density'], bins = bin_list)
    # 1st group by bins
    data_total_tmp = data_total_tmp.groupby(by = ['channel', 'group', 'filename', 'bins']).size()
    # reset index
    data_total_tmp = data_total_tmp.reset_index()
    data_total_tmp = data_total_tmp.rename(index = int, columns={0: 'counts'})
    # 2nd group by 
    data_total_tmp_mean = data_total_tmp.groupby(by = ['channel', 'group', 'bins']).mean()['counts']
    data_total_tmp_sem = data_total_tmp.groupby(by = ['channel', 'group', 'bins']).sem()['counts']

    
    print('binned data, mean')
    display(data_total_tmp_mean)
    print('binned data, sem')
    display(data_total_tmp_sem)
    

    # plot mean dataset
    fig, axes = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    colors = ['red', 'blue']
    for m in range(len(treatment)):
        # print(m)
        data_mean_temp_mean = data_total_tmp_mean.loc[str(c+1), treatment[m]]
        x = list(range(0, data_mean_temp_mean.shape[0]*binsize, binsize))
        # print(x)
        # x = data_mean_temp_mean.reset_index()['bins']
        # print(x)
        y = data_mean_temp_mean.reset_index()['counts']
        # print(y)
        
        data_mean_temp_sem = data_total_tmp_sem.loc[str(c+1), treatment[m]]
        yerr = data_mean_temp_sem.reset_index()['counts']
        # print(yerr)
        plt.yscale('log')
        #plt.xscale('log')
        
        # make plots
        plt.errorbar(x, y, yerr = yerr, color = colors[m], alpha = 0.2)
    
    plt.yscale('log')
    axes.set_xlim(0, max_value)
    oppath_temp = os.path.join(intcsv_histo_summary_path, 'density_mean' + '_c' +  str(c+1) + '.png')
    print(oppath_temp)
    fig.savefig(oppath_temp)
    plt.close()

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
        