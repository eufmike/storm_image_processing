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
outputdata = 'data'
outputbi = 'binaryfv_K'

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
rmax = 3000

# process data
for (i in 1:length(filelist)){
# for(i in c(1)){
        filename <- filelist[i]
        filepath <- file.path(inputpath, filename)
        data <- read.csv(file = filepath)
        
        # create pattern
        pattern <- ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
        
        # run analysis
        resultKest <- Kest(pattern, rmax = rmax)
        r <- resultKest$r
        K_r <- resultKest$border
        L_r <- sqrt(K_r/pi)
        H_r <- L_r - r
        outputdata_temp <- data.frame(
                r = r,
                K_r = K_r,
                L_r = L_r,
                H_r = H_r
        )
        outputcsvpath_tmp <- file.path(outputdatapath, filename)
        write.csv(outputdata_temp, file = outputcsvpath_tmp, quote = F)   
        
        outputbipath_tmp <- file.path(outputbipath, filename)
        save(outputbipath, file = gsub('.csv', '.rda', outputbipath_tmp))
        
        
}      
