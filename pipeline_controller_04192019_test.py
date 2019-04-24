# %%
import subprocess
import os, sys
import winsound

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
codepath = '/Users/michaelshih/Documents/code/wucci/storm_image_processing'
datapath = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
subdir = 'Fiji'
analysis_dir = 'analysis_20190419'

# %%
# imgproc.py
script_name = 'imgproc.py'
arg_dict = {
    'dir_output': analysis_dir,
    'path': datapath,
    'dir_srcimg': 'testdata',
    'batchmodeop': 'false',
}

arg = dict2arg_fiji(arg_dict)
print(arg)

# %%
print("Start running: {}".format(script_name))
subprocess.check_output([fiji, '--ij2', '--run', os.path.join(codepath, subdir, script_name), arg])
print("End: {}".format(script_name))

# %%
# tstormanalysis.py
script_name = 'tstormanalysis.py'
arg_dict = {
    'dir_output': analysis_dir,
    'path': datapath,
    'dir_srcimg': 'testdata',
    'dir_preproimg': 'preproimg',
    'batchmodeop': 'false', 
}
arg = dict2arg_fiji(arg_dict)
print(arg)

# %%
print("Start running: {}".format(script_name))
subprocess.check_output([fiji, '--ij2', '--run', os.path.join(codepath, subdir, script_name), arg])
print("End: {}".format(script_name))

# %%
# csv_slicer.py 
script_name = 'csv_slicer.py'
arg_list = [datapath, analysis_dir,'tstorm','csvdata', 2, 5000, 10001, 'csvdata_sliced']
arg = list2arg_python(arg_list)
print(arg)

print("Start running: {}".format(script_name))
shellcmd = str('python '+ os.path.join(codepath, script_name)+ ' '+ arg)
print(shellcmd)
process = subprocess.run(shellcmd, shell = True, check=True)
print("End: {}".format(script_name))

# %%
# csv_slicer_crop.py
script_name = 'csv_slicer_crop.py'
arg_list = [datapath, analysis_dir,'tstorm','csvdata_sliced', 2, 3, 'csvdata_crop']
arg = list2arg_python(arg_list)
print(arg)

print("Start running: {}".format(script_name))
shellcmd = str('python '+ os.path.join(codepath, script_name)+ ' '+ arg)
print(shellcmd)
process = subprocess.run(shellcmd, shell = True, check=True)
print("End: {}".format(script_name))

# %%
