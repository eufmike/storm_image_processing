#@UIService uiService
#@LogService log

print("Script Starts")
print('Importing modules ...')

# Import ImageJ/Fiji package
import sys 
import os
import re
import csv
from ij import IJ
from ij import plugin
from ij import gui
from ij.io import FileSaver
from ij import WindowManager as wm
from ij.process import ImageStatistics as IS 
import java.awt.Color as Color
import java.lang as jl

# load bio-format
from loci.plugins import BF
from loci.plugins.in import ImporterOptions


path = "/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/resource/03_testdata/2018-10-26/2018_10_26_k2.nd2"
# imps = BF.openImagePlus(path)
# print(locals())


log.info('Current Image File: {}'.format("test.tif"))
import gc
gc.collect()

'''
a = 42
print(sys.getsizeof(a))

a = 2**1000
print(sys.getsizeof(a))
print(sys.getsizeof(imps))


for i in locals(): 
	print(i)
	x = sys.getsizeof(i)
	print(x)
