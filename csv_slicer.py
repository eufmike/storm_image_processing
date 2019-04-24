
# %%
'''
%load_ext autoreload
%autoreload 2
'''
# slice the csv according to the frame size
import os, sys
import pandas as pd
from core.fileop import DirCheck, ListFiles, GetPendingList, GetGrpFLs

# Functions Section Begins ----------------------------------------------------- #


# Functions Section Ends ----------------------------------------------------- #

# create input path
# load the csv file
'''
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190419'
analysis_subdir = 'tstorm'
csvdata_dir = 'csvdata'
nchannel = 2 
# define the range of time frame
frame_start = 5000
frame_end = 10001
'''
path = str(sys.argv[1])
analysis_dir = str(sys.argv[2])
analysis_subdir = str(sys.argv[3])
csvdata_dir = str(sys.argv[4])
nchannel = int(sys.argv[5])
frame_start = int(sys.argv[6])
frame_end = int(sys.argv[7])
op_dir = str(sys.argv[8])

ip_path = os.path.join(path, analysis_dir, analysis_subdir, csvdata_dir)

# create output path
dir_for_check = []
# op_dir = 'csvdata_sliced'
op_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir)
dir_for_check.append(op_path)
for i in range(nchannel):
	dir_tmp = os.path.join(op_path, str(i+1))
	dir_for_check.append(dir_tmp)
print(dir_for_check)
DirCheck(dir_for_check)

# %%
# prepare input file list
pendingfllist = []
pendingpathlist_input = []
pendingpathlist_output = []
for i in range(nchannel):
	src_dir = os.path.join(ip_path, str(i+1))
	op_dir = os.path.join(op_path, str(i+1))
	pendingfllist_tmp, pendingpathlist_input_tmp, pendingpathlist_output_tmp = GetPendingList(src_dir, op_dir, src_ext = '.csv', op_ext = '.csv')
	pendingfllist = pendingfllist + pendingfllist_tmp
	pendingpathlist_input = pendingpathlist_input + pendingpathlist_input_tmp
	pendingpathlist_output = pendingpathlist_output + pendingpathlist_output_tmp
# print(pendingfllist)
print('pendingpathlist_input')
print(pendingpathlist_input)
print('pendingpathlist_output')
print(pendingpathlist_output)

# %%
# slice the csv file
#for i in range(1):
for i in range(len(pendingfllist)):
    filepath = pendingpathlist_input[i]
    data = pd.read_csv(filepath, header=0)
    data = pd.DataFrame(data)
    print(data.head())

    data_sliced = data[(data['frame'] >= frame_start) & (data['frame'] < frame_end)]
    print(data_sliced.head())
    print(data_sliced.tail())
    
    print(pendingpathlist_output[i])
    data_sliced.to_csv(pendingpathlist_output[i], index = False)
    