# Temp -------------------------------------- #
from ij import IJ
from ij import plugin
from ij import WindowManager as wm
imp_all = IJ.getImage()
imp_basename = imp_all.title.replace(".nd2", "")
#------------------------------------------- #

nFrames = imp_all.getNFrames()

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