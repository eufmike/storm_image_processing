
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
csvdata_dir = 'csvdata'
nchannel = 2 

ip_path = os.path.join(path, analysis_dir, analysis_subdir, csvdata_dir)

# create output path
dir_for_check = []
op_dir = 'csvdata_sliced'
op_path = os.path.join(path, analysis_dir, analysis_subdir, op_dir)
dir_for_check.append(op_path)
for i in range(nchannel):
	dir_tmp = os.path.join(op_path, str(i+1))
	dir_for_check.append(dir_tmp)
dircheck(dir_for_check)

# %%
# prepare input file list
pendingfllist = []
pendingpathlist_input = []
pendingpathlist_output = []
for i in range(nchannel):
	src_dir = os.path.join(ip_path, str(i+1))
	op_dir = os.path.join(op_path, str(i+1))
	pendingfllist_tmp, pendingpathlist_input_tmp, pendingpathlist_output_tmp = getpendinglist(src_dir, op_dir, src_ext = '.csv', op_ext = '.csv')
	pendingfllist = pendingfllist + pendingfllist_tmp
	pendingpathlist_input = pendingpathlist_input + pendingpathlist_input_tmp
	pendingpathlist_output = pendingpathlist_output + pendingpathlist_output_tmp
# print(pendingfllist)
print(pendingpathlist_input)
print(pendingpathlist_output)



# %%
# define the range of time frame
frame_start = 7000
frame_end = 10001

# slice the csv file
#for i in range(1):
for i in range(len(pendingfllist)):
    filepath = pendingpathlist_input[i]
    data = pd.read_csv(filepath, header=0)
    data = pd.DataFrame(data)
    print(data.head())

    data_sliced = data[(data['frame'] >= frame_start) & (data['frame'] < frame_end)]
    print(data_sliced.head())
    print(data_sliced.tail())
    
    print(pendingpathlist_output[i])
    data_sliced.to_csv(pendingpathlist_output[i], index = False)
    