# Temp -------------------------------------- #
from ij import IJ
from ij import plugin
from ij import gui
from ij import WindowManager as wm
import java.awt.Color as Color
imp_max = IJ.getImage()
imp_basename = imp_max.title.replace(".nd2", "")

#------------------------------------------- #

region_1 = [239, 359, 30, 30]
region_2 = [344, 386, 30, 30]
region_3 = [396, 340, 30, 30]
region_all = [236, 337, 193, 83]

roi_dict = {'1': region_1,
			'2': region_2,
			'3': region_3,
			}

IJ.run("Make Composite")
IJ.run("RGB Color")
imp_RGB = IJ.getImage()

# Create empty overlay
overlay = gui.Overlay()

for i in range(len(roi_dict)):
	# print(i)
	# create key
	key = str(i + 1)
	# 
	crop_roi = gui.Roi(roi_dict[key][0], roi_dict[key][1], roi_dict[key][2], roi_dict[key][3])
	crop_roi.setStrokeColor(Color(153, 204, 255))
	overlay.add(crop_roi)
	# ROI text
	text_roi = gui.TextRoi(roi_dict[key][0] + 3 , roi_dict[key][1] + 3, key)
	text_roi.setStrokeColor(Color(153, 204, 255))
	text_roi.setFont("Arial", 10, 0)
	overlay.add(text_roi)


ROIall = gui.Roi(region_all[0], region_all[1], region_all[2], region_all[3])
ROIall.setStrokeColor(Color(255, 204, 153))
overlay.add(ROIall)

imp_RGB.setOverlay(overlay)
imp_RGB.flatten()