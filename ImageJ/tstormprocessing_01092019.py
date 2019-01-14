# For ImageJ/Fiji
import sys
# print(sys.version)

from ij import IJ
import os
import csv
from ij.io import FileSaver
from ij import WindowManager as wm

# Parameter
imwidth = "30.0"
imheight = "30.0"
areacount = 3
channelcount = 2


# ---- Start Functions ----#
def FileSaverCheck(fs, outputdir, filename):
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
		"magnification=5.0 colorizez=false threed=false shifts=2");
	imp_histogram = IJ.getImage()
	fs = FileSaver(imp_histogram)
	FileSaverCheck(fs, os.path.dirname(hppath), os.path.basename(hppath))
	
	# close windows --------------------------------------------------------
	inputfile.close()
	imp_histogram.close()
	driftwd.close()
	
# ---- End Functions ---- #


# load image
import os
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
rawimgfolder = '03_testdata'
analysis_dir = 'analysis_012019'
csvdatadir = 'csvdata'
hpdir = 'histogram_plot'

# create path
rawimgpath = os.path.join(dir, resource_dir, rawimgfolder)
analysispath = os.path.join(dir, analysis_dir)

# check the existence of output folders
targetfolders = [csvdatadir, hpdir]
for foldername in targetfolders:
	if not os.path.exists(os.path.join(analysispath, foldername)):
		os.makedirs(os.path.join(analysispath, foldername))

# create a file list for all images
filelist = []
fileabslist = []
for directory, dir_names, file_names in os.walk(rawimgpath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			filepath_tmp =  os.path.join(directory, file_name)
			filelist.append(file_name)

print(filelist)

# image processing
inputdir = 'crop_img'


channelnames = []
for i in range(channelcount):
	tempname = 'c' + str(i+1)
	channelnames.append(tempname)
print(channelnames)

for i in range(len(filelist)): 
	for j in range(areacount):
		for k in range(channelcount):
			filebasename = filelist[i].replace('.nd2', '') + '_' + str(j+1) + '_' + channelnames[k]
			filepath = os.path.join(dir, analysis_dir, inputdir, filebasename + '.tif')
			opcsvfile = os.path.join(dir, analysis_dir, csvdatadir, filebasename + '.csv')
			hp = os.path.join(dir, analysis_dir, hpdir, filebasename + '.tif')
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
'''
			break
		break
	break
'''
	
	
