library(spatstat)
library(ggplot2)

# define input folders
path <- '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
inputfolder = 'csvdata_sliced'
# create input path
inputpath <- file.path(path, analysis_dir, inputfolder)
print(inputpath)

# define output folders
outputfolder = 'spacial_test'
outputdata = 'datalocalL'
outputbi = 'binarylocalL'

outputdatapath = file.path(path, analysis_dir, outputfolder, outputdata)
outputbipath = file.path(path, analysis_dir, outputfolder, outputbi)

# create filelist
filelist <- list.files(inputpath)
print(filelist)

# define region of interest
dead_pixel = 3
x_start = dead_pixel * 160
x_end = (128 - dead_pixel) * 160
y_start = dead_pixel * 160
y_end = (128 - dead_pixel) * 160
rvalue = 1000

# process data
for (i in 1:length(filelist)){
# for(i in c(1)){
        filename <- filelist[i]
        filepath <- file.path(inputpath, filename)
        data <- read.csv(file = filepath)
        
        data <- data[1:4000, ]
        
        # create pattern
        pattern <- ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
        
        # run analysis for localL, 
        L_50 <- localL(pattern, rvalue = rvalue)
        print('done')
        
        x <- pattern$x
        y <- pattern$y
        z <- L_50
        
        
        outputdata_temp <- data.frame(x, y, z)
        
        outputcsvpath_tmp <- file.path(outputdatapath, filename)
        write.csv(outputdata_temp, file = outputcsvpath_tmp, quote = F, row.names = FALSE)   
        
        # outputbipath_tmp <- file.path(outputbipath, filename)
        # save(outputbipath, file = gsub('.csv', '.rda', outputbipath_tmp))
        
        # pattern <- ppp(data$x, data$y, c(x_start, x_end), c(y_start, y_end))
        # L_50 <- data$z
        
        # X12 <- pattern %mark% L_50
        # Z <- Smooth(X12, sigma=3, dimyx=256)
        # 
        # plot(Z, col=topo.colors(128),  drawlabels = F, nlevels = 20, main="smoothed neighbourhood density")
        # # contour(Z, add=TRUE)
        # points(X12, pch=16, cex=0.5)
        # 
}      

