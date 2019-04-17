#@ UIService uiService
#@ LogService log
#@ File(label="Select a directory", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging", persist=true) path_j
#@ String(label="Folder for output", value = "analysis_20190308", persist=false) dir_output
#@ File(label="Directory for input image", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_20190308/spacial_test/spacialdata_local_pad_grid", persist=true) ippath_j
#@ File(label="Directory for output binary image", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_20190308/spacial_test/nnd/int_grid_bi", persist=true) op_bi_path_j
#@ File(label="Directory for data", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_20190308/spacial_test/nnd/int_grid_data", persist=true) op_data_path_j
#@ Boolean(label="Batchmode", value=false, persist=true) batchmodeop
print('Script Starts')
print('Importing modules ...')

# For ImageJ/Fiji
import sys
import os
import re
import csv
import gc
import pprint
import time
from ij import IJ
from ij import plugin
from ij import gui
from ij.io import FileSaver
from ij import WindowManager as wm
from ij.process import ImageStatistics as IS 
from ij.macro import Interpreter


# Import JAVA modules
from java.io import File
import java.awt.Color as Color
import java.lang.System.gc as javagc

# Import Bio-Formats
from loci.plugins import BF
from loci.plugins.in import ImporterOptions


# Functions Section Begins ----------------------------------------------------- #
print('Loading functions ...')


def filesavercheck(fs, outputdir, filename):
	
	"""
	FileSaverCheck first check if the input folder exists, 
	then check if the input file exists in the targer folder
	
	If the folder does not exist, it returns error message:
	"Folder does not exist or it's not a folder!"
	If the folder exists but the file also exists:
	File exists! Not saving the image, would overwrite a file!"
	Otherwise, it will save file and return message: 
	"File saved successfully at given filepath"
	 
	Arguments:
	outputdir: output directory
	filename: input file with absolute path
	"""
	
	if os.path.exists(outputdir) and os.path.isdir(outputdir):  
  		print "folder exists:", outputdir
  		filepath = os.path.join(outputdir, filename) # Operating System-specific  
  		if os.path.exists(filepath):
  			print "File exists! Not saving the image, would overwrite a file!"  
  		elif fs.saveAsTiff(filepath):
  			print "File saved successfully at ", filepath  
	else:  
  		print "Folder does not exist or it's not a folder!" 
	
def dircheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	
	# print(type(targetpaths))
	if type(targetpaths) is unicode: 
		# print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif type(targetpaths) is list: 
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
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name)
				fileabslist.append(filepath_tmp)
	
	return {'filelist': filelist,
			'fileabslist': fileabslist}  
	
def getpendinglist(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv'):
	"""
	getpendinglist compares the files from src_dir and the accomplisjed file in op_dir, 
	then creates a pending list of unprocessed image. 
	"""
	
	srclist = listfiles(src_dir, src_ext)
	oplist = listfiles(op_dir, op_ext)

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

# Particle Analysis ------------------------------------------------------- #
def run_script():
	print('Print Script Parameter')
	print('path: {}'.format(path_j))
	print('dir_output: {}'.format(dir_output))
	print('ippath: {}'.format(ippath_j))
	print('op_bi_path: {}'.format(op_bi_path_j))
	print('op_data_path: {}'.format(op_data_path_j))
	print(batchmodeop)
	
	path = str(path_j)
	ippath = str(ippath_j)
	op_bi_path = str(op_bi_path_j)
	op_data_path = str(op_data_path_j)

	print('Preparing ...')
	
	import gc
	
	if batchmodeop:
		Interpreter.batchMode = True

	nchannels = 2
	dir_check = []	
	# create output path
	for c in range(nchannels):
		dir_check.append(os.path.join(op_bi_path, str(c+1)))
		dir_check.append(os.path.join(op_data_path, str(c+1)))

	dircheck(dir_check)

	# create the pending file list ------------------------------------------ #
	pendingfllist = []
	pendingpathlist_ip = []
	pendingpathlist_op_data = []
	pendingpathlist_op_bi = []
	
	# return the pending files ------------------------------------------ #
	filelist = {}

	filenamelist = listfiles(os.path.join(ippath, '1'), '.tif')['filelist']
	filedir = ['ip_filename', 'ip_path', 'op_data', 'op_bi']
	treatment = ['wildtype', 'knockout']
	
	# group the data by the treatment ------------------------------------------ #
	for c in range(nchannels):
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
	        op_bi_filepath = []
	        op_data_filepath = []
	
	        for f in filelist_temp: 
	            ip_filepath_tmp = os.path.join(ippath, str(c+1), f)
	            ip_filepath.append(ip_filepath_tmp)

	            op_data_filepath_temp = os.path.join(op_data_path, str(c+1), f.replace('.tif', '.csv'))
	            op_data_filepath.append(op_data_filepath_temp)
	            op_bi_filepath_temp = os.path.join(op_bi_path, str(c+1), f)
	            op_bi_filepath.append(op_bi_filepath_temp)
	            
	        filelist[str(c+1)][group][filedir[0]] = filelist_temp
	        filelist[str(c+1)][group][filedir[1]] = ip_filepath
	        filelist[str(c+1)][group][filedir[2]] = op_bi_filepath
	        filelist[str(c+1)][group][filedir[3]] = op_data_filepath

	pprint.pprint(filelist)
	
	
	# image processing ------------------------------------------ #
	threshold_c = {'1': 300, '2': 100}

	for c in range(nchannels):
		for group in treatment:
			for i in range(len(filelist[str(c+1)][group][filedir[0]])):
				# open image
				ipfilepath_tmp = filelist[str(c+1)][group][filedir[1]][i]
				op_bi_filepath_tmp = filelist[str(c+1)][group][filedir[2]][i]
				op_data_filepath_tmp = filelist[str(c+1)][group][filedir[3]][i]
				
				print(ipfilepath_tmp)
				print(op_bi_filepath_tmp)
				print(op_data_filepath_tmp)
				
				imp = IJ.openImage(ipfilepath_tmp)
				imp.show()
				IJ.setThreshold(threshold_c[str(c+1)], 5000)
				IJ.run(imp, "Convert to Mask", "")
				
				IJ.run(imp, "Set Measurements...", "area mean standard modal min centroid center perimeter bounding fit shape feret's integrated median skewness kurtosis area_fraction stack redirect=None decimal=9")
				
				IJ.run(imp, "Analyze Particles...", "size=0-Infinity show=Masks display exclude clear")

				# save binary
				imp_bi = IJ.getImage()
				fs = FileSaver(imp_bi)
				fs.saveAsTiff(op_bi_filepath_tmp)
				imp_bi.close()

				# save results
				biresults = wm.getWindow("Results")
				wm.setWindow(biresults)

				IJ.saveAs("Results", op_data_filepath_tmp)
				if not biresults is None:
					biresults.close()
				
				imp.close()
		
	if batchmodeop:
		Interpreter.batchMode = False
	
	return


if __name__ in ['__builtin__','__main__']:
	run_script()
	print("Script Ends ...")
	# quit script after running the script
	# from java.lang import System
	# System.exit(0)
