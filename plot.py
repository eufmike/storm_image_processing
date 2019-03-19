# %%
# make plot
import os, sys
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

dir_for_check = []
opK_path = os.path.join(path, analysis_dir, spacialtestdir, opK_dir)
opL_path = os.path.join(path, analysis_dir, spacialtestdir, opL_dir)
opH_path = os.path.join(path, analysis_dir, spacialtestdir, opH_dir)
dir_for_check.append(opK_path)
dir_for_check.append(opL_path)
dir_for_check.append(opH_path)

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
filelist = []
fileabslist = []
outputfilelist_K = []
outputfilelist_L = []
outputfilelist_H = []

# %%
for c in range(nchannel):
    for directory, dir_names, file_names in os.walk(ip_path):
        for file_name in file_names:
            if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
                filepath_tmp =  os.path.join(directory, file_name)
                filelist.append(file_name)
                fileabslist.append(filepath_tmp)
                filenamepng = file_name.replace('.csv', '.png')
                filepath_K_tmp = os.path.join(opK_path, str(c+1), filenamepng)
                filepath_L_tmp = os.path.join(opL_path, str(c+1), filenamepng)
                filepath_H_tmp = os.path.join(opH_path, str(c+1), filenamepng)
                outputfilelist_K.append(filepath_K_tmp)
                outputfilelist_L.append(filepath_L_tmp)
                outputfilelist_H.append(filepath_H_tmp)

print(filelist)
print(fileabslist)

# %%
for i in range(len(filelist)):
# for i in range(1):
    filepath = fileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    
    print(data)

    fig, axes = plt.subplots()
    plt.plot(data['r'], data['K_r'])
    fig.savefig(outputfilelist_K[i])
    axes.set_xlim(0, 2500)
    plt.close()

    fig, axes = plt.subplots()
    plt.plot(data['r'], data['L_r'])
    fig.savefig(outputfilelist_L[i])
    axes.set_xlim(0, 2500)
    plt.close()

    fig, axes = plt.subplots()
    plt.plot(data['r'], data['H_r'])
    fig.savefig(outputfilelist_H[i])
    axes.set_xlim(0, 2500)
    plt.close()

    

# %%
print(1+1)