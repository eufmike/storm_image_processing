# %% make plot
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Functions Section Begins ----------------------------------------------------- #
def dircheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if isinstance(targetpaths, str): 
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif isinstance(targetpaths, list): 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def listfiles(path, extension = None):
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(path):
		# print(file_names)
		
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(extension)):
				filepath_tmp =  os.path.join(directory, file_name + extension)
				filelist.append(file_name)
				fileabslist.append(filepath_tmp)
	
	return {'filelist': filelist,
			'fileabslist': fileabslist}               
# Functions Section Ends ----------------------------------------------------- #

nchannels = 2

# %%
# histogram for photon count
# create input path
dir_check = []

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
tstorm_dir = 'tstorm'
st_dir = 'spacial_test'
stormcsv_dir = 'csvdata_crop'
cbccsv_dir = 'CBC_results'
stormcsv_path = os.path.join(path, analysis_dir, tstorm_dir, stormcsv_dir)
cbccsv_path = os.path.join(path, analysis_dir, st_dir, cbccsv_dir)
print(stormcsv_path)

# create output path
photon_histo_dir = 'photons_hist'
CBC_histo_dir = 'CBC_histogram'
photon_histo_path = os.path.join(path, analysis_dir, st_dir, photon_histo_dir)
CBC_histo_path = os.path.join(path, analysis_dir, st_dir, CBC_histo_dir)
for c in range(nchannels):
    dir_check.append(os.path.join(photon_histo_path, str(c+1)))
    dir_check.append(os.path.join(CBC_histo_path, str(c+1)))

print(photon_histo_path)

# %%
# check dir
dircheck(dir_check)
'''
inputfilelist = []
inputfileabslist = []
opfilelist_cbc_histo = []

for c in range(nchannels):
    for directory, dir_names, file_names in os.walk(os.path.join(stormcsv_path, str(c+1))):
        for file_name in file_names:
            if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
                inputfilepath_tmp = os.path.join(directory, file_name)
                # print(inputfilepath_tmp)
                inputfilelist.append(file_name)
                inputfileabslist.append(inputfilepath_tmp)
                filenamepng = file_name.replace('.csv', '.png')
                filepath_png = os.path.join(photon_histo_path, str(c+1), filenamepng)
                opfilelist_cbc_histo.append(filepath_png)

print(inputfilelist)
print(inputfileabslist)
print(opfilelist_cbc_histo)
'''
# %%
'''
# plot the histgram
for i in range(len(inputfilelist)):
# for i in range(len(inputfilelist)-1, len(inputfilelist)):
    filepath = inputfileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    data_sorted = data.sort_values(by = ['intensity [photon]'], ascending=False)
    # display(data_sorted.head(10))

    fig = plt.figure()
    plt.hist(data['intensity [photon]'], 100)
    plt.yscale('log')
    plt.grid(True)
    fig.savefig(opfilelist_cbc_histo[i])
    plt.close()
'''
# %%
# Grouped by the channels and treatment ------------------------------------------ #
filelist = {}

filenamelist = listfiles(os.path.join(stormcsv_path, '1'), '.csv')['filelist']
filedir = ['ip_filename', 'ip_path', 'op_intensity']
treatment = ['wildtype', 'knockout']
channel = list(range(2))
print(channel)

# group the data by the treatment 
for c in channel:
    filelist[str(c+1)] = {}
    for group in treatment:
        filelist[str(c+1)][group] = {}    
        
        # create list
        filelist_temp = []
        for l in filenamelist: 
            if group == 'wildtype':
                x = re.search('(.*)_w{1}[0-9]{1}_(.*)', l)
            else: 
                x = re.search('(.*)_k{1}[0-9]{1}_(.*)', l) 
            try: 
                found = x.group(0)
                filelist_temp.append(found)
            except AttributeError:
                found = ''

        ip_filepath = []
        op_intensity_filepath = []
        for f in filelist_temp: 
            filepath_tmp =  os.path.join(stormcsv_path, str(c+1), f)
            ip_filepath.append(filepath_tmp)

            filename_tmp_png = f.replace('.csv', '.png')
            op_intensity_filepath_temp = os.path.join(photon_histo_path, str(c+1), filename_tmp_png)
            op_intensity_filepath.append(op_intensity_filepath_temp)

        filelist[str(c+1)][group][filedir[0]] = filelist_temp
        filelist[str(c+1)][group][filedir[1]] = ip_filepath
        filelist[str(c+1)][group][filedir[2]] = op_intensity_filepath

print(filelist)
# ----------------------------------------------------- #
# %%
data_list = []
for c in channel:
    for group in treatment:
        for i in range(len(filelist[str(c+1)][group][filedir[0]])):
        # for i in range(10):
            filepath = filelist[str(c+1)][group][filedir[1]][i]
            # print(filepath)
            data = pd.read_csv(filepath, header=0, index_col = 0)
            data['filename'] = filelist[str(c+1)][group][filedir[0]][i]
            data['group'] = group
            data['channel'] = str(c+1)
            data_list.append(data)

            # print(data)
            fig = plt.figure()
            plt.hist(data['intensity [photon]'], 100)
            plt.yscale('log')
            plt.grid(True)
            opfilename = filelist[str(c+1)][group][filedir[2]][i]
            print(opfilename)
            fig.savefig(opfilename)
            plt.close()

data_total = pd.concat(data_list, axis = 0)


# %%
data_total = pd.DataFrame(data_total)
display(data_total)
# ----------------------------------------------------- #
# %%
for c in channel:
    print(c)
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    photon_max = max(data_temp['intensity [photon]'])
    print(photon_max)
    binsize = 1000
    photon_bin_max = photon_max//binsize
    print(photon_bin_max)
    bin_list = list(range(0, (int(photon_bin_max) + 2) * binsize, binsize))
    print(bin_list)
    fig, axes = plt.subplots()
    colors = ['red', 'blue']
    
    for m in range(len(treatment)):
        for i in range(len(filelist[str(c+1)][treatment[m]][filedir[0]])):
        # for i in range(10):
            filename_tmp = filelist[str(c+1)][treatment[m]][filedir[0]][i]
            # print(filename_tmp)
            data_plot = data_temp[data_temp['filename'] == filename_tmp]
            # print(data_plot)
            plt.hist(data_plot['intensity [photon]'], bins= bin_list, histtype = 'step', color = colors[m], alpha = 0.2)
            plt.yscale('log')
            plt.xscale('log')
        
    fig.savefig(os.path.join(photon_histo_path, 'photon' + '_c' +  str(c+1) + '.png'))
    axes.set_xlim(0, 2500)
    plt.close()
    
    

# ----------------------------------------------------- #
# %%
# CBC trend 

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