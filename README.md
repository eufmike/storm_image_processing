# STORM Imaging Analysis
Features: Python, R, MATLAB, Numpy, Scipy, ImageJ/Fiji

## Introduction
This project was a collaboration aiming to analyze the nanoclusters of membrane proteins and the interaction between membrane proteins and lipid rafts. The function combined multiple platforms and packages including Python, R (spatstat), MATLAB, and ImageJ/Fiji(Thunderstorm) to employ Ripley's K function, Local-K, density map, and Coordinate-based colocalization. 

![](/figures/storm_image_analysis.png)

## Instruction
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

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.