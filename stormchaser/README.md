# STORM Chaser
## STORM Imaging Analysis
This repository stores code generated for storm image analysis. 

Image: `.nd2` files acquired from Nikon d-STORM microscope.

Analytical steps: 
1. Script for Fiji `imgproc.py`: 
    1. create folder `preprocessing`
        * proproimg: split channel and save images individually
        * imgintensity: measure the intensity from a 128*128 central region of image
        * imageinfo
            * imgstat.csv: image information includes following information: 
                1. image_name: name of the image
                2. ip_file_name: input file name (with extension)
                3. xSize: frame size on the x-axis
                4. ySize: frame size on the y-axis
                5. nSlices: z dimension
                6. nFrames: t dimension
                7. nChannels: c dimension
                8. size_MB: size of the file in MB
            * imgmetadata: store image metadata for individual files
    2. create folder `temp` 