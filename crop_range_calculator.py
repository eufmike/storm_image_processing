# %%
import os, sys
import pandas as pd
import numpy as np

path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
analysis_dir = 'analysis_20190122'
filename = 'cropsize.csv'
filepath = os.path.join(path, analysis_dir, filename)

# %%
data = pd.read_csv(filepath)
data = pd.DataFrame(data)
display(data)

# %%
data.dtypes
# %%
xymargin = (3, 3)
ROIframe = (30, 30)

data_gp = data.groupby('name')
data_min = data_gp.min()
data_max = data_gp.max()
xymin = np.array(data_min[['x', 'y']]) - xymargin[0]
xymax = np.array(data_max[['x', 'y']]) + [[ROIframe[0], ROIframe[1]]] + xymargin[1]
print(xymin)
# print(xymax)
xydelta = xymax - xymin
print(xydelta)

# %%
data_name = np.array([list(data_gp.indices.keys())]).T
data_group = np.array([data_min['group']]).T
print(data_name)
print(data_group)

# %%
xyall = np.concatenate((data_name, data_group, xymin, xydelta), axis = 1)
print(xyall)
xyall_df = pd.DataFrame(xyall, columns = ['name', 'group', 'x', 'y', 'dx', 'dy'])
display(xyall_df)

# %%
csv_filename = 'cropsize_compiled.csv'
outputfilename = os.path.join(path, analysis_dir, csv_filename)
xyall_df.to_csv(outputfilename, index = False)