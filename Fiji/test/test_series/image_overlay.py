from ij import IJ 
from ij import gui
from ij import ImagePlus
import java.awt.Color as Color

imp = IJ.getImage()

# get the size of the image
xsize = imp.getWidth()
ysize = imp.getHeight()

# create a Overlay obj
overlay = gui.Overlay()

# ROI ----------------------------------------------------

# create roi for annotation (text with box)
roi = [(xsize/2) - (xsize/4), (ysize/2) - (ysize/4), xsize/2, ysize/2]
box_roi = gui.Roi(roi[0], roi[1], roi[2], roi[3])
# set color (RGB)
box_roi.setStrokeColor(Color(153, 204, 255))
# add the roi to the overlay
overlay.add(box_roi)

# --------------------------------------------------------

# Text ---------------------------------------------------
text_roi = gui.TextRoi(roi[0] + 3, roi[1] + 3, "text box")
# set color (RGB)
text_roi.setStrokeColor(Color(153, 204, 255))
# set font
text_roi.setFont("Arial", 10, 0)
overlay.add(text_roi)

# --------------------------------------------------------

imp.setOverlay(overlay)
imp.flatten()
