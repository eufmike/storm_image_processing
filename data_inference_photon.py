#%%
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

# Functions Section Begins ----------------------------------------------------- #
            
# Functions Section Ends ----------------------------------------------------- #

# %%

'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
tstorm_dir = 'tstorm'
st_dir = 'spacial_test'
csvdata_dir = 'csvdata_sliced_T_ROI'
nchannel = 2
stormdatainf_dir = 'stormdatainf_dir'
photon_histo_summary_dir = 'photons_hist_summary'
photon_histo_dir = 'photons_hist'
'''

path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
tstorm_dir = str(sys.argv[3])
st_dir = str(sys.argv[4])
csvdata_dir = str(sys.argv[5])
nchannel = int(sys.argv[6])
stormdatainf_dir  = str(sys.argv[7])
photon_histo_summary_dir = str(sys.argv[8])
photon_histo_dir = str(sys.argv[9])

# create input path
stormcsv_path = os.path.join(path, analysis_dir, tstorm_dir, csvdata_dir)
print(stormcsv_path)

# create output path
photon_histo_summary_path = os.path.join(path, analysis_dir, tstorm_dir, stormdatainf_dir, photon_histo_summary_dir)
photon_histo_path = os.path.join(path, analysis_dir, tstorm_dir, stormdatainf_dir, photon_histo_dir)

dir_check = []
dir_check.append(photon_histo_summary_path)
for c in range(nchannel):
    dir_check.append(os.path.join(photon_histo_path, str(c+1)))

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
    'stormdata':{
        'dir': stormcsv_path,
        'ext': '.csv',
    }
}

oppath = {
    'histogram': {
        'dir': photon_histo_path,
        'ext': '.png'
    }
}

# %%
# create filenamelist
filenamelist = ListFiles(os.path.join(stormcsv_path, str(1)), '.csv')['filelist']
mainfilelist = GetGrpFLs(filenamelist, nchannel, group, ippath, oppath)
pprint.pprint(mainfilelist)


# ----------------------------------------------------- #
# %%
data_list = []
for c in range(nchannel):
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filepath = mainfilelist[str(c+1)][g]['stormdata'][i]
            # print(filepath)
            data = pd.read_csv(filepath, header=0, index_col = 0)
            data['filename'] = mainfilelist[str(c+1)][g]['filename_ip'][i]
            data['group'] = g
            data['channel'] = str(c+1)
            data_list.append(data)

            # print(data)
            fig = plt.figure()
            plt.hist(data['intensity [photon]'], 100)
            plt.yscale('log')
            plt.grid(True)
            opfilename = mainfilelist[str(c+1)][g]['histogram'][i]
            print(opfilename)
            fig.savefig(opfilename)
            plt.close()

data_total = pd.concat(data_list, axis = 0)

# %%
data_total = pd.DataFrame(data_total)
# display(data_total)
# ----------------------------------------------------- #
# %%
# mergeed plot, grouped by channel and treatment
for c in range(nchannel):
    print(c)
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    photon_max = max(data_temp['intensity [photon]'])
    print(photon_max)
    binsize = 1000
    photon_bin_max = photon_max//binsize
    print(photon_bin_max)
    bin_list = list(range(0, (int(photon_bin_max) + 2) * binsize, binsize))
    print(bin_list)
    fig, axes = plt.subplots()
    
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filename_tmp = mainfilelist[str(c+1)][g]['filename_ip'][i]
            # print(filename_tmp)
            data_plot = data_temp[data_temp['filename'] == filename_tmp]
            # print(data_plot)
            plt.hist(data_plot['intensity [photon]'], bins= bin_list, histtype = 'step', color = colors[g], alpha = 0.2)
            plt.yscale('log')
            #plt.xscale('log')

    plt.legend(['wildtype', 'knockout'])

    fig.savefig(os.path.join(photon_histo_summary_path, 'photon_all' + '_c' +  str(c+1) + '.png'))
    axes.set_xlim(0, 2500)
    plt.close()

# %%
# mergeed plot, grouped by channel and treatment, average and errorbar
for c in range(nchannel):
    
    print('channel: {}'.format(c))
    # load data
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    
    # prepare binning (bin_list)
    photon_max = max(data_temp['intensity [photon]'])
    print('photon_max: {}'.format(photon_max))
    binsize = 1000
    photon_bin_max = photon_max//binsize
    print('photon_bin_max: {}'.format(photon_bin_max))
    bin_list = list(range(0, (int(photon_bin_max) + 2) * binsize, binsize))
    print(bin_list)
    
    # prepare binned data
    data_total_tmp = data_total
    data_total_tmp['bins'] = pd.cut(data_total['intensity [photon]'], bins = bin_list)
    # 1st group by bins
    data_total_tmp = data_total_tmp.groupby(by = ['channel', 'group', 'filename', 'bins']).size()
    # reset index
    data_total_tmp = data_total_tmp.reset_index()
    data_total_tmp = data_total_tmp.rename(index = int, columns={0: 'counts'})
    # 2nd group by 
    data_total_tmp_mean = data_total_tmp.groupby(by = ['channel', 'group', 'bins']).mean()['counts']
    data_total_tmp_sem = data_total_tmp.groupby(by = ['channel', 'group', 'bins']).sem()['counts']

    
    print('binned data, mean')
    # display(data_total_tmp_mean)
    print('binned data, sem')
    # display(data_total_tmp_sem)
    

    # plot mean dataset
    fig, axes = plt.subplots()
    fig.set_figheight(15)
    fig.set_figwidth(15)
    
    for g in group.keys():
        # print(m)
        data_mean_temp_mean = data_total_tmp_mean.loc[str(c+1), g]
        x = list(range(0, data_mean_temp_mean.shape[0]*binsize, binsize))
        # print(x)
        # x = data_mean_temp_mean.reset_index()['bins']
        # print(x)
        y = data_mean_temp_mean.reset_index()['counts']
        # print(y)
        
        data_mean_temp_sem = data_total_tmp_sem.loc[str(c+1), g]
        yerr = data_mean_temp_sem.reset_index()['counts']
        # print(yerr)
        plt.yscale('log')
        #plt.xscale('log')
        
        # make plots
        plt.errorbar(x, y, yerr = yerr, color = colors[g], alpha = 0.2)

    plt.legend(['wildtype', 'knockout'])
    plt.yscale('log')
    fig.savefig(os.path.join(photon_histo_summary_path, 'photon_mean' + '_c' +  str(c+1) + '.png'))
    plt.close()

# ----------------------------------------------------- #
