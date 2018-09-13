# make plot
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

# create input/output path
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
csvdatadir = 'csvdata'
inputfilepath = os.path.join(path, analysis_dir, csvdatadir)

outputfolder = 'csvdata_inference'
histo = 'histogram'

inputfilelist = []
inputfileabslist = []
opfilelist_histo = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            inputfilepath_tmp = os.path.join(directory, file_name)
            inputfilelist.append(file_name)
            inputfileabslist.append(inputfilepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            filepath_png = os.path.join(path, analysis_dir, outputfolder, histo, filenamepng)
            opfilelist_histo.append(filepath_png)

print(inputfilelist)
print(inputfileabslist)
print(opfilelist_histo)

#for i in range(len(inputfilelist)):
for i in range(len(inputfilelist)-1, len(inputfilelist)):
    filepath = inputfileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    data_sorted = data.sort_values(by = ['intensity [photon]'], ascending=False)
    display(data_sorted.head(10))

    fig = plt.figure()
    plt.hist(data['intensity [photon]'], 100)
    plt.yscale('log')
    plt.grid(True)
    fig.savefig(opfilelist_histo[i])
        
