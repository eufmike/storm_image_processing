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
def FltByMaxMin(data, key, filterpar):

    filterpar_dic = filterpar[key]
    
    if ('min' in filterpar_dic.keys()) & ('max' in filterpar_dic.keys()):
        data_flt = data.loc[(data[key] > filterpar_dic['min']) & (data[key] < filterpar_dic['max']), :]
    elif ('min' in filterpar_dic.keys()) & (not 'max' in filterpar_dic.keys()):
        data_flt = data.loc[data[key] > filterpar_dic['min'], :]
    elif ('min' in filterpar_dic.keys()) & (not 'max' in filterpar_dic.keys()):
        data_flt = data.loc[data[key] < filterpar_dic['max'], :]
    
    return data_flt

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
nnd_data_dir = 'int_grid_data'
nnd_data_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_dir)
print(nnd_data_path)

# output folder
nnd_data_summary_dir = 'int_grid_data_summary'
nnd_data_summary_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_summary_dir)
print(nnd_data_summary_path)
nnd_data_flt_dir = 'int_grid_data_filtered'
nnd_data_flt_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_flt_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(nnd_data_flt_path, str(c+1)))

dir_check.append(nnd_data_summary_path)

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
        'dir': nnd_data_summary_dir,
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
        
        plt.hist(data_temp['Area'], bins = 100, color = colors[g], alpha = 0.2)
        plt.yscale('log')

    figop = os.path.join(nnd_data_summary_path, "summary_c" + str(c+1) + "_area.png")
    fig.savefig(figop)
    plt.close()
    

# %%
# create pending filename and file path 
src_ext = '.csv'
op_ext = '.csv'

flnamels = []
flpth_ip = []
flpth_op = []
for c in range(nchannels):
	src_dir = os.path.join(nnd_data_path, str(c+1))
	op_dir = os.path.join(nnd_data_flt_path, str(c+1))
	flnamels_tmp, flpth_ip_tmp, flpth_op_tmp = GetPendingList(src_dir, op_dir, src_ext = '.csv', op_ext = '.csv')
	flnamels = flnamels + flnamels_tmp
	flpth_ip = flpth_ip + flpth_ip_tmp
	flpth_op = flpth_op + flpth_op_tmp

# print(flnamels)
print(flpth_op)

# filter parameter
filterpar = {
    'Area': {'min' : 50, 'max': 1000}, 
    'Circ.': {'min': 0.5, },        
}

# data inference
# %%
for i in range(len(flpth_ip)):
    flpth_ip_tmp = flpth_ip[i]
    flpth_op_tmp = flpth_op[i]
    
    # load csv
    data = pd.read_csv(flpth_ip_tmp, header = 0)

    # filter the data
    data_flt = FltByMaxMin(data, 'Area', filterpar)
    data_flt = FltByMaxMin(data_flt, 'Circ.', filterpar)
    
    data_flt.to_csv(flpth_op_tmp, index=False)
    