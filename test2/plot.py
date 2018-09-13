# make plot
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

# load the csv file
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
spacialtestdir = 'spacial_test'
csvdir = 'data'
inputfilepath = os.path.join(path, analysis_dir, spacialtestdir, csvdir)

outputfolder_K = 'plot_K'
outputfolder_L = 'plot_L'
outputfolder_H = 'plot_H'

filelist = []
fileabslist = []
outputfilelist_K = []
outputfilelist_L = []
outputfilelist_H = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            filepath_tmp =  os.path.join(directory, file_name)
            filelist.append(file_name)
            fileabslist.append(filepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            filepath_K_tmp = os.path.join(path, analysis_dir, spacialtestdir, outputfolder_K, filenamepng)
            filepath_L_tmp = os.path.join(path, analysis_dir, spacialtestdir, outputfolder_L, filenamepng)
            filepath_H_tmp = os.path.join(path, analysis_dir, spacialtestdir, outputfolder_H, filenamepng)
            outputfilelist_K.append(filepath_K_tmp)
            outputfilelist_L.append(filepath_L_tmp)
            outputfilelist_H.append(filepath_H_tmp)

print(filelist)
print(fileabslist)

for i in range(len(filelist)):
# for i in range(1):
    filepath = fileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    
    print(data)
    
    fig = plt.figure()
    plt.plot(data['r'], data['K_r'])
    fig.savefig(outputfilelist_K[i])
    
    fig = plt.figure()
    plt.plot(data['r'], data['L_r'])
    fig.savefig(outputfilelist_L[i])

    fig = plt.figure()
    plt.plot(data['r'], data['H_r'])
    fig.savefig(outputfilelist_H[i])
