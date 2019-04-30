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

#%%
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
tstorm_dir = 'tstorm'
st_dir = 'spacial_test'
csvdata_dir = 'csvdata_sliced_T_ROI'
nchannel = 2
threshold_photon_c1 = 7000
threshold_photon_c2 = 15000
csv_th_dir = 'csvdata_sliced_T_ROI_th'
cutoff_c1 = 50
cutoff_c2 = 50
csv_th_match_dir = 'csvdata_sliced_T_ROI_th_match'

'''
path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
tstorm_dir = str(sys.argv[3])
st_dir = str(sys.argv[4])
csvdata_dir = str(sys.argv[5])
nchannel = int(sys.argv[6])
threshold_photon_c1 = int(sys.argv[7])
threshold_photon_c2 = int(sys.argv[8])
csv_th_dir = str(sys.argv[9])
cutoff_c1 = int(sys.argv[10])
cutoff_c2 = int(sys.argv[11])
csv_th_match_dir = str(sys.argv[12])


#%%
# create input path
stormcsv_path = os.path.join(path, analysis_dir, tstorm_dir, csvdata_dir)
print(stormcsv_path)

# exportfile
csv_th_path = os.path.join(path, analysis_dir, tstorm_dir, csv_th_dir)
csv_th_match_path = os.path.join(path, analysis_dir, tstorm_dir, csv_th_match_dir)

dir_check = []

for c in range(nchannel):
    dir_check.append(os.path.join(csv_th_path, str(c+1)))
    dir_check.append(os.path.join(csv_th_match_path, str(c+1)))

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
    'stormdata_th': {
        'dir': csv_th_path,
        'ext': '.csv'
    }
}

# %%
# create filenamelist
filenamelist = ListFiles(os.path.join(stormcsv_path, str(1)), '.csv')['filelist']
mainfilelist = GetGrpFLs(filenamelist, nchannel, group, ippath, oppath)
pprint.pprint(mainfilelist)

#%%
# export sliced csv
threshold = {
    '1': threshold_photon_c1,
    '2': threshold_photon_c2,
}

data_list = []
for c in range(nchannel):
    for g in group.keys():
        for i in range(len(mainfilelist[str(c+1)][g]['filename_ip'])):
        # for i in range(10):
            filepath = mainfilelist[str(c+1)][g]['stormdata'][i]
            # print(filepath)
            data = pd.read_csv(filepath, header=0, index_col = False)
            '''
            data['filename'] = filelist[str(c+1)][group][filedir[0]][i]
            data['group'] = group
            data['channel'] = str(c+1)
            '''
            data=data[(data['intensity [photon]'] > threshold[str(c+1)])]
            csvpath = mainfilelist[str(c+1)][g]['stormdata_th'][i]
            data.to_csv(csvpath, index = False)

# ----------------------------------------------------- #
# remove files by the amount of event
# %%
cutoff = {
    '1': cutoff_c1, 
    '2': cutoff_c2,
}
threshold_filelist = {}
for c in range(nchannel):
    filelist_tmp = ListFiles(os.path.join(csv_th_path, str(c+1)), extension = '.csv')['fileabslist']
    filelist_th_tmp = []
    for i in filelist_tmp:
        #print(i)
        data_tmp = pd.read_csv(i, header=0, index_col = False)
        if data_tmp.shape[0] > cutoff[str(c+1)]:
           filelist_th_tmp.append(os.path.basename(i)) 
    threshold_filelist[str(c+1)] = filelist_th_tmp
print(threshold_filelist)

# %%
def compare_intersect(x, y):
    return frozenset(x).intersection(y)

c1 = threshold_filelist['1']
c2 = threshold_filelist['2']
print(len(c1))
print(len(c2))
matches = compare_intersect(c1, c2)
print(len(matches))
# %%
print(matches)

# %%
import shutil
for i in matches: 
    for c in range(nchannel):
        ipfilepath = os.path.join(csv_th_path, str(c+1), i)  
        opfilepath = os.path.join(csv_th_match_path, str(c+1), i)
        shutil.copy2(ipfilepath, opfilepath)
    