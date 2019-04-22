# %%
import subprocess
import os

# Functions ---------------------------------------------------------------
def dict2arg_fiji(arg):
    arg_str = str()
    for key, val in arg.items():
        str_tmp = str(key + '="' + val + '", ')
        arg_str = arg_str + str_tmp
    return arg_str

def list2arg_python(arg):
    arg_str = str()
    for var in arg:
        arg_str = arg_str +  "'" + str(var) + "' " 
    return arg_str
# -------------------------------------------------------------------------

# %%
fiji = '/Applications/Fiji.app/Contents/MacOS/ImageJ-macosx'
path = '/Users/michaelshih/Documents/code/wucci/storm_image_processing'
subdir = 'Fiji'

# %%
# imgproc.py
script_name = 'imgproc.py'
arg_dict = {
    'dir_output': 'analysis_20190419',
    'path': '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging',
    'dir_srcimg': 'testdata',
    'batchmodeop': 'false',
}

arg = dict2arg_fiji(arg_dict)
print(arg)

# %%
print("Start running: {}".format(script_name))
subprocess.check_output([fiji, '--ij2', '--run', os.path.join(path, subdir, script_name), arg])
print("End: {}".format(script_name))

# %%
# tstormanalysis.py
script_name = 'tstormanalysis.py'
arg_dict = {
    'dir_output': 'analysis_20190419',
    'path': '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging',
    'dir_srcimg': 'testdata',
    'dir_preproimg': 'preproimg',
    'batchmodeop': 'false', 
}
arg = dict2arg_fiji(arg_dict)
print(arg)

# %%
print("Start running: {}".format(script_name))
subprocess.check_output([fiji, '--ij2', '--run', os.path.join(path, subdir, script_name), arg])
print("End: {}".format(script_name))

# %%
# csv_slicer.py 
script_name = 'csv_slicer.py'
arg_list = ['/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging', 
                'analysis_20190419',
                'tstorm',
                'csvdata', 
                2,
                5000, 
                10001,
                ]
arg = list2arg_python(arg_list)
print(arg)

# %%
print("Start running: {}".format(script_name))
process = subprocess.run(str('python '+ os.path.join(path, script_name)+ ' '+ arg), 
                shell = True, check=True, stdout=subprocess.PIPE)
print("End: {}".format(script_name))


