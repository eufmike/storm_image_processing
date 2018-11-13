from ij import IJ, ImagePlus, 'plugin.frame'
import inspect
import pprint as pp

imp = IJ.getImage()

a = inspect.getmembers(imp)
print(a)


## test
from ij import WindowManager as wm
wm.closeAllWindows("Others")

import inspect
from ij import IJ, ImagePlus
from ij import WindowManager as wm
IJ.selectWindow('ThunderSTORM: results')
a = wm.getCurrentWindow()

b = inspect.getmembers(a)
print(b)


'''
a = wm.getWindow('ThunderSTORM: results')
a.close()
'''


