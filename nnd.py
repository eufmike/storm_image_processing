# %%
import os, sys
import re
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
def Distance(point_ref, point_target):
    a_delta = point_target - point_ref
    a_square = np.square(a_delta)
    a_sum = np.sum(a_square, axis = 1, keepdims = True)
    dist = np.sqrt(a_sum)

    return dist

def BfMinDistIdx(point_ref, point_target):
    
    min_dist_list = []
    min_dist_idx_list = []
    for point in point_ref:
        dist = Distance(point, point_target)
        min_dist_list.append(dist.min())
        min_dist_idx_list.append(dist.argmin())
    return (min_dist_list, min_dist_idx_list)



# %%
# test code
'''
point1 = np.array([[2, 3], [2, 30], [40, 50], [5, 1], [12, 10], [6, 4]])
point2 = np.array([[3, 4], [5, 10], [43,12]])

test = Distance(point2[0], point1)
print(test)

test_2 = BfMinDistIdx(point2, point1)
print(test_2)
'''

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
nnd_data_dir = 'int_grid_data_filtered'
nnd_data_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_dir)
print(nnd_data_path)

# output folder
nnd_data_dist_dir = 'int_grid_data_dist'
nnd_data_dist_path = os.path.join(path, analysis_dir, spacialtest_dir, nnd_dir, nnd_data_dist_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(nnd_data_dist_path, str(c+1)))

DirCheck(dir_check)

# %%
# create pending filename and file path 
src_ext = '.csv'
op_ext = '.csv'

flnamels, flpth_ip, flpth_op = GetPendingList(nnd_data_path, nnd_data_dist_path, src_ext = src_ext, op_ext = op_ext)


# %%
data_c1_count = []
data_c2_count = []

for i in range(len(flnamels)):
    inputdata_c1 = os.path.join(nnd_data_path, str(1), flnamels[i] + '.csv') 
    inputdata_c2 = os.path.join(nnd_data_path, str(2), flnamels[i] + '.csv')

    data_c1 = pd.read_csv(inputdata_c1, header = 0)
    data_c2 = pd.read_csv(inputdata_c2, header = 0)
    
    data_c1_count.append(len(data_c1))
    data_c2_count.append(len(data_c2))
    
    print(flnamels[i])
    print(len(data_c1))
    print(len(data_c2))

    if (len(data_c1) == 0) or (len(data_c2) == 0):
        continue
    else: 
        # display(data_c1)
        point_c1 = np.array(data_c1.loc[:, ['X', 'Y']])
        point_c2 = np.array(data_c2.loc[:, ['X', 'Y']])

        mindist_c1c2 = BfMinDistIdx(point_c1, point_c2)
        print(mindist_c1c2)
        
        mindist_c2c1 = BfMinDistIdx(point_c2, point_c1)
        print(mindist_c2c1)

        data_c1['min_dist'] = mindist_c1c2[0]
        data_c1['min_dist_idx'] = mindist_c1c2[1]

        data_c2['min_dist'] = mindist_c2c1[0]
        data_c2['min_dist_idx'] = mindist_c2c1[1]

        outputdata_c1 = os.path.join(nnd_data_dist_path, str(1), flnamels[i] + '.csv') 
        outputdata_c2 = os.path.join(nnd_data_dist_path, str(2), flnamels[i] + '.csv')

        data_c1.to_csv(outputdata_c1, index=False) 
        data_c2.to_csv(outputdata_c2, index=False)

    