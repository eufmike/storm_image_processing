# %%
%load_ext autoreload
%autoreload 2

import os, sys
import re
import pprint
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
from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs

# %%
# Functions Section Begins ----------------------------------------------------- #

# Grouped by the channels and treatment ------------------------------------------ #
# %%
nchannels = 2
dir_check = []

# %%
# input folder
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
spacialtest_dir = 'spacial_test'
nnd_dir = 'nnd'
nnd_data_dir = 'int_grid_data_dist'
nnd_data_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_dir)
print(nnd_data_path)

# output folder
nnd_plot_dir = 'int_grid_data_nndplot'
nnd_plot_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_plot_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(nnd_plot_path, str(c+1)))

DirCheck(dir_check)

# %%
# create grouped filename and file path 
group = {
    'wildtype': 'w',
    'knockout': 'k'
}
ippath = {
    'dir': nnd_data_path,
    'ext': '.csv'
}

oppath = {
    'summary': {
        'dir': nnd_plot_path,
        'ext': '.png'
    }
}

# %%
# create filenamelist
filenamelist = ListFiles(os.path.join(nnd_data_path, str(1)), '.csv')['filelist']
mainfilelist = GetGrpFLs(filenamelist, nchannels, group, ippath, oppath)
pprint.pprint(mainfilelist)

# concate the data into one dataframe
data_list = []
for c in range(nchannels):
    for g in group.keys():
            for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
                filepath = mainfilelist[str(c+1)][g]['filepath_ip'][i]
                data = pd.read_csv(filepath, header=0, index_col = 0)
                data['filename'] = mainfilelist[str(c+1)][g]['filename_ip'][i]
                data['group'] = g
                data['channel'] = str(c+1)
                data_list.append(data)

data_total = pd.concat(data_list, axis = 0)

# %%
data_total = pd.DataFrame(data_total)
# display(data_total)
# print(data_total.shape)
data_total['Area'] = data_total['Area'].astype('int') 
print(data_total.dtypes)

# %%
# plot merge histogram with Area
for c in range(nchannels):
    print('channel: {}'.format(c))
    
    fig, axes = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    colors = {
        'wildtype':'red', 
        'knockout':'blue'
    }

    for g in group.keys():
        print(data_total['channel'])
        data_temp = data_total[data_total['channel'] == str(c+1)]
        data_temp = data_temp[data_temp['group'] == g]
        display(data_temp)
        
        plt.hist(data_temp['min_dist'], bins = 100, color = colors[g], alpha = 0.2, density = True)
        #plt.yscale('log')

    figop = os.path.join(nnd_plot_path, "summary_c" + str(c+1) + "_nnd.png")
    fig.savefig(figop)
    plt.close()
    