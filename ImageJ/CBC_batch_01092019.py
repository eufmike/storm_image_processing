# For ImageJ/Fiji
import sys
# print(sys.version)
import os
import csv

from ij import IJ
from ij import WindowManager as wm
from ij.io import FileSaver

# Parameter
areacount = 3
channelcount = 2

# create all input/output folder name
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
rawimg_dir = '03_testdata'
analysis_dir = 'analysis_012019'
cropimg_dir = 'crop_img'
inputfolder = 'csvdata_sliced'
outputfilder = 'CBC_results'

# create input/output path
filenamepath = os.path.join(dir, resource_dir, rawimg_dir)
inputpath = os.path.join(dir, analysis_dir, inputfolder)
outputpath = os.path.join(dir, analysis_dir, outputfilder)

# create unexisted folder
if not os.path.exists(outputpath):
		os.makedirs(outputpath)

inputfilelist = []
outputfilelist = []
for directory, dir_names, file_names in os.walk(filenamepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			inputfilepath_tmp =  os.path.join(inputpath, file_name)		
			inputfilelist.append(inputfilepath_tmp)

			outputfilepath_tmp = os.path.join(outputpath, file_name)
			outputfilepath_tmp = outputfilepath_tmp.replace('.nd2', '.csv')
			outputfilelist.append(outputfilepath_tmp)

#print(inputfilelist)
#print(outputfilelist)

for i in range(len(inputfilelist)):
# for i in range(1):
	for j in range(areacount):
		c1_filename = inputfilelist[i].replace('.nd2', '_' + str(j+1) + '_c1.csv')
		c2_filename = inputfilelist[i].replace('.nd2', '_' + str(j+1) + '_c2.csv')
		# print(outputfilelist[i])
		
		IJ.run("Import results", "filepath=[" + c1_filename + "] fileformat=[CSV (comma separated)] livepreview=false rawimagestack= startingframe=1 append=false")
		IJ.run("Import ground-truth", "filepath=[" + c2_filename + "] fileformat=[CSV (comma separated)] startingframe=1 append=false")
		IJ.run("CBC", "addcbc=true radiusstep=50 addnncount=true channel1=[Results table] channel2=[Ground-truth table] stepcount=10 dimensions=2D addnndist=true")
		IJ.run("Export ground-truth", ("filepath=[" + outputfilelist[i] + "] "
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
	