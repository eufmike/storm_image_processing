# %% make plot
import numpy as np
import re
import os, sys
import pandas as pd
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

# Functions Section Ends ----------------------------------------------------- #
# %%
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
cbc_dir = 'CBC'
cbc_subdir = 'CBC_results'
nchannel = 2
CBC_histo_dir = 'CBC_histogram'
CBC_histo_sum_dir = 'CBC_histogram_summary'
'''

path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
cbc_dir = str(sys.argv[3])
cbc_subdir = str(sys.argv[4])
nchannel = int(sys.argv[5])
CBC_histo_dir = str(sys.argv[6])
CBC_histo_sum_dir = str(sys.argv[7])

# histogram for photon count
# create input path
dir_check = []

cbccsv_path = os.path.join(path, analysis_dir, cbc_dir, cbc_subdir)
print(cbccsv_path)

# create output path

CBC_histo_path = os.path.join(path, analysis_dir, cbc_dir, CBC_histo_dir)
CBC_histo_sum_path = os.path.join(path, analysis_dir, cbc_dir, CBC_histo_sum_dir)
print(CBC_histo_path)

for c in range(nchannel):
    dir_check.append(os.path.join(CBC_histo_path, str(c+1)))
dir_check.append(os.path.join(CBC_histo_sum_path))

# check dir
DirCheck(dir_check)
# %%
# create grouped filename and file path 
colors = {
    'wildtype': 'red',
    'knockout': 'blue'
}

group = {
    'wildtype': 'w',
    'knockout': 'k'
}
ippath = {
    'cbcdata':{
        'dir': cbccsv_path,
        'ext': '.csv',
    }
}

oppath = {
    'histogram': {
        'dir': CBC_histo_path,
        'ext': '.png'
    }
}

# %%
# create filenamelist
filenamelist = ListFiles(os.path.join(cbccsv_path, str(1)), '.csv')['filelist']
mainfilelist = GetGrpFLs(filenamelist, nchannel, group, ippath, oppath)
pprint.pprint(mainfilelist)

# %%
# Grouped by the channels and treatment ------------------------------------------ #

# ----------------------------------------------------- #

# %%
binsize = 20
bin_list = np.linspace(-1.0, 1.0, binsize+1)
print(bin_list)
# %%
data_list = []
for c in range(nchannel):
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filepath = mainfilelist[str(c+1)][g]['cbcdata'][i]
            # print(filepath)
            data = pd.read_csv(filepath, header=0, index_col = 0)
            data['filename'] = mainfilelist[str(c+1)][g]['filename_ip'][i]
            data['group'] = g
            data['channel'] = str(c+1)
            data_list.append(data)

            # print(data)
            fig = plt.figure()
            plt.hist(data['cbc'], binsize)
            # plt.yscale('log')
            plt.grid(True)
            plt.xlim(-1, 1)
            opfilename = mainfilelist[str(c+1)][g]['histogram'][i]
            print(opfilename)
            fig.savefig(opfilename)
            plt.close()

data_total = pd.concat(data_list, axis = 0)

# %%
print(data_total.shape)
# display(data_total.head())
# %%
# CBC visualization
# Plot individual CBC data
for c in range(nchannel):
    print(c)
    data_temp = pd.DataFrame(data_total[data_total['channel'] == str(c+1)])
    fig, axes = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filename_tmp = mainfilelist[str(c+1)][g]['filename_ip'][i]
            print(filename_tmp)
            data_plot = data_temp[data_temp['filename'] == filename_tmp]
            data_plot_temp = pd.cut(data_plot['cbc'], bins = bin_list)
            data_plot_bin = data_plot.copy()
            data_plot_bin['bins'] = data_plot_temp
            data_plot_bin = data_plot_bin.groupby(by = 'bins').size()
            data_plot_bin = data_plot_bin.reset_index()
            data_plot_bin = data_plot_bin.rename(index = int, columns={0: 'counts'})
            
            x = bin_list[0: -1]
            y = data_plot_bin.reset_index()['counts']/data_plot.shape[0]
            
            plt.step(x, y, color = colors[g], where = 'post', alpha = 0.2)
    
    fig.savefig(os.path.join(CBC_histo_sum_path, 'CBC_total' + '_c' +  str(c+1) + '.png'))
    plt.close()
    
# %%
# mergeed plot, grouped by channel and treatment, average and errorbar
for c in range(nchannel):
    print('channel: {}'.format(c))
    # load data
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    
    # prepare binned data
    data_total_tmp = data_total
    data_total_tmp['bins'] = pd.cut(data_total['cbc'], bins = bin_list)
    # group by bins
    data_total_count_tmp = data_total_tmp.groupby(by = ['channel', 'group', 'filename', 'bins']).size()
    data_total_count_tmp = data_total_count_tmp.reset_index()
    data_total_count_tmp = data_total_count_tmp.rename(index = int, columns={0: 'counts'})
    # display(data_total_count_tmp.head())

    # reset index for total events
    data_total_size_tmp = data_total_count_tmp.groupby(by = ['channel', 'group', 'filename']).sum()
    data_total_size_tmp = data_total_size_tmp.reset_index()
    data_total_size_tmp = data_total_size_tmp.rename(index = int, columns={'counts': 'total_events'})
    # display(data_total_size_tmp.head())

    df_temp = data_total_count_tmp.merge(data_total_size_tmp)
    df_temp['counts_normed'] = df_temp['counts']/df_temp['total_events']
    # display(df_temp)

    # 2nd group by 
    data_total_tmp_mean = df_temp.groupby(by = ['channel', 'group', 'bins']).mean()['counts_normed']
    data_total_tmp_sem = df_temp.groupby(by = ['channel', 'group', 'bins']).sem()['counts_normed']

    # plot mean dataset
    fig, axes = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    for g in group.keys():
        print(g)
        data_mean_temp_mean = data_total_tmp_mean.loc[str(c+1), g]
        x = bin_list[0: -1] + 0.05
        print(x)
        y = data_mean_temp_mean.reset_index()['counts_normed']
        data_mean_temp_sem = data_total_tmp_sem.loc[str(c+1), g]
        yerr = data_mean_temp_sem.reset_index()['counts_normed']
        # print(yerr)
        
        # make plots
        width = 0.040
        if g == 'wildtype':
            plt.bar(x - width/2, y, width = width, yerr=yerr, capsize=2, color = colors[g], alpha = 0.2)
        else: 
            plt.bar(x + width/2, y, width = width, yerr=yerr, capsize=2, color = colors[g], alpha = 0.2)

    plt.legend(['wildtype', 'knockout'])
    
    fig.savefig(os.path.join(CBC_histo_sum_path, 'CBC_mean' + '_c' +  str(c+1) + '.png'))
    plt.close()

# ----------------------------------------------------- #
