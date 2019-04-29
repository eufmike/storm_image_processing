# %%
# slice the csv according to the frame size
import os, sys
import pandas as pd
# from tkinter import *

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
				file_name_base = file_name.replace(extension, '')
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name_base)
				fileabslist.append(filepath_tmp)
	
	return {'filelist': filelist,
			'fileabslist': fileabslist}

def getpendinglist(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv'):
	"""
	getpendinglist compares the files from src_dir and the accomplisjed file in op_dir, 
	then creates a pending list of unprocessed image. 
	"""
	
	srclist = listfiles(src_dir, src_ext)
	srclist = srclist['fileabslist']
	oplist = listfiles(op_dir, op_ext)
	oplist = oplist['fileabslist']

	oplist_basename = []
	for i in oplist:
		name = os.path.basename(i)
		print('name: {}'.format(name))
		basename = os.path.splitext(name)[0]
		print('basename: {}'.format(basename))
		oplist_basename.append(basename)
	
	pendingfllist = []
	pendingpathlist_input = []
	pendingpathlist_output = []
	
	for i in range(len(srclist)):
		srcflname = os.path.basename(srclist[i])
		srcflbasename = os.path.splitext(srcflname)[0]
		
		if not srcflbasename in oplist_basename:
			pendingfllist.append(srcflbasename)
			pendingpathlist_input.append(srclist[i])			
			pendingpathlist_output.append(os.path.join(op_dir, srcflbasename + op_ext))
			
	return (pendingfllist, pendingpathlist_input, pendingpathlist_output)
# Functions Section Ends ----------------------------------------------------- #

# create input path
# load the csv file
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
analysis_subdir = 'tstorm'
csvdata_dir = 'csvdata_crop'
nchannel = 2 
crop_region = 3

ip_path = os.path.join(path, analysis_dir, analysis_subdir, csvdata_dir)

# create output path
dir_for_check = []
op_dir = 'csvdata_crop_th'
op_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir)
dir_for_check.append(op_path)
for i in range(nchannel):
	dir_tmp = os.path.join(op_path, str(i+1))
	dir_for_check.append(dir_tmp)
dircheck(dir_for_check)


# %%
# load crop data
dir_par = 'par'
path_cropdata = os.path.join(path, analysis_dir, dir_par, 'cropsize.csv')
df_cropdata = pd.read_csv(path_cropdata, header = 0)
display(df_cropdata)

# %%
# load image stat
path_imgstat = os.path.join(path, analysis_dir, 'preprocessing', 'imginfo', 'imgstat.csv')
df_imgstat = pd.read_csv(path_imgstat, header = 0)
display(df_imgstat)

# %%
# covert ROI in pixel to µm
df_cropdata['x_min_nm'] = df_cropdata['x'] * 160
df_cropdata['y_min_nm'] = df_cropdata['y'] * 160
df_cropdata['dx_nm'] = df_cropdata['dx'] * 160
df_cropdata['dy_nm'] = df_cropdata['dy'] * 160
df_cropdata['x_max_nm'] = df_cropdata['x_min_nm'] + df_cropdata['dx_nm']
df_cropdata['y_max_nm'] = df_cropdata['y_min_nm'] + df_cropdata['dy_nm']

display(df_cropdata)
print(df_cropdata.shape[0])
# %%
# slice the csv file
#for i in range(1):
threshold = {
    '1': 10000,
    '2': 15000,
}
for i in range(df_cropdata.shape[0]):
    imgname = df_cropdata['name'][i]
    x_min = df_cropdata['x_min_nm'][i]
    x_max = df_cropdata['x_max_nm'][i]
    y_min = df_cropdata['y_min_nm'][i]
    y_max = df_cropdata['y_max_nm'][i]
    img_region = df_cropdata['img'][i]
    for j in range(nchannel):
        path_csv_ip = os.path.join(ip_path, str(j+1), imgname + '.csv')
        print(path_csv_ip)
        data = pd.read_csv(path_csv_ip, header=0)
        data_sliced = data[(data['x [nm]'] >= x_min) & (data['x [nm]'] < x_max) & \
                            (data['y [nm]'] >= y_min) & (data['y [nm]'] < y_max)]
        threshold_temp = threshold[str(j+1)]
        data_sliced = data_sliced[(data['intensity [photon]'] > threshold_temp)]                    
        path_csv_op = os.path.join(op_path, str(j+1), imgname + '_r' + str(img_region) + '.csv')
        data_sliced.to_csv(path_csv_op, index = False)
        