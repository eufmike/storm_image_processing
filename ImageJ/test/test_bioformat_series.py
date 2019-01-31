# For ImageJ/Fiji
import sys
# print(sys.version)
import re
from ij import IJ
import os
import csv
from ij.io import FileSaver

filepath = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/resource/03_testdata/2018-10-26/2018_10_26_k1.nd2'
metadata = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_test/metadata'

'''
# parse metadata
from loci.formats import ImageReader
from loci.formats import MetadataTools

reader = ImageReader()
omeMeta = MetadataTools.createOMEXMLMetadata()
reader.setMetadataStore(omeMeta)
reader.setId(filepath)
SizeT = reader.getSizeT()
reader.close()

print(SizeT)
'''


# load bio-format
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

options = ImporterOptions()
# options.setTBegin(0, SizeT)
# options.setTEnd(0, SizeT + 5)
options.setId(filepath)

# open image
imps = BF.openImagePlus(filepath)
for imp in imps:
	imp.show()

# image processing -------------------------- #


# ------------------------------------------- #


# import the source code for ImageJ
from ij import IJ
from ij import plugin
from ij import WindowManager as wm

# get image object
imp_all = IJ.getImage()
# print the base name of the file
imp_basename = imp_all.title.replace(".nd2", "")
print(imp_basename)

# return the info for image
# No need to have image object in the arguments
IJ.run("Show Info...")
# select the info window
img_info = wm.getActiveWindow()
# return the title of the window (optional)
print(img_info.title)
# save the info information
IJ.saveAs("Text", metadata + imp_basename + ".txt")
# close the window
img_info.close()

# Temp -------------------------------------- #
from ij import IJ
from ij import plugin
from ij import WindowManager as wm
imp_all = IJ.getImage()
imp_basename = imp_all.title.replace(".nd2", "")
#------------------------------------------- #
nSlices = imp_all.getNSlices()
nFrames = imp_all.getNFrames()
nChannels = imp_all.getNChannels()
print('nSlices: {}'.format(nSlices))
print('nFrames: {}'.format(nFrames))
print('nChannels: {}'.format(nChannels))

# duplicate the center part of the experiment as image reference

IJ.run(imp_all, "Duplicate...", "duplicate frames="+ str(nFrames/2) + "-" + str(nFrames/2 + 500))
# perform maximum projection
imp_sliced = IJ.getImage()
IJ.run(imp_sliced, "Z Project...", "projection=[Max Intensity]")
imp_sliced.close()

# select windows
imp_max = IJ.getImage()
IJ.selectWindow(imp_max.title)

nSlices = imp_max.getNSlices()
nFrames = imp_max.getNFrames()
nChannels = imp_max.getNChannels()
print(imp_max.title)
print('nSlices: {}'.format(nSlices))
print('nFrames: {}'.format(nFrames))
print('nChannels: {}'.format(nChannels))

# set channel
LUT = imp_max.getChannelLut()
print(LUT)
mode = imp_max.getMode()
print(mode)

imp_max.setC(1)
IJ.run("Green")
IJ.run("Enhance Contrast", "saturated=0.35")
imp_max.setC(2)
IJ.run("Enhance Contrast", "saturated=0.35")

# Temp -------------------------------------- #
from ij import IJ
from ij import plugin
from ij import gui
from ij import WindowManager as wm
import java.awt.Color as Color
imp_max = IJ.getImage()
imp_basename = imp_max.title.replace(".nd2", "")

#------------------------------------------- #

region_1 = [239, 359, 30, 30]
region_2 = [344, 386, 30, 30]
region_3 = [396, 340, 30, 30]
region_all = [236, 337, 193, 83]

roi_dict = {'1': region_1,
			'2': region_2,
			'3': region_3,
			}

deji

# Temp -------------------------------------- #
from ij import IJ
from ij import plugin
from ij import gui
from ij import WindowManager as wm
import java.awt.Color as Color
imp_max = IJ.getImage()
imp_basename = imp_max.title.replace(".nd2", "")

#------------------------------------------- #

IJ.run("Make Composite")
IJ.run("RGB Color")
imp_RGB = IJ.getImage()

# Create empty overlay
overlay = gui.Overlay()

for i in range(len(roi_dict)):
	# print(i)
	# create key
	key = str(i + 1)
	# 
	crop_roi = gui.Roi(roi_dict[key][0], roi_dict[key][1], roi_dict[key][2], roi_dict[key][3])
	crop_roi.setStrokeColor(Color(153, 204, 255))
	overlay.add(crop_roi)
	# ROI text
	text_roi = gui.TextRoi(roi_dict[key][0] + 3 , roi_dict[key][1] + 3, key)
	text_roi.setStrokeColor(Color(153, 204, 255))
	text_roi.setFont("Arial", 10, 0)
	overlay.add(text_roi)


ROIall = gui.Roi(region_all[0], region_all[1], region_all[2], region_all[3])
ROIall.setStrokeColor(Color(255, 204, 153))
overlay.add(ROIall)

imp_RGB.setOverlay(overlay)
imp_RGB.flatten()

# ============================================
from ij.plugin.frame import RoiManager
RM = RoiManager()        # we create an instance of the RoiManager class
rm = RM.getRoiManager()  