#@ UIService uiService
#@ LogService log
#@ File(label="Select a directory", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging", persist=false) path
#@ String(label="Folder for output", value = "analysis_20190419", persist=false) dir_output
#@ File(label="Select a directory", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_20190419/tstorm/csvdata_sliced_T_ROI", persist=false) ippath_j
#@ String(label="folder for CBC output .csv", value = "CBC", persist=false) op_dir
#@ String(label="Subfolder for CBC output .csv", value = "CBC_results", persist=false) op_subdir
#@ Boolean(label="Batchmode", value=false, persist=true) batchmodeop


# For ImageJ/Fiji
import sys
import os
import re
import csv
import gc
import time
from ij import IJ
from ij import plugin
from ij import gui
from ij.io import FileSaver
from ij import WindowManager as wm
from ij.process import ImageStatistics as IS 
from ij.macro import Interpreter

# Import JAVA modules
import java.awt.Color as Color
import java.lang.System.gc as javagc

# Import Bio-Formats
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

# Functions Section Begins ----------------------------------------------------- #
print('Loading functions ...')
# log.info('Loading functions ...')
  		
def dircheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if type(targetpaths) is unicode: 
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif type(targetpaths) is list: 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def getprocessedimg(op_dir, pattern = r'(.+?).'):
	"""
	NOT USING
	getprocessedimg check the output folder and create a list of processed data
	pattern: the pattern re search
	"""
	processed_img = []
	for (directory, dir_names, file_names) in os.walk(op_dir):
		for file_name in file_names:
			# print(file_name)

			# search the processed files by using re.search
			m = re.search(pattern, file_name)
			if m: 
				# print(m)
				file_name_temp = m.group(1)
				processed_img.append(file_name_temp)
	# replace the duplicated filenames
	processed_img = list(set(processed_img))
	
	return (processed_img)

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
def run_script(path=path):
	print('Preparing ...')
	
	import gc
	path = str(path)
	nchannels = 2
	 
	if batchmodeop:
		Interpreter.batchMode = True
	
	#ip_path = os.path.join(path, dir_output, ip_dir, ip_subdir)
	ip_path = str(ippath_j)
	op_path = os.path.join(path, dir_output, op_dir, op_subdir)
	
	for c in range(nchannels): 
		dircheck(os.path.join(op_path, str(c+1)))

	pendingfllist = []
	pendingpathlist_ip = []
	pendingpathlist_op = []

	src_ext = '.csv'
	op_ext = '.csv'

	filename = listfiles(os.path.join(ip_path, '1'), '.csv')['filelist']
	print(filename)
	
	for i in range(len(filename)):
	# for i in range(1):
		# input path
		c1_filename = filename[i].replace('.tif', '.csv')
		c2_filename = filename[i].replace('.tif', '.csv')
		c1_path = os.path.join(ip_path, '1', c1_filename)
		c2_path = os.path.join(ip_path, '2', c2_filename)
		print(c1_path)
		print(c2_path)

		# output path
		op_filename = filename[i].replace('.tif', '.csv')
		op_path_temp_c1 = os.path.join(op_path, '1', op_filename)
		op_path_temp_c2 = os.path.join(op_path, '2', op_filename)
		print(op_path_temp_c1)
		print(op_path_temp_c2)
		
		IJ.run("Import results", "filepath=[" + c1_path + "] fileformat=[CSV (comma separated)] livepreview=false rawimagestack= startingframe=1 append=false")
		
		IJ.run("Import ground-truth", "filepath=[" + c2_path + "] fileformat=[CSV (comma separated)] startingframe=1 append=false")
		IJ.run("CBC", "addcbc=true radiusstep=50 addnncount=true channel1=[Results table] channel2=[Ground-truth table] stepcount=10 dimensions=2D addnndist=true")
		IJ.run("Export results", ("filepath=[" + op_path_temp_c1 + "] "
				"fileformat=[CSV (comma separated)] "
				"sigma=true chi2=true offset=true "
				"cbc=true " 
				"x=true y=true id=true frame=true "
				"nn_dist=true bkgstd=true "
				"uncertainty=true "
				"intensity=true " 
				"neighbors_in_dist_50=true "
				"neighbors_in_dist_100=true "
				"neighbors_in_dist_150=true "
				"neighbors_in_dist_200=true "
				"neighbors_in_dist_250=true "
				"neighbors_in_dist_300=true "
				"neighbors_in_dist_350=true "
				"neighbors_in_dist_400=true "
				"neighbors_in_dist_450=true "
				"neighbors_in_dist_500=true "))
		
		IJ.run("Export ground-truth", ("filepath=[" + op_path_temp_c2 + "] "
				"fileformat=[CSV (comma separated)] "
				"sigma=true chi2=true offset=true "
				"cbc=true " 
				"x=true y=true id=true frame=true "
				"nn_dist=true bkgstd=true "
				"uncertainty=true "
				"intensity=true " 
				"neighbors_in_dist_50=true "
				"neighbors_in_dist_100=true "
				"neighbors_in_dist_150=true "
				"neighbors_in_dist_200=true "
				"neighbors_in_dist_250=true "
				"neighbors_in_dist_300=true "
				"neighbors_in_dist_350=true "
				"neighbors_in_dist_400=true "
				"neighbors_in_dist_450=true "
				"neighbors_in_dist_500=true "))

		imp = IJ.getImage()
		imp.close()
		imp = IJ.getImage()
		imp.close()

		# break

if __name__ in ['__builtin__','__main__']:
	run_script()
	
	# quit script after running the script
	from java.lang import System
	System.exit(0)
	