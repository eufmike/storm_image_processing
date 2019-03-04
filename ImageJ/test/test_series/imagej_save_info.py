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