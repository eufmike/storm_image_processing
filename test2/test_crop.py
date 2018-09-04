
# prepare environment ------------------------------------
from ij.io import FileSaver
from ij import IJ
import os

# ---- Start Functions ----#
def FileSaverCheck(outputdir, filename):
	if os.path.exists(outputdir) and os.path.isdir(outputdir):  
  		print "folder exists:", outputdir
  		filepath = os.path.join(outputdir, filename) # Operating System-specific  
  		if os.path.exists(filepath):
  			print "File exists! Not saving the image, would overwrite a file!"  
  		elif fs.saveAsTiff(filepath):
  			print "File saved successfully at ", filepath  
	else:  
  		print "Folder does not exist or it's not a folder!" 

# ---- End Functions ---- #


imp = IJ.getImage()
print(imp.title.replace('.nd2', ''))

# define workspace
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
outputdir = 'crop_img'
path = os.path.join(dir, analysis_dir, outputdir)

# define region ------------------------------------------
x_size = "128" 
y_size = "128"
x = "160"
y = "224"
# run macro
IJ.run(imp, "Specify...", "width=" + x_size + " height=" + y_size + " x=" + x + " y=" + y)


# save c1 image ------------------------------------------
IJ.run(imp, "Duplicate...", "duplicate channels=1")
imp_c1 = IJ.getImage()
fs = FileSaver(imp_c1)
filename = imp.title.replace('.nd2', '') + '_c1' + '.tif'
FileSaverCheck(path, filename)
imp_c1.close()

# save c2 image ------------------------------------------

IJ.run(imp, "Duplicate...", "duplicate channels=2")
imp_c2 = IJ.getImage()
fs = FileSaver(imp_c2)
filename = imp.title.replace('.nd2', '') + '_c2' + '.tif'
FileSaverCheck(path, filename)
imp_c2.close()

# functions ------------------------------------------




'''
imp_c2 = IJ.getImage()
'''