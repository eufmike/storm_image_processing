# %%
import os, sys
from PIL import Image

# create input folder
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_012019'
image_dir = 'crop_img'
inputfilepath = os.path.join(path, analysis_dir,image_dir)

# %%
inputfilelist = []
inputfileabslist = []
for directory, dir_names, file_names in os.walk(inputfilepath):
	for file_name in file_names:
		if (not file_name.startswith('.')) & (file_name.endswith('.tif')):
			filepath_tmp =  os.path.join(directory, file_name)
			inputfilelist.append(file_name)
			inputfileabslist.append(filepath_tmp)
print(inputfilelist)
print(inputfileabslist)
print(len(inputfilelist))

# %%
for i in range(len(inputfilelist)):
    print(inputfileabslist[i])
    # pil_im = Image.open(inputfileabslist[i])
    break
    