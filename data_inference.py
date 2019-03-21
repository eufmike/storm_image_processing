# %% make plot
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# %%
# histogram for photon count
# create input path
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
csvdatadir = 'csvdata'
inputfilepath = os.path.join(path, analysis_dir, csvdatadir)

# create output path
outputfolder = 'csvdata_inference'
histo = 'histogram'
outputfilepath = os.path.join(path, analysis_dir, outputfolder, histo)
if not os.path.exists(outputfilepath):
		os.makedirs(outputfilepath)

inputfilelist = []
inputfileabslist = []
opfilelist_cbc_histo = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            inputfilepath_tmp = os.path.join(directory, file_name)
            inputfilelist.append(file_name)
            inputfileabslist.append(inputfilepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            filepath_png = os.path.join(outputfilepath, filenamepng)
            opfilelist_cbc_histo.append(filepath_png)

print(inputfilelist)
print(inputfileabslist)
print(opfilelist_cbc_histo)

# %%
for i in range(len(inputfilelist)):
# for i in range(len(inputfilelist)-1, len(inputfilelist)):
    filepath = inputfileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    data_sorted = data.sort_values(by = ['intensity [photon]'], ascending=False)
    display(data_sorted.head(10))

    fig = plt.figure()
    plt.hist(data['intensity [photon]'], 100)
    plt.yscale('log')
    plt.grid(True)
    fig.savefig(opfilelist_cbc_histo[i])

# %%
# CBC trend 
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
st_dir = 'spacial_test'
csvdatadir = 'CBC_results'
inputfilepath = os.path.join(path, analysis_dir, st_dir, csvdatadir)

outputfolder = 'csvdata_inference'
CBC_histo = 'CBC_histogram'

inputfilelist = []
inputfileabslist = []
opfilelist_cbc_histo = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            inputfilepath_tmp = os.path.join(directory, file_name)
            inputfilelist.append(file_name)
            inputfileabslist.append(inputfilepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            filepath_png = os.path.join(path, analysis_dir, outputfolder, CBC_histo, filenamepng)
            opfilelist_cbc_histo.append(filepath_png)

print(inputfilelist)
print(inputfileabslist)
print(opfilelist_cbc_histo)

bins  = np.linspace(-1.0, 1.0, num = 21)
print(bins)

# %%
group = {'w': 'wildtype', 'k': 'knockout'}
data_all = pd.DataFrame()

for i in range(len(inputfilelist)):
# for i in range(1):
    # get file name
    filepath = inputfileabslist[i]
    print(filepath)
    
    # get file basename
    filename = os.path.basename(filepath).replace('.csv', '')
    print(filename)
    
    # extract group
    pattern = r'[0-9]{4}_[0-9]{2}_[0-9]{2}_(.*?)[0-9]'
    try:
        found = re.search(pattern, filename).group(1)
    except AttributeError:
        fount = ''

    group_tmp = group[found]
    print(group_tmp)

    # load file
    data = pd.read_csv(filepath, header=0)
    data = data.dropna()
    data['cbc'] = data['cbc'].apply(pd.to_numeric)
    data['binned'] = pd.cut(data['cbc'], bins)
    data['filename'] = filename
    data['group'] = group_tmp
    
    display(data.loc[:, ['cbc', 'binned', 'filename', 'group']].head(10))
    # print(data.columns.values)

    data_all = pd.concat([data_all, data], ignore_index= True)

    '''
    fig = plt.figure()
    plt.hist(data['cbc'], 40)
    # plt.yscale('log')
    plt.grid(True)
    plt.xlim(-1, 1)
    fig.savefig(opfilelist_cbc_histo[i])
    '''

# %%
print(data_all.shape)

# %%
display(data_all)
# %%
# CBC data
# binning 
aggregations = {
    'id' : 'count',
    'group': 'max'
}
data_grouped = data_all.groupby(['filename', 'binned'], as_index=False).agg(aggregations)
display(data_grouped)

aggregations = {
    'id' : {'average' : 'mean','sem': 'sem'}
}
data_grouped_2 = data_grouped.groupby(['group', 'binned'], as_index=False).agg(aggregations)
display(data_grouped_2)


# %%
# filename
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
csvdatadir = 'csvdata_inference'
outputplot = os.path.join(path, analysis_dir, csvdatadir, 'CBC_results', 'CBC_results.png')
print(outputplot)

# create bins
plot_bins = np.linspace(-0.975, 0.975, num = 20)
print(plot_bins)

width = 0.040
fig = plt.figure(figsize = (12,5), dpi = 100)
ax = fig.add_subplot(111)

data_wt = data_grouped_2.loc[data_grouped_2['group'] == 'wildtype']
data_ko = data_grouped_2.loc[data_grouped_2['group'] == 'knockout']
ax.bar(plot_bins - width/2, data_wt['id']['average'], width, yerr=data_wt['id']['sem'], capsize=2)
ax.bar(plot_bins + width/2, data_ko['id']['average'], width, yerr=data_ko['id']['sem'], capsize=2)

ax.set_xlim(-1.1, 1.1)

fig.savefig(outputplot)