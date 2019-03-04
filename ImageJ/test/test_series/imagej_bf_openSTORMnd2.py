# For ImageJ/Fiji
import sys
# print(sys.version)
import re
from ij import IJ
import os
import csv
from ij.io import FileSaver

filepath = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/resource/03_testdata/2018-10-26/2018_10_26_k1.nd2'
metadata = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging/analysis_test/metadata'

'''
# parse metadata
from loci.formats import ImageReader
from loci.formats import MetadataTools

reader = ImageReader()
omeMeta = MetadataTools.createOMEXMLMetadata()
reader.setMetadataStore(omeMeta)
reader.setId(filepath)
SizeT = reader.getSizeT()
reader.close()

print(SizeT)
'''


# load bio-format
from loci.plugins import BF
from loci.plugins.in import ImporterOptions

options = ImporterOptions()
# options.setTBegin(0, SizeT)
# options.setTEnd(0, SizeT + 5)
options.setId(filepath)

# open image
imps = BF.openImagePlus(filepath)
for imp in imps:
	imp.show()