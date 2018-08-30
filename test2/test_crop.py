from ij import IJ
imp = IJ.getImage()
print(imp)

x_size = "128"
y_size = "128"
x = "160"
y = "224"

IJ.run(imp, "Specify...", "width=" + x_size + " height=" + y_size + " x=" + x + " y=" + y)
IJ.run(imp, "Duplicate...", "duplicate channels=1")