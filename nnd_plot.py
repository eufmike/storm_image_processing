# %%
# %load_ext autoreload
# %autoreload 2

import os, sys
import pandas as pd
import numpy as np
import re
import pprint

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style as styl
import matplotlib.image as mpimg
styl.use('default')

from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs

# %%
# Functions Section Begins ----------------------------------------------------- #

# Grouped by the channels and treatment ------------------------------------------ #
# %%
pixelsize = 0.01 # 0.01 µm/pixel

# %%
# input folder

'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
analysis_subdir = 'tstorm'
st_dir = 'spacial_test'
nnd_dir = 'nnd'
nnd_data_dist_dir = 'int_grid_data_dist'
nchannel = 2 
crop_region = 3
pad_pixel = 3
pixelsize = 0.01
nnd_plot_dir = 'int_grid_data_nndplot'
'''

path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
analysis_subdir = str(sys.argv[3])
st_dir = str(sys.argv[4])
nnd_dir = str(sys.argv[5])
nnd_data_dist_dir = str(sys.argv[6])
nchannel = int(sys.argv[7])
crop_region = int(sys.argv[8])
pad_pixel = int(sys.argv[9])
pixelsize = float(sys.argv[10])
nnd_plot_dir = str(sys.argv[11])

# input path
nnd_data_path = os.path.join(path, analysis_dir, st_dir, nnd_dir, nnd_data_dist_dir)
print(nnd_data_path)

# output folder
nnd_plot_path = os.path.join(path, analysis_dir, st_dir, nnd_dir, nnd_plot_dir)

dir_check = []
dir_check.append(nnd_plot_path)
DirCheck(dir_check)

# %%
# create grouped filename and file path 
group = {
    'wildtype': 'w',
    'knockout': 'k'
}
ippath = {
    'nnddata':{
        'dir': nnd_data_path,
        'ext': '.csv',
    }
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
mainfilelist = GetGrpFLs(filenamelist, nchannel, group, ippath, oppath)
pprint.pprint(mainfilelist)

# concate the data into one dataframe
data_list = []
for c in range(nchannel):
    for g in group.keys():
            for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
                filepath = mainfilelist[str(c+1)][g]['nnddata'][i]
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
data_total['Area_nm2'] = data_total['Area'] * (pixelsize * 10**3)**2
data_total['min_dist_nm'] = data_total['min_dist'] * pixelsize * 10**3

print(data_total.dtypes)
#display(data_total)

# %%
# plot merge nnd histogram with Area
for c in range(nchannel):
    # print('channel: {}'.format(c))
    
    dpi = 300
    fig, axes = plt.subplots(dpi = dpi)
    fig.set_figheight(5)
    fig.set_figwidth(8)
    colors = {
        'wildtype':'red', 
        'knockout':'blue'
    } 
    
    data_temp_c = data_total[data_total['channel'] == str(c+1)]
    # prepare binning (bin_list)
    val_max = max(data_temp_c['min_dist_nm'])
    print('min_dist_nm_max: {}'.format(val_max))
    binsize = 50
    bin_max = val_max//binsize
    print('min_dist_nm_bin_max: {}'.format(bin_max))
    bin_list = list(range(0, (int(bin_max) + 2) * binsize, binsize))
    print(bin_list)
    
    for g in group.keys():
        # print(data_total['channel'])
        data_temp_cg = data_temp_c[data_temp_c['group'] == g]
        # display(data_temp_cg)
        
        # plt.hist(data_temp_cg['min_dist_nm'], bins = 50, color = colors[g], alpha = 0.2)

        hist, bins = np.histogram(data_temp_cg['min_dist_nm'], bins = bin_list)
        
        plt.bar(bins[:-1], hist.astype(np.float32)/hist.sum() * 100, width=binsize, color = colors[g], alpha = 0.2)
    axes.legend(colors.keys())
    plt.title('NND Distribution for Channel ' + str(c+1), fontsize = 18)
    plt.xlabel('Centroid NND (µm)', fontsize = 18)
    plt.ylabel('Freqency counts (%)', fontsize = 18)
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    
    figop = os.path.join(nnd_plot_path, "summary_c" + str(c+1) + "_nnd.png")
    fig.savefig(figop)
    plt.close()

# %%
# mean nnd distance
for c in range(nchannel):
    
    dpi = 300
    fig = plt.figure(dpi = dpi)
    fig.set_figheight(5)
    fig.set_figwidth(5)

    ## size of nnd
    data_temp_c = data_total[data_total['channel'] == str(c+1)]
    data_temp_c_group = data_temp_c.groupby(by= ['group','filename'])['min_dist_nm'].mean()
    # display(data_temp_c_group)
    data_temp_c_mean = data_temp_c_group.reset_index()
    data_temp_c_mean_group = data_temp_c_mean.groupby(by = "group").mean()
    data_temp_c_sem_group = data_temp_c_mean.groupby(by = "group").sem()
    # display(data_temp_c_mean_group['min_dist_nm'])
    # display(data_temp_c_sem_group['min_dist_nm'])

    ## make plot    
    ax1 = plt.subplot(111)
    ax1.bar(['widetype', 'knockout'], 
            data_temp_c_mean_group['min_dist_nm'], 
            yerr= data_temp_c_sem_group['min_dist_nm'], 
            color=['red', 'blue'],
            alpha = 0.2,
            width = 0.8, 
            capsize = 10)
    plt.title('Nearest Neighbor Distance', fontsize = 18)
    plt.xticks(fontsize = 18)
    plt.ylabel('NN Distance (nm)', fontsize = 18)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    plt.gcf().subplots_adjust(left=0.15)
    
    figop = os.path.join(nnd_plot_path, "summary_c" + str(c+1) + "_nnd_mean.png")
    fig.savefig(figop)
    plt.close()

# %%
# plot nanocluster areas
for c in range(nchannel):
    
    dpi = 300
    fig = plt.figure(dpi = dpi)
    fig.set_figheight(5)
    fig.set_figwidth(10)
    
    ## size of nano cluster
    data_temp_c = data_total[data_total['channel'] == str(c+1)]
    data_temp_c_group = data_temp_c.groupby(by= ['group','filename'])['Area_nm2'].mean()
    # display(data_temp_c_group)
    data_temp_c_mean = data_temp_c_group.reset_index()
    data_temp_c_mean_group = data_temp_c_mean.groupby(by = "group").mean()
    data_temp_c_sem_group = data_temp_c_mean.groupby(by = "group").sem()
    # display(data_temp_c_mean_group['Area_nm2'])
    # display(data_temp_c_sem_group['Area_nm2'])

    ## make plot    
    ax1 = plt.subplot(121)
    ax1.bar(['widetype', 'knockout'], 
            data_temp_c_mean_group['Area_nm2'], 
            yerr= data_temp_c_sem_group['Area_nm2'], 
            color=['red', 'blue'],
            alpha = 0.2,
            width = 0.8, 
            capsize = 10)
    plt.title('Nanocluster Area', fontsize = 18)
    plt.xticks(fontsize = 18)
    plt.ylabel(r'$Nanocluster\ areas\ (nm^2)$', fontsize = 18)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    
    ## density of nano cluster
    # calculate the size of field of view
    frame_xsize = 480
    frame_ysize = 480
    fvarea_µm = (frame_xsize * pixelsize) * (frame_ysize * pixelsize)

    # count objects
    data_temp_c = data_total[data_total['channel'] == str(c+1)]
    data_temp_c_group = data_temp_c.groupby(by= ['group','filename'])['Area_nm2'].agg('count')
    data_temp_c_count = data_temp_c_group.reset_index()
    # display(data_temp_c_count)
    data_temp_c_count_mean_group = data_temp_c_count.groupby(by = "group").mean()
    data_temp_c_count_sem_group = data_temp_c_count.groupby(by = "group").sem()
    # display(data_temp_c_count_mean_group['Area_nm2'])
    # display(data_temp_c_count_sem_group['Area_nm2'])

    ## make plot    
    ax2 = plt.subplot(122)
    ax2.bar(['widetype', 'knockout'], 
            data_temp_c_count_mean_group['Area_nm2'], 
            yerr= data_temp_c_count_sem_group['Area_nm2'], 
            color=['red', 'blue'],
            alpha = 0.2,
            width = 0.8, 
            capsize = 10,)
    plt.title('Nanocluster Density', fontsize = 18)
    plt.xticks(fontsize = 18)
    plt.ylabel(r'$Nanocluster\ \slash \ µm^2$', fontsize = 18)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    figop = os.path.join(nnd_plot_path, "summary_c" + str(c+1) + "_nanocluster.png")
    fig.savefig(figop)
    plt.close()
