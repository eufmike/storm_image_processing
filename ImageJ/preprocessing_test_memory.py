#@UIService uiService
#@LogService log

print('Script Starts')
print('Importing modules ...')

# log.info('Script Starts)
# log.info('Importing modules ...')

# Import ImageJ/Fiji package
import sys
import os
import re
import csv
import gc
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


# Functions Section Begins ----------------------------------------------------- #
print('Loading functions ...')
log.info('Loading functions ...')

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

	
# def getpendinglist(src_dir, op_dir, src_ext = '.nd2', op_ext = '.csv', pattern = r'(.+?).'):
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

def getStatistics(imp):  
	""" Return statistics for the given ImagePlus """  
	options = IS.MEAN | IS.MEDIAN | IS.MIN_MAX
	ip = imp.getProcessor()  
	stats = IS.getStatistics(ip, options, imp.getCalibration())  
	return stats.mean, stats.median, stats.min, stats.max  

def garbagecollect(iteration = 3):
	for i in range(iteration):
		gc.collect()
		
# Functions Section Ends ----------------------------------------------------- #



# STORM Image Analysis ------------------------------------------------------- #

# Prepare workspace ========================= #
print('Preparing ...')
log.info('Preparing ...')

# define workspace
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
dir_output = 'analysis_20190220'
pathlist = []

# define temp folder
dir_temp = 'temp'
file_par = 'par'

# create temp folder  
path_temp = os.path.join(path, dir_output, dir_temp)
pathlist.append(path_temp)

# define input folder
dir_src = 'resource'
dir_srcimg = 'test_raw'

# create input path
path_srcimg = os.path.join(path, dir_src, dir_srcimg)

# define output folder
outputdir = 'preprocessing'
dir_preproimg = 'preproimg'
dir_imginfo = 'imginfo'
dir_imgintensity = 'imgintensity'
dir_imgmetadata = 'imgmetadata'
file_imgstat = 'imgstat.csv'

# create output path
path_preproimg = os.path.join(path, dir_output, outputdir, dir_preproimg)
path_imginfo = os.path.join(path, dir_output, outputdir, dir_imginfo)
path_imgintensity = os.path.join(path, dir_output, outputdir, dir_imgintensity)
path_imgmetadata = os.path.join(path_imginfo, dir_imgmetadata)
pathlist.append(path_preproimg)
pathlist.append(path_imginfo)
pathlist.append(path_imgintensity)
pathlist.append(path_imgmetadata)

# create output file path
path_imgstat = os.path.join(path_imginfo, file_imgstat)

# check the existence of output folders and create folders if necessary
dircheck(pathlist)

# Create img list for processing ============ #
# create a file list for all images

# return the processed img
src_ext = '.tif'
pendingfllist, pendingpathlist_input, pendingpathlist_output = getpendinglist(path_srcimg, path_imgintensity, src_ext = src_ext)

print(pendingfllist)
log.info(pendingfllist)

# Processing start ========================== #

processed_filename = [] # <- for trouble shooting
list_xsize = []
list_ysize = []
list_nSlices = []
list_nFrames = []
list_nChannels = []
list_sizebytes = []

