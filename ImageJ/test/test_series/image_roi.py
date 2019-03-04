from ij import IJ 
from ij import gui
from ij import ImagePlus

imp = IJ.getImage()
xsize = imp.getWidth()
ysize = imp.getHeight()
# get the center part of the image
# Argument for IJ.gui.Roi:
# (double x, double y, double width, double height)
roi = [(xsize/2) - (xsize/4), (ysize/2) - (ysize/4), xsize/2, ysize/2]
# create Roi object
crop_roi = gui.Roi(roi[0], roi[1], roi[2], roi[3])
# add the Roi obj to the image
imp.setRoi(crop_roi)