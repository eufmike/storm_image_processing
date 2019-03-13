library(spatstat)
library(ggplot2)

# define input folders
path <- '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
subfolder = 'tstorm'
inputfolder = 'csvdata_crop'
# create input path
inputpath <- file.path(path, analysis_dir, subfolder, inputfolder)
print(inputpath)

# define output folders
outputfolder = 'spacial_test'
outputdata = 'datalocalL_test'
outputbi = 'binarylocalL'

outputdatapath = file.path(path, analysis_dir, outputfolder, outputdata)
outputbipath = file.path(path, analysis_dir, outputfolder, outputbi)

# channel count
nchannel = 2

# create filelist
filelist <- list.files(inputpath)
print(filelist)
pathlist <- vector()
for (c in nchannel){
        filelist_temp <- list.files(file.path(inputpath, c))
        
        pathlist_temp = file.path(inputpath, c, filelist_temp)
        pathlist <- c(pathlist, pathlist_temp)
        
}
print(pathlist)
print(basename(pathlist))

###!!!!!!!!!!!!!!!!offset required!!!!!!!!!!!!!!!!!!######
# define region of interest
x_frame_size = 30
y_frame_size = 30
dead_pixel = 3
x_start = dead_pixel * 160
x_end = (x_frame_size - dead_pixel) * 160
y_start = dead_pixel * 160
y_end = (y_frame_size - dead_pixel) * 160
rvalue = 50

# process data
for (i in 1:length(pathlist)){
# for(i in c(1)){
        filepath <- pathlist[i]
        filename <- basename(pathlist[i])
        
        data <- read.csv(file = filepath)
        print(nrow(data))
        set.seed(1947)
        sample_row <- sample(1:nrow(data), 7000)
        # print(sample_row)
        print(length(sample_row))
        data <- data[sample_row, ]
        
        # create pattern
        pattern <- ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
        
        # run analysis for localL, 
        L_50 <- localL(pattern, correction = "best", rvalue = rvalue)
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

