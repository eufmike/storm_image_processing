
# %%
# slice the csv according to the frame size
import os, sys
import pandas as pd
# from tkinter import *

# create input path
# load the csv file
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_012019'
csvdatadir = 'csvdata'
filepath = os.path.join(path, analysis_dir, csvdatadir)

filelist = []
fileabslist = []
for directory, dir_names, file_names in os.walk(filepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
			filepath_tmp =  os.path.join(directory, file_name)
			filelist.append(file_name)
			fileabslist.append(filepath_tmp)

print(filelist)
print(fileabslist)

# create output path
outputfolder = 'csvdata_sliced'
outputfilepath = os.path.join(path, analysis_dir, outputfolder)
if not os.path.exists(outputfilepath):
		os.makedirs(outputfilepath)

outputfilelist = []
outputfileabslist = []
for directory, dir_names, file_names in os.walk(filepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
			filepath_tmp =  os.path.join(outputfilepath, file_name)
			outputfilelist.append(file_name)
			outputfileabslist.append(filepath_tmp)

print(outputfileabslist)


# %%
# define the range of time frame
frame_start = 5000
frame_end = 10001

# slice the csv file
#for i in range(1):
for i in range(len(filelist)):
    filepath = fileabslist[i]
    data = pd.read_csv(filepath, header=0)
    data = pd.DataFrame(data)
    print(data.head())

    data_sliced = data[(data['frame'] >= frame_start) & (data['frame'] < frame_end)]
    print(data_sliced.head())
    print(data_sliced.tail())
    
    print(outputfileabslist[i])
    data_sliced.to_csv(outputfileabslist[i], index = False)
    