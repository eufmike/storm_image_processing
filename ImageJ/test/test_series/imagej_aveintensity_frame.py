# Temp -------------------------------------- #
import os
import csv
from ij import gui
from ij import IJ
from ij import plugin
from ij import WindowManager as wm
from ij.process import ImageStatistics as IS 
imp_main = IJ.getImage()
imp_basename = imp_main.title.replace(".nd2", "")
#------------------------------------------- #
options = IS.MEAN | IS.MEDIAN | IS.MIN_MAX

def getStatistics(imp):  
  """ Return statistics for the given ImagePlus """  
  global options  
  ip = imp.getProcessor()  
  stats = IS.getStatistics(ip, options, imp.getCalibration())  
  return stats.mean, stats.median, stats.min, stats.max  

#------------------------------------------- #
csvpath_test = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_test'
test_filename = 'intensity_ROI.csv'
csvfilepath = os.path.join(csvpath_test, test_filename)

xsize = imp_main.getWidth()
ysize = imp_main.getHeight()
nframe = imp_main.getNFrames()
nchannel = imp_main.getNChannels()

roi = [(xsize/2) - 64, (ysize/2) - 64, 128, 128]
crop_roi = gui.Roi(roi[0], roi[1], roi[2], roi[3])

stats_allframe = []

for i in range(nchannel):
	IJ.run(imp_main, "Duplicate...", "duplicate channels=" + str(i+1))
	imp_channel = IJ.getImage()
	imp_channel.setRoi(crop_roi)	
	
	for j in range(nframe):
		imp_channel.setT(j+1)
		stats = list(getStatistics(imp_channel))
		head = [i+1, j+1]
		stats_allframe.append(head + stats)
	
	'''
	fs = FileSaver(imp)
	filename = imp.title.replace('.nd2', '') + '_c' + 'str(i+1)' + '.tif')
	FileSaverCheck(outputpath, filename)
	imp.close()
	'''
	
# start a csv writer
with open(csvfilepath, 'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=",")
	csvwriter.writerow(['channel', 'frame', 'mean', 'median','min', 'max'])
	for i in range(len(stats_allframe)):
		csvwriter.writerow(stats_allframe[i])