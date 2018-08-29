import sys
# print(sys.version)

from ij import IJ
import os


dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
image_dir = '03_testdata'
analysis_dir = 'analysis'

path = os.path.join(dir, resource_dir, image_dir)
#imgfolderlist = os.listdir(path)
#print(imgfolderlist)

filelist = []
for directory, dir_names, file_names in os.walk(path):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.nd2')):
			filepath_tmp =  os.path.join(directory, file_name)
			filelist.append(filepath_tmp)
print(filelist)



from loci.plugins import BF
from loci.plugins.in import ImporterOptions

#for i in range(len(filelist)): 
for i in range(2):
	options = ImporterOptions()
	options.setColorMode(ImporterOptions.COLOR_MODE_DEFAULT)
	options.setId(filelist[i]) 
	imps = BF.openImagePlus(filelist[i])
	for imp in imps:
    	imp.show()
	
	#imp = IJ.openImage(filelist[i])
	print(i)




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
