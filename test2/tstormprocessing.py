import sys
# print(sys.version)

from ij import IJ
import os
import csv
from ij.io import FileSaver

# ---- Start Functions ----#
def FileSaverCheck(outputdir, filename):
	'''
	This function will check if the file exist and report file status
	'''
	if os.path.exists(outputdir) and os.path.isdir(outputdir):  
  		print "folder exists:", outputdir
  		filepath = os.path.join(outputdir, filename) # Operating System-specific  
  		if os.path.exists(filepath):
  			print "File exists! Not saving the image, would overwrite a file!"  
  		elif fs.saveAsTiff(filepath):
  			print "File saved successfully at ", filepath  
	else:  
  		print "Folder does not exist or it's not a folder!" 
	
	
def tstormanlysis(inputfile, csvdatapath):
	'''
	TSTORMANALYSIS will use predefined parameter for storm analysis in "ThunderSTORM"
	'''
	
	IJ.run(inputfile, "Camera setup", "offset=166.0 isemgain=true photons2adu=8.8 gainem=300.0 pixelsize=160.0")
	IJ.run(inputfile, "Run analysis", ("filter=[Wavelet filter (B-Spline)] "  
		"scale=2.0 order=3 detector=[Local maximum] connectivity=8-neighbourhood "
		"threshold=std(Wave.F1) estimator=[PSF: Integrated Gaussian] sigma=1.6 "
		"fitradius=3 method=[Weighted Least squares] full_image_fitting=false " 
		"mfaenabled=false renderer=[No Renderer]"))
	IJ.run(inputfile, "Show results table", ("action=drift magnification=5.0 "
		"method=[Cross correlation] save=false steps=5 showcorrelations=false"))
	IJ.run(inputfile, "Show results table", "action=density neighbors=5 radius=50.0 dimensions=2D")

	IJ.run(inputfile, "Export results", ("filepath=[" + 
		csvdatapath + 
		"] "
		"fileformat=[CSV (comma separated)] "
		"sigma=true intensity=true chi2=true "
		"offset=true saveprotocol=true "
		"x=true y=true bkgstd=true "
		"id=true uncertainty=true frame=true"))
	

	
# ---- End Functions ---- #


# load image
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
image_dir = '03_testdata'
analysis_dir = 'analysis'
csvdatadir = 'csvdata'

csvdatapath = os.path.join(dir, analysis_dir, csvdatadir)
path = os.path.join(dir, resource_dir, image_dir)


# create a file list for all images
filelist = []
fileabslist = []
for directory, dir_names, file_names in os.walk(path):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			filepath_tmp =  os.path.join(directory, file_name)
			filelist.append(file_name)
			fileabslist.append(filepath_tmp)

# image processing
inputdir = 'crop_img'

#for i in range(len(filelist)): 
for i in range(1):
	
	C1_filename = filelist[i].replace('.nd2', '') + '_c1.tif'
	C1_filepath = os.path.join(dir, analysis_dir, inputdir, C1_filename)
	print(C1_filepath)
	
	C1_opcsvfile = os.path.join(csvdatapath, filelist[i].replace('.nd2', '') + '_c1.csv')
	print(C1_opcsvfile)

	
	imp_c1 = IJ.openImage(C1_filepath)
	imp_c1.show()
	
	tstormanlysis(imp_c1, C1_opcsvfile)
	
	
