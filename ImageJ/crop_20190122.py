# For ImageJ/Fiji
import sys
# print(sys.version)
import re
from ij import IJ
import os
import csv
from ij.io import FileSaver

# load bio-format
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

# ---- Start Functions ---- #
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
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
image_dir = '03_testdata'
analysis_dir = 'analysis_20190122'
# define output folder
outputdir = 'crop_img'
croproi = 'crop_region'
# crop csv
csvfilename = 'cropsize_compiled.csv'

csvpath = os.path.join(path, analysis_dir, csvfilename)
imgpath = os.path.join(path, resource_dir, image_dir)

# check the existence of output folders
targetfolders = [outputdir, croproi]
for foldername in targetfolders:
	if not os.path.exists(os.path.join(path, analysis_dir, foldername)):
		os.makedirs(os.path.join(path, analysis_dir, foldername))

# create the path for output images
imgoppath = os.path.join(path, analysis_dir, outputdir)
print('output path')
print(imgoppath)

processed_img = []
for (directory, dir_names, file_names) in os.walk(imgoppath):
	print(file_names)
	for file_name in file_names:
		print(file_name)
		m = re.search(r'(.+?)_c', file_name)
		if m: 
			print(m)
			file_name_temp = m.group(1)
			processed_img.append(file_name_temp)
processed_img = set(processed_img)
print(processed_img)

# create a file list for all images
filelist = []
fileabslist = []
for directory, dir_names, file_names in os.walk(imgpath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			file_name_base = file_name.replace('.nd2', '')
			if (file_name_base not in processed_img):
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name)
				fileabslist.append(filepath_tmp)

print('Completed file path:')
print(filelist)
# print('Completed abs file path:')
# print(fileabslist)
print('The number of the images:')
print(len(filelist))

# load the cropsize

with open(csvpath, 'rb') as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    # Read each row of data after the header
    dict_group = {}
    dict_list = {}
    for row in csvreader:
        dict_list[row[0]] = row[2:]
print('csv header:')
print(csv_header)
print('dict_list:')
print(dict_list)


# load and crop the image

for i in range(len(filelist)): 
#for i in range(1):
	print(filelist[i])
	# check if the target file exist
	
	outputpath = os.path.join(path, analysis_dir, outputdir)		
	imps = BF.openImagePlus(fileabslist[i])
	inputfilebasename = filelist[i].replace(".nd2", "")
	
	for imp in imps:
		imp.show()
		data = dict_list[inputfilebasename]
		x_size = data[2]
		y_size = data[3]
		x = data[0]
		y = data[1]
	
		print(inputfilebasename, x_size, y_size, x, y)
	
		# run macro
		IJ.run(imp, "Specify...", "width=" + x_size + " height=" + y_size + " x=" + x + " y=" + y)
	
		# save c1 image ------------------------------------------
		IJ.run(imp, "Duplicate...", "duplicate channels=1")
		imp_c1 = IJ.getImage()
		fs = FileSaver(imp_c1)
		outputfilename = imp.title.replace('.nd2', '') + '_c1' + '.tif'
		FileSaverCheck(outputpath, outputfilename)
		imp_c1.close()
	
		# save c2 image ------------------------------------------
		
		IJ.run(imp, "Duplicate...", "duplicate channels=2")
		imp_c2 = IJ.getImage()
		fs = FileSaver(imp_c2)
		outputfilename = imp.title.replace('.nd2', '') + '_c2' + '.tif'
		FileSaverCheck(outputpath, outputfilename)
		imp_c2.close()

		break	
	imp.close()	
	del imps
	break
