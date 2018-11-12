# %%
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid
from matplotlib.mlab import griddata


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


def grid(x, y, z, resX=100, resY=100):
    "Convert 3 column data to matplotlib grid"
    xi = linspace(min(x), max(x), resX)
    yi = linspace(min(y), max(y), resY)
    Z = griddata(x, y, z, xi, yi, interp='linear')
    X, Y = meshgrid(xi, yi)
    return X, Y, Z

# %%
for i in range(len(filelist)):
    filepath = fileabslist[i]
    # print(filepath)
    data = pd.read_csv(filepath, header=0)
    #print(data)
    
    fig = plt.figure(figsize = (5,10))
    
    plt.subplot(211)
    plt.scatter(data['x'], data['y'], c = data['z'], s = 1)

    plt.subplot(212)
    X, Y, Z = grid(data['x'], data['y'], data['z'])
    plt.contourf(X, Y, Z)
    
    plt.show

    break