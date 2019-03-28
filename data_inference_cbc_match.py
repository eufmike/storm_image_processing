# %% make plot
import numpy as np
import re
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
from itertools import repeat
mpl.style.use('default')

# %%
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
# %%
nchannels = 2

# histogram for photon count
# create input path
dir_check = []

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
st_dir = 'spacial_test'
cbccsv_dir = 'CBC_results_th_match'
cbccsv_path = os.path.join(path, analysis_dir, st_dir, cbccsv_dir)

# create output path
CBC_histo_dir = 'CBC_histogram_th_match'
CBC_histo_sum_dir = 'CBC_histogram_summary_th_match'
CBC_histo_path = os.path.join(path, analysis_dir, st_dir, CBC_histo_dir)
CBC_histo_sum_path = os.path.join(path, analysis_dir, st_dir, CBC_histo_sum_dir)

for c in range(nchannels):
    dir_check.append(os.path.join(CBC_histo_path, str(c+1)))
dir_check.append(os.path.join(CBC_histo_sum_path))

# check dir
dircheck(dir_check)

# %%
# Grouped by the channels and treatment ------------------------------------------ #
filelist = {}

filenamelist = listfiles(os.path.join(cbccsv_path, '1'), '.csv')['filelist']
filedir = ['ip_filename', 'ip_path', 'op_histogram']
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
        op_th_filepath = []
        for f in filelist_temp: 
            filepath_tmp =  os.path.join(cbccsv_path, str(c+1), f)
            ip_filepath.append(filepath_tmp)

            filename_tmp_png = f.replace('.csv', '.png')
            op_intensity_filepath_temp = os.path.join(CBC_histo_path, str(c+1), filename_tmp_png)
            op_intensity_filepath.append(op_intensity_filepath_temp)

        filelist[str(c+1)][group][filedir[0]] = filelist_temp
        filelist[str(c+1)][group][filedir[1]] = ip_filepath
        filelist[str(c+1)][group][filedir[2]] = op_intensity_filepath


print(filelist)
# ----------------------------------------------------- #

# %%
binsize = 20
bin_list = np.linspace(-1.0, 1.0, binsize+1)
print(bin_list)
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
            plt.hist(data['cbc'], binsize)
            # plt.yscale('log')
            plt.grid(True)
            plt.xlim(-1, 1)
            opfilename = filelist[str(c+1)][group][filedir[2]][i]
            print(opfilename)
            fig.savefig(opfilename)
            plt.close()

data_total = pd.concat(data_list, axis = 0)

# %%
print(data_total.shape)
display(data_total.head())
# %%
# CBC visualization
# Plot individual CBC data
for c in channel:
    print(c)
    data_temp = pd.DataFrame(data_total[data_total['channel'] == str(c+1)])
    fig, axes = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    
    colors = ['red', 'blue']
    for m in range(len(treatment)):
        for i in range(len(filelist[str(c+1)][treatment[m]][filedir[0]])):
        # for i in range(10):
            filename_tmp = filelist[str(c+1)][treatment[m]][filedir[0]][i]
            print(filename_tmp)
            data_plot = data_temp[data_temp['filename'] == filename_tmp]
            data_plot_temp = pd.cut(data_plot['cbc'], bins = bin_list)
            data_plot_bin = data_plot.copy()
            data_plot_bin['bins'] = data_plot_temp
            data_plot_bin = data_plot_bin.groupby(by = 'bins').size()
            data_plot_bin = data_plot_bin.reset_index()
            data_plot_bin = data_plot_bin.rename(index = int, columns={0: 'counts'})
            
            x = bin_list[0: -1]
            y = data_plot_bin.reset_index()['counts']/data_plot.shape[0]
            
            plt.step(x, y, color = colors[m], where = 'post', alpha = 0.2)
    
    fig.savefig(os.path.join(CBC_histo_sum_path, 'CBC_total' + '_c' +  str(c+1) + '.png'))
    plt.close()
    
# %%
# mergeed plot, grouped by channel and treatment, average and errorbar
for c in channel:
    print('channel: {}'.format(c))
    # load data
    data_temp = data_total[data_total['channel'] == str(c+1)]
    #print(data_temp)
    
    # prepare binned data
    data_total_tmp = data_total
    data_total_tmp['bins'] = pd.cut(data_total['cbc'], bins = bin_list)
    # group by bins
    data_total_count_tmp = data_total_tmp.groupby(by = ['channel', 'group', 'filename', 'bins']).size()
    data_total_count_tmp = data_total_count_tmp.reset_index()
    data_total_count_tmp = data_total_count_tmp.rename(index = int, columns={0: 'counts'})
    display(data_total_count_tmp.head())

    # reset index for total events
    data_total_size_tmp = data_total_count_tmp.groupby(by = ['channel', 'group', 'filename']).sum()
    data_total_size_tmp = data_total_size_tmp.reset_index()
    data_total_size_tmp = data_total_size_tmp.rename(index = int, columns={'counts': 'total_events'})
    display(data_total_size_tmp.head())

    df_temp = data_total_count_tmp.merge(data_total_size_tmp)
    df_temp['counts_normed'] = df_temp['counts']/df_temp['total_events']
    display(df_temp)

    # 2nd group by 
    data_total_tmp_mean = df_temp.groupby(by = ['channel', 'group', 'bins']).mean()['counts_normed']
    data_total_tmp_sem = df_temp.groupby(by = ['channel', 'group', 'bins']).sem()['counts_normed']

    # plot mean dataset
    fig, axes = plt.subplots()
    fig.set_figheight(5)
    fig.set_figwidth(12)
    colors = ['red', 'blue']
    for m in range(len(treatment)):
        print(m)
        data_mean_temp_mean = data_total_tmp_mean.loc[str(c+1), treatment[m]]
        x = bin_list[0: -1] + 0.05
        print(x)
        y = data_mean_temp_mean.reset_index()['counts_normed']
        data_mean_temp_sem = data_total_tmp_sem.loc[str(c+1), treatment[m]]
        yerr = data_mean_temp_sem.reset_index()['counts_normed']
        # print(yerr)
        
        # make plots
        width = 0.040
        # plt.errorbar(x, y, yerr = yerr, color = colors[m], alpha = 0.2)
        if m == 0:
            plt.bar(x - width/2, y, width = width, yerr=yerr, capsize=2, color = colors[m])
        else: 
            plt.bar(x + width/2, y, width = width, yerr=yerr, capsize=2, color = colors[m])

    fig.savefig(os.path.join(CBC_histo_sum_path, 'CBC_mean' + '_c' +  str(c+1) + '.png'))
    plt.close()

# ----------------------------------------------------- #
