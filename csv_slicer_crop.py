# %%
# slice the csv according to the frame size
import os, sys
import pandas as pd
from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs

# from tkinter import *

# Functions Section Begins ----------------------------------------------------- #

# Functions Section Ends ----------------------------------------------------- #

# create input path
# load the csv file
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190325'
analysis_subdir = 'tstorm'
csvdata_dir = 'csvdata_sliced'
nchannel = 2 
crop_region = 3
'''
path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
analysis_subdir = str(sys.argv[3])
csvdata_dir = str(sys.argv[4])
nchannel = int(sys.argv[5])
crop_region = int(sys.argv[6])
op_dir = str(sys.argv[7])

ip_path = os.path.join(path, analysis_dir, analysis_subdir, csvdata_dir)

# create output path
dir_for_check = []
# op_dir = 'csvdata_crop'
op_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir)
dir_for_check.append(op_path)
for i in range(nchannel):
	dir_tmp = os.path.join(op_path, str(i+1))
	dir_for_check.append(dir_tmp)
print(dir_for_check)
DirCheck(dir_for_check)

# %%
# load crop data
dir_par = 'par'
path_cropdata = os.path.join(path, analysis_dir, dir_par, 'cropsize.csv')
df_cropdata = pd.read_csv(path_cropdata, header = 0)
# display(df_cropdata)

# %%
# load image stat
path_imgstat = os.path.join(path, analysis_dir, 'preprocessing', 'imginfo', 'imgstat.csv')
df_imgstat = pd.read_csv(path_imgstat, header = 0)
# display(df_imgstat)

# %%
# covert ROI in pixel to µm
df_cropdata['x_min_nm'] = df_cropdata['x'] * 160
df_cropdata['y_min_nm'] = df_cropdata['y'] * 160
df_cropdata['dx_nm'] = df_cropdata['dx'] * 160
df_cropdata['dy_nm'] = df_cropdata['dy'] * 160
df_cropdata['x_max_nm'] = df_cropdata['x_min_nm'] + df_cropdata['dx_nm']
df_cropdata['y_max_nm'] = df_cropdata['y_min_nm'] + df_cropdata['dy_nm']

# display(df_cropdata)
print(df_cropdata.shape[0])
# %%
# slice the csv file
#for i in range(1):

for i in range(df_cropdata.shape[0]):
    imgname = df_cropdata['name'][i]
    x_min = df_cropdata['x_min_nm'][i]
    x_max = df_cropdata['x_max_nm'][i]
    y_min = df_cropdata['y_min_nm'][i]
    y_max = df_cropdata['y_max_nm'][i]
    img_region = df_cropdata['img'][i]
    for j in range(nchannel):
        path_csv_ip = os.path.join(ip_path, str(j+1), imgname + '.csv')
        print(path_csv_ip)
        data = pd.read_csv(path_csv_ip, header=0)
        data_sliced = data[(data['x [nm]'] >= x_min) & (data['x [nm]'] < x_max) & \
                            (data['y [nm]'] >= y_min) & (data['y [nm]'] < y_max)]
                            
        path_csv_op = os.path.join(op_path, str(j+1), imgname + '_r' + str(img_region) + '.csv')
        data_sliced.to_csv(path_csv_op, index = False)
        