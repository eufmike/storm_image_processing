# Temp -------------------------------------- #
import os
import csv
from ij import IJ
from ij import plugin
from ij import WindowManager as wm
imp_main = IJ.getImage()
imp_basename = imp_main.title.replace(".nd2", "")
#------------------------------------------- #
csvpath_test = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_test'

list_xsize = []
list_ysize = []
list_nSlices = []
list_nFrames = []
list_nChannels = []

print(imp_main.getWidth())
list_xsize.append(imp_main.getWidth())
list_ysize.append(imp_main.getHeight())
list_nSlices.append(imp_main.getNSlices())
list_nFrames.append(imp_main.getNFrames())
list_nChannels.append(imp_main.getNChannels())

with open(os.path.join(csvpath_test, 'imageinfo.csv'), 'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=",")
	csvwriter.writerow(['filename', 'xSize', 'ySize', 'nSlices', 'nFrames', 'nChannels'])
	for j in range(len(list_xsize)):
		csvwriter.writerow([imp_basename, list_xsize[j], list_ysize[j], 
						list_nSlices[j], list_nFrames[j], list_nChannels[j]])