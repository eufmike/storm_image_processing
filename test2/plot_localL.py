# %%
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
spacialtestdir = 'spacial_test'
csvdir = 'datalocalL_test'
inputfilepath = os.path.join(path, analysis_dir, spacialtestdir, csvdir)

outputfolder = 'plot_densitymap'

filelist = []
fileabslist = []
outputfilelist_DM = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            filepath_tmp =  os.path.join(directory, file_name)
            filelist.append(file_name)
            fileabslist.append(filepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            outputfilelist_DM_tmp = os.path.join(path, analysis_dir, spacialtestdir, outputfolder, filenamepng)
            outputfilelist_DM.append(outputfilelist_DM_tmp)

print(filelist)
print(fileabslist)

# %%
for i in range(len(filelist)):
    filepath = fileabslist[i]
    # print(filepath)
    data = pd.read_csv(filepath, header=0)
    
    #print(data)
    
    fig = plt.figure()
    plt.scatter(data['x'], data['y'], c = data['z'], size = 0.2)
    fig.savefig(outputfilelist_DM[i])
    break