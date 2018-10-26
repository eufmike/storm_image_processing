# make plot
# %%
import os, sys
import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import ndimage, misc
from scipy.interpolate import griddata
from tqdm import tqdm
import time

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
spacialtestdir = 'spacial_test'
csvdir = 'datalocalL'
inputfilepath = os.path.join(path, analysis_dir, spacialtestdir, csvdir)

outputfolder_DM = 'plot_densitymap'

filelist = []
fileabslist = []
outputfilelist_DM = []

for directory, dir_names, file_names in os.walk(inputfilepath):
    for file_name in file_names:
        if (not file_name.startswith('.')) & (file_name.endswith('.csv')):
            filepath_tmp =  os.path.join(directory, file_name)
            filelist.append(file_name)
            fileabslist.append(filepath_tmp)
            filenamepng = file_name.replace('.csv', '.png')
            filepath_DM_tmp = os.path.join(path, analysis_dir, spacialtestdir, outputfolder_DM, filenamepng)
            outputfilelist_DM.append(filepath_DM_tmp)

print(filelist)
print(fileabslist)
print(outputfilelist_DM)

# %%
# for i in tqdm(range(len(filelist))):
for i in tqdm(range(1)):
    filepath = fileabslist[i]
    print(filepath)
    data = pd.read_csv(filepath, header=0)
    display(data)

    x = np.array(data['x'])
    y = np.array(data['y'])
    z = np.array(data['z'])

    fig = plt.figure()
    plt.scatter(x, y, marker='.', c=z)
    plt.show()
    '''
    # print(data)
    dataarray = np.array((x, y))
    dataarray = dataarray.T

    start = time.time()
    grid_x, grid_y = np.mgrid[0:20480:2048j, 0:20480:2048j]
    print(grid_x.shape)
    end = time.time()
    print('processing time for mgrid: {}'.format(end - start))

    start = time.time()
    grid_data = griddata(dataarray, z, (grid_x, grid_y), method='cubic', fill_value=0)
    print("finish griddata")
    print(grid_data.shape)
    end = time.time()
    print('processing time for griddata: {}'.format(end - start))

    
    start = time.time()
    grid_data_zoom = scipy.ndimage.zoom(grid_data, 10)
    print("finish zoom")
    print(grid_data_zoom.shape)
    end = time.time()
    print('processing time for scipy.ndimage.zoom: {}'.format(end - start))
    

    levels = np.arange(min(z), max(z), 1)
    
    print(grid_data.T)

    start = time.time()
    fig = plt.figure()
    plt.imshow(grid_data_zoom.T, origin='lower', extent= (0, 20480, 0, 20480))
    plt.plot(data['x'], data['y'], 'k.', ms=1)
    # plt.contourf(grid_data.T, levels = levels, extend = 'both', origin='lower')
    print(outputfilelist_DM[i])
    # plt.show()
    fig.savefig(outputfilelist_DM[i])
    end = time.time()
    print('processing time for plotting: {}'.format(end - start))
    '''
    
    