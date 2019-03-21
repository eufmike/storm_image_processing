# %%
# make plot
import os, sys
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')


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
# parameter
nchannel= 2

# %%
# load the csv file
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
spacialtestdir = 'spacial_test'
csvdir = 'spacialdata'
ip_path = os.path.join(path, analysis_dir, spacialtestdir, csvdir)

opK_dir = 'plot_K'
opL_dir = 'plot_L'
opH_dir = 'plot_H'
optotal_dir = 'plot_total'

dir_for_check = []
opK_path = os.path.join(path, analysis_dir, spacialtestdir, opK_dir)
opL_path = os.path.join(path, analysis_dir, spacialtestdir, opL_dir)
opH_path = os.path.join(path, analysis_dir, spacialtestdir, opH_dir)
optotal_path = os.path.join(path, analysis_dir, spacialtestdir, optotal_dir)
dir_for_check.append(opK_path)
dir_for_check.append(opL_path)
dir_for_check.append(opH_path)
dir_for_check.append(optotal_path)

for i in range(nchannel):
    dir_tmp = os.path.join(opK_path, str(i+1))
    dir_for_check.append(dir_tmp)
    dir_tmp = os.path.join(opL_path, str(i+1))
    dir_for_check.append(dir_tmp)
    dir_tmp = os.path.join(opH_path, str(i+1))
    dir_for_check.append(dir_tmp)
dircheck(dir_for_check)
print(dir_for_check)


# %%
filelist = {}

filenamelist = listfiles(os.path.join(ip_path, '1'), '.csv')['filelist']
# print(filenamelist)

filedir = ['ip_filename', 'ip_path', 'plot_K', 'plot_L', 'plot_H']
treatment = ['wildtype', 'knockout']
channel = list(range(2))
print(channel)

# %%
# group the data by the treatment 
for c in channel:
    filelist[str(c+1)] = {}
    # print(filelist)
    for group in treatment:
        # print(group)
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
        
        # print(filelist_temp)

        ip_filepath = []
        op_path_K = []
        op_path_L = []
        op_path_H = []
        
        for f in filelist_temp: 
            filepath_tmp =  os.path.join(ip_path, str(c+1), f)
            ip_filepath.append(filepath_tmp)
            # print(ip_filepath)

            filename_tmp_png = f.replace('.csv', '.png')
            op_path_K_tmp = os.path.join(opK_path, str(c+1), filename_tmp_png)
            op_path_L_tmp = os.path.join(opL_path, str(c+1), filename_tmp_png)
            op_path_H_tmp = os.path.join(opH_path, str(c+1), filename_tmp_png)
            op_path_K.append(op_path_K_tmp)
            op_path_L.append(op_path_L_tmp)
            op_path_H.append(op_path_H_tmp)

        filelist[str(c+1)][group][filedir[0]] = filelist_temp
        filelist[str(c+1)][group][filedir[1]] = ip_filepath
        filelist[str(c+1)][group][filedir[2]] = op_path_K
        filelist[str(c+1)][group][filedir[3]] = op_path_L
        filelist[str(c+1)][group][filedir[4]] = op_path_H

print(filelist)
# %%
# print keys of the dictionary
for key, value in filelist.items() :
    print (key)
    for key2, value2 in filelist[key].items():
        print(key2)
        for key3, value3 in filelist[key][key2].items():
            print(key3)

# %%
# plot the results from repliey's K, L and H
# individual images for 
variable = ['K_r', 'L_r', 'H_r']
data_list = []
for c in channel:
    for group in treatment:
        for i in range(len(filelist[str(c+1)][group][filedir[0]])):
        # for i in range(10):
            filepath = filelist[str(c+1)][group][filedir[1]][i]
            print(filepath)
            data = pd.read_csv(filepath, header=0, index_col = 0)
            data['filename'] = filelist[str(c+1)][group][filedir[0]][i]
            data['group'] = group
            data['channel'] = str(c+1)
            data_list.append(data)

            # print(data)
            
            for j in range(2, 5): 
                fig, axes = plt.subplots()
                plt.plot(data['r'], data[variable[j-2]])
                fig.savefig(filelist[str(c+1)][group][filedir[j]][i])
                axes.set_xlim(0, 2500)
                plt.close()
        
        data_total = pd.concat(data_list, axis = 0)

# %%
print(data_total)

# %%
for c in channel:
    print(c)
    data_temp = data_total[data_total['channel'] == str(c+1)]
    print(data_temp)
    for j in range(2, 5):
        print(variable[j-2])
        fig, axes = plt.subplots()
        colors = ['red', 'blue']
        for m in range(len(treatment)):
            for i in range(len(filelist[str(c+1)][treatment[m]][filedir[0]])):
            # for i in range(10):
                filename_tmp = filelist[str(c+1)][treatment[m]][filedir[0]][i]
                print(filename_tmp)
                data_plot = data_temp[data_temp['filename'] == filename_tmp]
                print(data_plot)
                plt.plot(data_plot['r'], data_plot[variable[j-2]], color = colors[m], alpha = 0.2)
        
        fig.savefig(os.path.join(optotal_path, variable[j-2] + '_c' +  str(c+1) + '.png'))
        axes.set_xlim(0, 2500)
        optotal_path
        plt.close()
# %%
data_total = pd.DataFrame(data_total)
display(data_total)
# %%
data_grouped_mean = data_total.groupby(by = ['channel', 'group', 'r']).mean()
print(data_grouped_mean)
data_grouped_sem = data_total.groupby(by = ['channel', 'group', 'r']).sem()
print(data_grouped_sem)
# %%
for c in channel:
    for var in variable:
        fig, axes = plt.subplots()
        colors = ['red', 'blue']
        for m in range(len(treatment)):
            data_mean_temp = data_grouped_mean.loc[str(c+1), treatment[m]]
            x = data_mean_temp.reset_index()['r']
            y = data_mean_temp.reset_index()[var]
            data_sem_temp = data_grouped_sem.loc[str(c+1), treatment[m]]
            yerr = data_sem_temp.reset_index()[var]
            plt.errorbar(x, y, yerr = yerr, color = colors[m], alpha = 0.2)

        fig.savefig(os.path.join(optotal_path, var + '_mean_c' +  str(c+1) + '.png'))
        axes.set_xlim(0, 2500)
        optotal_path
        plt.close()


print(data_x.reset_index()['r'])

# %%
print(1+1)

