# %%
# %load_ext autoreload
# %autoreload 2

import os, sys
import re
import pprint
import pandas as pd

from sys import platform as sys_pf
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style as styl
styl.use('default')

from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs


# Functions Section Begins ----------------------------------------------------- #

# Functions Section Ends ----------------------------------------------------- #

# %%
# parameter
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
analysis_subdir = 'spacial_test'
ip_dir = 'spacialdata'
nchannel = 2
op_dir = 'plot'
'''

path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
analysis_subdir = str(sys.argv[3])
ip_dir = str(sys.argv[4])
nchannel = int(sys.argv[5])
op_dir = str(sys.argv[6])

ip_path = os.path.join(path, analysis_dir, analysis_subdir, ip_dir)

# create op dir
dir_for_check = []
opK_dir = 'plot_K'
opL_dir = 'plot_L'
opH_dir = 'plot_H'
optotal_dir = 'plot_total'

opK_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir, opK_dir)
opL_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir, opL_dir)
opH_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir, opH_dir)
optotal_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir, optotal_dir)
dir_for_check.append(opK_path)
dir_for_check.append(opL_path)
dir_for_check.append(opH_path)
dir_for_check.append(optotal_path)

for i in range(nchannel):
    dir_tmp = os.path.join(opK_path, str(i+1))
    dir_for_check.append(dir_tmp)
    dir_tmp = os.path.join(opL_path, str(i+1))
    dir_for_check.append(dir_tmp)
    dir_tmp = os.path.join(opH_path, str(i+1))
    dir_for_check.append(dir_tmp)
DirCheck(dir_for_check)
print(dir_for_check)

# %%
# set parameter
colors = {
    'wildtype': 'red',
    'knockout': 'blue'
}

group = {
    'wildtype': 'w',
    'knockout': 'k'
}
ippath = {
    'spatialdata':{
        'dir': ip_path,
        'ext': '.csv',
    },
}

oppath = {
    'plot_K': {
        'name': 'K(r)',
        'colname': 'K_r',
        'dir': opK_path,
        'ext': '.png'
    },
    'plot_L': {
        'name': 'L(r)',
        'colname': 'L_r',
        'dir': opL_path,
        'ext': '.png'
    },
    'plot_H': {
        'name': 'H(r)',
        'colname': 'H_r',
        'dir': opH_path,
        'ext': '.png'
    },
}

# %%
# create filenamelist
filenamelist = ListFiles(os.path.join(ip_path, str(1)), '.csv')['filelist']
mainfilelist = GetGrpFLs(filenamelist, nchannel, group, ippath, oppath)
pprint.pprint(mainfilelist)

# %%
# plot the results from repliey's K, L and H
# individual images
data_list = []
for c in range(nchannel):
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filepath = mainfilelist[str(c+1)][g]['spatialdata'][i]
            data = pd.read_csv(filepath, header=0, index_col = 0)
            data['filename'] = mainfilelist[str(c+1)][g]['filename_ip'][i]
            data['group'] = g
            data['channel'] = str(c+1)
            data_list.append(data)
            
            for j, val in oppath.items(): 
                # print(val['colname'])
                fig, axes = plt.subplots()
                plt.plot(data['r'], data[val['colname']])
                oppath_tmp = mainfilelist[str(c+1)][g][j][i]
                fig.savefig(oppath_tmp)
                axes.set_xlim(0, 2500)
                plt.close()
                
data_total = pd.concat(data_list, axis = 0)

# %%
# print(data_total)
# print(data_total.shape)
# %%
# plot K_r, L_r and H_r in one single graph
for c in range(nchannel):
    print(c)
    data_temp = data_total[data_total['channel'] == str(c+1)]
    print(data_temp)
    for j, val in oppath.items():
        print(j)
        print(val)
        print(len(oppath))
        
        fig, axes = plt.subplots()
        
        for g in group.keys():
            for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
            # for i in range(10):
                filename_tmp = mainfilelist[str(c+1)][g]['filename_ip'][i]
                print(filename_tmp)
                data_plot = data_temp[data_temp['filename'] == filename_tmp]
                print(data_plot)
                plt.plot(data_plot['r'], data_plot[val['colname']], color = colors[g], alpha = 0.2)
        
        fig.savefig(os.path.join(optotal_path, val['colname'] + '_c' +  str(c+1) + '.png'))
        axes.set_xlim(0, 2500)
        optotal_path
        plt.close()
        
# %%
data_total = pd.DataFrame(data_total)
# display(data_total)
# %%
data_grouped_mean = data_total.groupby(by = ['channel', 'group', 'r']).mean()
# print(data_grouped_mean)
data_grouped_sem = data_total.groupby(by = ['channel', 'group', 'r']).sem()
# print(data_grouped_sem)

# %%
# plot mean and SEM for K_r, L_r and H_r
for c in range(nchannel):
    for j, val in oppath.items(): 

        dpi = 300
        fig = plt.figure(dpi = dpi)
        fig.set_figheight(5)
        fig.set_figwidth(5)
        
        axes = plt.subplot(111)
        for g in group.keys():
            data_mean_temp = data_grouped_mean.loc[str(c+1), g]
            x = data_mean_temp.reset_index()['r']
            y = data_mean_temp.reset_index()[val['colname']]
            data_sem_temp = data_grouped_sem.loc[str(c+1), g]
            yerr = data_sem_temp.reset_index()[val['colname']]
            plt.errorbar(x, y, yerr = yerr, color = colors[g], alpha = 0.2)
            
        plt.legend(g)
        plt.gcf().subplots_adjust(left=0.15)
        plt.xlabel('Radius (nm)')
        plt.ylabel(val['name'])
        axes.spines['right'].set_visible(False)
        axes.spines['top'].set_visible(False)
        axes.set_xlim(0, 2500)

        fig.savefig(os.path.join(optotal_path, val['colname'] + '_mean_c' +  str(c+1) + '.png'))
        plt.close()
