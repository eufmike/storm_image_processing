#@ UIService uiService
#@ LogService log
#@ File(label="Select a directory", style="directory", value="/Users/mike_data_analysis/Documents/projects/STORM_imaging", persist=false) path
#@ String(label="Folder for raw images", value = "testdata", persist=false) dir_srcimg
#@ String(label="Folder for output", value = "analysis_20190305", persist=false) dir_output
#@ String(label="Folder for input images", value = "crop_img", persist=false) inputdir
#@ String(label="imwidth", value = "30.0", persist=false) imwidth
#@ String(label="imheight", value = "30.0", persist=false) imheight

print('Script Starts')
print('Importing modules ...')

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

# Import JAVA modules
import java.awt.Color as Color
import java.lang.System.gc as javagc

# Import Bio-Formats
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

# Parameter
# imwidth = "30.0"
# imheight = "30.0"
channelcount = 2

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
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif type(targetpaths) is list: 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def listfiles(path, extension = None):
	"""
	
	"""
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(path):
		# print(file_names)
		
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(extension)):
				file_name_base = file_name.replace(extension, '')
				filepath_tmp =  os.path.join(directory, file_name)
				fileabslist.append(filepath_tmp)
	
	return fileabslist
	
def getpendinglist(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv'):
	"""
	getpendinglist compares the files from src_dir and the accomplisjed file in op_dir, 
	then creates a pending list of unprocessed image. 
	"""
	
	srclist = listfiles(src_dir, src_ext)
	print(srclist)
	oplist = listfiles(op_dir, op_ext)
	print(oplist)

	oplist_basename = []
	for i in oplist:
		name = os.path.basename(i)
		basename = os.path.splitext(name)[0]
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

def tstormanlysis(inputfile, csvdatapath, hppath):
	'''
	TSTORMANALYSIS will use predefined parameter for storm analysis in "ThunderSTORM"
	'''

	# set camera
	IJ.run(inputfile, "Camera setup", "offset=166.0 isemgain=true photons2adu=8.8 gainem=300.0 pixelsize=160.0")
	
	# run STORM analysis
	IJ.run(inputfile, "Run analysis", ("filter=[Wavelet filter (B-Spline)] "  
		"scale=2.0 order=3 detector=[Local maximum] connectivity=8-neighbourhood "
		"threshold=std(Wave.F1) estimator=[PSF: Integrated Gaussian] sigma=1.6 "
		"fitradius=3 method=[Weighted Least squares] full_image_fitting=false " 
		"mfaenabled=false renderer=[No Renderer]"))
	resultwd = wm.getWindow('ThunderSTORM: results')

	# run drift correction
	IJ.run(inputfile, "Show results table", ("action=drift magnification=5.0 "
		"method=[Cross correlation] save=false steps=5 showcorrelations=false"))
	driftwd = wm.getWindow('Drift')
	
	IJ.run(inputfile, "Show results table", "action=density neighbors=5 radius=50.0 dimensions=2D")

	IJ.run(inputfile, "Export results", ("filepath=[" + 
		csvdatapath + 
		"] "
		"fileformat=[CSV (comma separated)] "
		"sigma=true intensity=true chi2=true "
		"offset=true saveprotocol=true "
		"x=true y=true bkgstd=true "
		"id=true uncertainty=true frame=true"))
	IJ.run(inputfile, "Visualization", 
		"imleft=0.0 imtop=0.0 "
		"imwidth=" + imwidth + " imheight="+ imheight + " "
		"renderer=[Averaged shifted histograms] "
		"magnification=5.0 colorizez=false threed=false shifts=2")
	imp_histogram = IJ.getImage()
	fs = FileSaver(imp_histogram)
	FileSaverCheck(fs, os.path.dirname(hppath), os.path.basename(hppath))
	
	# close windows --------------------------------------------------------
	inputfile.close()
	imp_histogram.close()
	driftwd.close()
	
# Functions Section Ends ----------------------------------------------------- #

# STORM Image Analysis ------------------------------------------------------- #

def run_script(path=path):
	
	import gc
	path = str(path)

	# load image
	# path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
	# dir_srcimg = 'testdata'
	dir_src = 'resource'
	# dir_output = 'analysis_20190122'
	
	# create input path
	# input dir
	dir_preprocessing = 'preprocessing'
	dir_preproimg = 'preproimg'
	dir_imginfo = 'imginfo'
	dir_imgmetadata = 'imgmetadata'	
	file_imgstat = 'imgstat.csv'

	# dir_imgmetadata 
	# create input path
	path_srcimg = os.path.join(path, dir_output, dir_preprocessing, dir_preproimg)
	print("path_srcimg")
	print(path_srcimg)
	
	# output dir
	dir_csvdata = 'csvdata'
	dir_histogram_plot = 'histogram_plot'

	# output path
	path_csvdata = os.path.join(path, dir_output, dir_csvdata)
	path_histogram_plot = os.path.join(path, dir_output, dir_histogram_plot)

	# check the existence of output folders
	targetfolders = [path_csvdata, dir_histogram_plot]
	dircheck(targetfolders)
	

	# return the pending files
	src_ext = '.tif'
	op_ext = '.csv'
	pendingfllist, pendingpathlist_input, pendingpathlist_output = getpendinglist(path_srcimg, path_csvdata, src_ext = src_ext, op_ext = op_ext)
	print(pendingfllist)
	print(pendingpathlist_input)
	print(pendingpathlist_output)

	'''
	# create a file list for all images
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(rawimgpath):
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name)
	
	print(pendingfllist)

	# image processing
	# inputdir = 'crop_img'

	channelnames = []
	for i in range(channelcount):
		tempname = 'c' + str(i+1)
		channelnames.append(tempname)
	print(channelnames)
	'''
	'''
	for i in range(len(filelist)): 
		for k in range(channelcount):
			filebasename = filelist[i].replace('.nd2', '') + '_' + str(j+1) + '_' + channelnames[k]
			filepath = os.path.join(path, dir_output, inputdir, filebasename + '.tif')
			opcsvfile = os.path.join(path, dir_output, csvdatadir, filebasename + '.csv')
			hp = os.path.join(path, dir_output, hpdir, filebasename + '.tif')
			print(filebasename)
			print(filepath)
			print(opcsvfile)
			print(hp)
			
			if os.path.exists(opcsvfile) and os.path.exists(hp):  
				print("File exists: " + filebasename + '.tif')
				print("Skip analysis")
			else:  
				# open image
				print("Start Analysis: " + filebasename + '.tif')
				imp = IJ.openImage(filepath)
				imp.show()
				# run storm analysis
				tstormanlysis(imp, opcsvfile, hp)

			break
		break

	'''	
	time.sleep(3)

	import gc
	gc.collect()

	return



if __name__ in ['__builtin__','__main__']:
	run_script()
	print("Script Ends ...")
	# quit script after running the script
	from java.lang import System
	System.exit(0)