# load and crop the image
for i in range(200):
	i = 0
	print(pendingfllist[i])
	
	imps = BF.openImagePlus(pendingpathlist_input[i])
	ipflbasename = pendingfllist[i]
	
	for imp in imps:
		imp.show()
	
	imp_main = IJ.getImage()
	
	# Save img metadata ========================== #
	print('Save image metadata...')
	log.info('Save image metadata...')
	
	# print info for each image
	# No need to have image object in the arguments
	IJ.run("Show Info...")
	# create window name
	img_info_title = 'Info for ' + imp_main.title
	# select the info window
	img_info = wm.getWindow(img_info_title)
	# wm.addWindow(img_info)
	wm.setWindow(img_info)
	
	# save the info information
	IJ.saveAs("Text", os.path.join(path_imgmetadata, (ipflbasename + ".txt")))
	# close the info window
	img_info.close()

	# Save img information ======================== #
	# return basic information of the image
	
	img_x = imp_main.getWidth()
	img_y = imp_main.getWidth()
	img_nslices = imp_main.getNSlices()
	img_nFrames = imp_main.getNFrames()
	img_nChannels = imp_main.getNChannels()
	img_sizebytes = imp_main.getSizeInBytes()
	
	list_xsize.append(img_x)
	list_ysize.append(img_y)
	list_nSlices.append(img_nslices)
	list_nFrames.append(img_nFrames)
	list_nChannels.append(img_nChannels)
	list_sizebytes.append(img_sizebytes)

	# Print information =========================== #
	# return the title of the window (optional)
	print('Current Image File: {}'.format(img_info.title))
	
	# return in log windows
	log.info('Current Image File: {}'.format(img_info.title))
	log.info('SizeZ: {}'.format(img_nslices))
	log.info('SizeT: {}'.format(img_nFrames))
	log.info('SizeC: {}'.format(img_nChannels))
	log.info('Size in Bytes: {}'.format(img_sizebytes))
	
	# Save average intensity  ===================== #
	processed_filename.append(imp_main.title)
	# define the size of center ROI 
	roi = [(img_x/2) - 64, (img_y/2) - 64, 128, 128]
	crop_roi = gui.Roi(roi[0], roi[1], roi[2], roi[3])

	stats_allframe = []	
	
	# Export individual channel  ================== #
	
	for j in range(img_nChannels):
		IJ.run(imp_main, "Duplicate...", "duplicate channels=" + str(j+1))
		imp_channel = IJ.getImage()
		fs = FileSaver(imp_channel)
		
		path_preproim_c = os.path.join(path_preproimg, str(j+1))
		dircheck(path_preproim_c)
		filesavercheck(fs, path_preproim_c, ipflbasename + '.tif')
		
		imp_channel.setRoi(crop_roi)	
		
		for k in range(img_nFrames):
			imp_channel.setT(k+1)
			stats = list(getStatistics(imp_channel))
			head = [j+1, k+1]
			stats_allframe.append(head + stats)

		imp_channel.close()
		del imp_channel
		del fs
	
	# save into a csv ============================= # 
	with open(os.path.join(path_imgintensity, pendingfllist[i] + '.csv'), 'wb') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=",")
		csvwriter.writerow(['channel', 'frame', 'mean', 'median','min', 'max'])
		for j in range(len(stats_allframe)):
			csvwriter.writerow(stats_allframe[j])

	# Ending the loop ============================= #
	# Close image windows and delete variables 
	imp_main.close()
	# not sure if this is necessary
	del stats_allframe
	del imp_main
	del imps

	# Close Exception window 
	'''
	img_ex = wm.getWindow('')
	wm.setWindow(img_ex)
	img_ex.close()
	'''

	# garbage collection
	# garbagecollect()
	gc.collect()
	
	
print('Saving image stats ...')
log.info('Saving image stats ...')

with open(os.path.join(path_imgstat), 'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=",")
	csvwriter.writerow(['image_name', 'ip_file_name','xSize', 'ySize', 'nSlices', 'nFrames', 'nChannels'])
	for i in range(len(list_xsize)):
		csvwriter.writerow([pendingfllist[i], processed_filename[i], list_xsize[i], list_ysize[i], \
					list_nSlices[i], list_nFrames[i], list_nChannels[i]])


print("Script Ends ...")
log.info("Script Ends ...")
'''
def exit(status=""):import gc
    """Exits without displaying a stack trace if :status: is empty"""
    if not status:
        from java.lang import RuntimeException
        from ij import Macro
        raise RuntimeException(Macro.MACRO_CANCELED) #Ignored by IJ2's Console
    else:
        raise RuntimeError(status)

exit()
'''

import gc
gc.collect()


