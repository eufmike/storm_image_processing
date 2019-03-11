#@ UIService uiService
#@ LogService log
#@ File(label="Select a directory", style="directory", value="/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging", persist=false) path
#@ String(label="Folder for output", value = "analysis_20190308", persist=false) dir_output
#@ String(label="Folder for raw images", value = "03_testdata", persist=false) dir_srcimg
#@ String(label="Folder for tif images", value = "preproimg", persist=false) dir_preproimg
#@ Boolean(label="Batchmode", value=false, persist=true) batchmodeop
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
from ij.macro import Interpreter

# Import JAVA modules
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

def tstormanlysis(inputfile, csvdatapath, dcpath, hppath, imwidth, imheight):
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
	IJ.run(inputfile, "Show results table", ("action=drift path=[" + dcpath + "] magnification=5.0 "
		"method=[Cross correlation] save=true steps=10 showcorrelations=false"))

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
	filesavercheck(fs, os.path.dirname(hppath), os.path.basename(hppath))
	
	# close windows --------------------------------------------------------
	inputfile.close()
	imp_histogram.close()
	driftwd.close()
	
# Functions Section Ends ----------------------------------------------------- #

# STORM Image Analysis ------------------------------------------------------- #

def run_script(path=path):
	
	import gc
	path = str(path)
	print('Preparing ...')
	# load image
	# path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
	# dir_srcimg = 'testdata'
	dir_src = 'resource'
	# dir_output = 'analysis_20190122'
	if batchmodeop:
		Interpreter.batchMode = True
	# create input path
	# input dir
	dir_preprocessing = 'preprocessing'
	# dir_preproimg = 'preproimg'
	dir_imginfo = 'imginfo'
	dir_imgmetadata = 'imgmetadata'	
	file_imgstat = 'imgstat.csv'

	# dir_imgmetadata 
	# create input path
	path_srcimg = os.path.join(path, dir_output, dir_preprocessing, dir_preproimg)
	path_imgstat = os.path.join(path, dir_output, dir_preprocessing, dir_imginfo, file_imgstat)
	# print("path_srcimg")
	# print(path_srcimg)
	
	# output dir
	dir_tstorm = 'tstorm'
	dir_csvdata = 'csvdata'
	dir_driftcorr = 'driftcorr'
	dir_histogram_plot = 'histogram_plot'

	# output path
	path_csvdata = os.path.join(path, dir_output, dir_tstorm, dir_csvdata)
	path_driftcorr = os.path.join(path, dir_output, dir_tstorm, dir_driftcorr)
	path_histogram_plot = os.path.join(path, dir_output, dir_tstorm, dir_histogram_plot)
	# check the existence of output folders
	targetfolders = [path_csvdata, path_driftcorr, path_histogram_plot]
	dircheck(targetfolders)
	
	pendingfllist = []
	pendingpathlist_ip = []
	pendingpathlist_op_csv = []
	pendingpathlist_op_dc = []
	pendingpathlist_op_hp = []
	
	# return the pending files
	src_ext = '.tif'
	op_ext = '.csv'

	for imgsubfolder in os.listdir(path_srcimg):
		path_ip_tmp = os.path.join(path_srcimg, imgsubfolder)
		path_op_tmp = os.path.join(path_csvdata, imgsubfolder)
		pendingfllist_temp, pendingpathlist_ip_temp, pendingpathlist_op_temp = getpendinglist(path_ip_tmp, path_op_tmp, src_ext = src_ext, op_ext = op_ext)
		pendingfllist = pendingfllist + pendingfllist_temp
		pendingpathlist_ip = pendingpathlist_ip + pendingpathlist_ip_temp
		pendingpathlist_op_csv = pendingpathlist_op_csv + pendingpathlist_op_temp
		
		# create subfolders for channel
		pathcsvfile_c = os.path.join(path_csvdata, imgsubfolder)
		dircheck(pathcsvfile_c)
		pathdcfile_c = os.path.join(path_driftcorr, imgsubfolder)
		dircheck(pathdcfile_c)
		pathhpfile_c = os.path.join(path_histogram_plot, imgsubfolder)
		dircheck(pathhpfile_c)

		# create path for dataoutput
		dc_tmp = []
		hp_tmp = []
		for j in pendingfllist:
			dc_tmp.append(os.path.join(pathdcfile_c, j + '.json'))
			hp_tmp.append(os.path.join(pathhpfile_c, j + '.tif'))
		pendingpathlist_op_dc = pendingpathlist_op_dc + dc_tmp
		pendingpathlist_op_hp = pendingpathlist_op_hp + hp_tmp
		
	print(pendingpathlist_ip)
	'''
	print(pendingpathlist_op_csv)
	print(pendingpathlist_op_dc)
	print(pendingpathlist_op_hp)
	'''
	
	img_stat = {}
	# read stat.csv exist
	with open(path_imgstat, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		csv_header = next(csvreader)
		for row in csvreader:
			img_stat[row[0]] = {
				"filename": row[1],
				"xsize": row[2],
				"ysize": row[3],
				"nSlices": row[4], 
				"nFrames": row[5],
				"nChannels": row[6],
				"sizebytes": row[7]
			}
	
	# print(img_stat)


	for i in range(len(pendingfllist)):
		# prepare filename
		imgname = pendingfllist[i]
		ipfilename = pendingpathlist_ip[i]
		opcsvfile = pendingpathlist_op_csv[i]
		opdcfile = pendingpathlist_op_dc[i]
		ophpfile = pendingpathlist_op_hp[i]
		print("Start Analysis: {}".format(ipfilename))
		'''
		print(opcsvfile)
		print(opdcfile)
		print(ophpfile)
		'''
		
		# load stat
		stattmp = img_stat[imgname]

		# open image
		imp = IJ.openImage(ipfilename)
		imp.show()

		# run storm analysis
		tstormanlysis(imp, opcsvfile, opdcfile, ophpfile, stattmp['xsize'], stattmp['ysize'])

		time.sleep(3)
		
		# garbage collection
		gc.collect()

		time.sleep(3)
		gc.collect()

	# time.sleep(3)
	if batchmodeop:
		Interpreter.batchMode = False
	import gc
	gc.collect()
	
	return

if __name__ in ['__builtin__','__main__']:
	run_script()
	print("Script Ends ...")
	# quit script after running the script
	from java.lang import System
	System.exit(0)
