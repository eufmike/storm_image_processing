import sys
# print(sys.version)

from ij import IJ
import os
import csv
from ij.io import FileSaver

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

# prepare the file path
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
image_dir = '03_testdata'
analysis_dir = 'analysis'
csvfilename = 'cropsize.csv'
csvpath = os.path.join(dir, analysis_dir, csvfilename)

path = os.path.join(dir, resource_dir, image_dir)
#imgfolderlist = os.listdir(path)
#print(imgfolderlist)

# create a file list for all images
filelist = []
fileabslist = []
for directory, dir_names, file_names in os.walk(path):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			filepath_tmp =  os.path.join(directory, file_name)
			filelist.append(file_name)
			fileabslist.append(filepath_tmp)
print(filelist)

# load the cropsize

with open(csvpath, 'rb') as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    # Read each row of data after the header
    dict_list = {}
    for row in csvreader:
        dict_list[row[0]] = row[1:]        
print(csv_header)
print(dict_list)


# load bio-format
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

# define output folder
outputdir = 'crop_img'

for i in range(len(filelist)): 
#for i in range(1):
	
	filename = filelist[i].replace(".nd2", "")
	x_size = dict_list[filename][2]
	y_size = dict_list[filename][3]
	x = dict_list[filename][0]
	y = dict_list[filename][1]

	print(filename, x_size, y_size, x, y)
	
	
	outputpath = os.path.join(dir, analysis_dir, outputdir)	
	
	imps = BF.openImagePlus(fileabslist[i])
	
	for imp in imps:
		imp.show()
	
		# run macro
		IJ.run(imp, "Specify...", "width=" + x_size + " height=" + y_size + " x=" + x + " y=" + y)
	
	
		# save c1 image ------------------------------------------
		IJ.run(imp, "Duplicate...", "duplicate channels=1")
		imp_c1 = IJ.getImage()
		fs = FileSaver(imp_c1)
		filename = imp.title.replace('.nd2', '') + '_c1' + '.tif'
		FileSaverCheck(outputpath, filename)
		imp_c1.close()
	
		# save c2 image ------------------------------------------
		
		IJ.run(imp, "Duplicate...", "duplicate channels=2")
		imp_c2 = IJ.getImage()
		fs = FileSaver(imp_c2)
		filename = imp.title.replace('.nd2', '') + '_c2' + '.tif'
		FileSaverCheck(outputpath, filename)
		imp_c2.close()
		
		imp.close()
	
	del imps
	

'''
imp.close()
'''

'''
filelist = []
for i in imgfolderlist: 
	path_tmp = os.path.join(dir, resource_dir, image_dir, i)
	filelist_tmp = os.listdir(path_tmp)
	filelist_tmp = [f for f in filelist_tmp if (not f.startswith('.')) & (f.endswith('.nd2'))]
	filelist_tmp_dir = [os.path.join(dir, resource_dir, image_dir, f) for f in filelist_tmp]
	filelist = filelist + filelist_tmp_dir

print(filelist)

#for i in range(len(filelist)): 
for i in range(2): 
	imp = IJ.openImage(filelist[i])
	print(i)
'''
