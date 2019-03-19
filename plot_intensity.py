# %%
# make plot
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl
mpl.style.use('default')

# Functions Section Begins ----------------------------------------------------- #
def dircheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if isinstance(targetpaths, str): 
		print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif isinstance(targetpaths, list): 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)
            
# Functions Section Ends ----------------------------------------------------- #
# %%
# load the csv file
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
ippath = os.path.join(path, 'analysis_20190308', 'preprocessing', 'imgintensity')
oppath = os.path.join(path, 'analysis_20190308', 'preprocessing', 'imginfo', 'plot')

# %%
# merge the csv file
filelist = os.listdir(ippath)
print(filelist)

def testgroup(x):
    if x == 'w':
        return 'wildtype'
    elif x == 'k': 
        return 'knockout'

list_data = []
for filename in filelist:
    df = pd.read_csv(os.path.join(ippath, filename), index_col=None, header=0)
    df['file_name'] = filename
    df['img_name'] = filename.replace('.csv', '')
    test = df['file_name'].str.extract(r'^\d{4}_\d{2}_\d{2}_([a-z])[0-9].csv')
    df['group'] = test[0].apply(lambda x : testgroup(x))
    
    list_data.append(df)

data = pd.concat(list_data, axis = 0, ignore_index=True)

# %%
display(data.head())

print(data.shape)

# %%
imgnamecreator = lambda x: x.replace('.csv', '')
filelist_imgname = list(map(imgnamecreator, filelist))
print(filelist_imgname)

# %% 
data_temp = data.loc[data['img_name'] == filelist_imgname[0]]
display(data_temp)

# %%
labels_group, uni_group = pd.factorize(data['group'])
labels_ch, uni_ch = pd.factorize(data['channel'])
print(uni_group)

# %%
dircheck(oppath)

for group in uni_group:
    data_group = data[data['group'] == group]
    imgname_labels, imgname_uni = pd.factorize(data_group['img_name'])
    print(imgname_uni)
    fig, axes = plt.subplots(ncols = 4, nrows = 5)
    for i, ax in enumerate(axes.flatten()):
        if i < len(imgname_uni):
            data_temp = data_group.loc[data_group['img_name'] == imgname_uni[i]]
            for j in uni_ch:
                df = data_temp[data_temp['channel'] == j]
                ax.plot(df['frame'], df['mean'])
            # ax.set_title('{}'.format(filelist_imgname[i]))
            ax.set_ylim(0, 20000)
    fig.set_figheight(10)
    fig.set_figwidth(10)
    fig.tight_layout()   
    plt.show()
    fig.savefig(os.path.join(oppath, group))

