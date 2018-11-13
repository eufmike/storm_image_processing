library(spatstat)
library(ggplot2)

path <- '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
inputfolder = 'spacial_test'
inputsubfolder = 'datalocalL'

inputpath <- file.path(path, analysis_dir, inputfolder, inputsubfolder)

# create filelist
filelist <- list.files(inputpath)
print(filelist)

dead_pixel = 3
x_start = dead_pixel * 160
x_end = (128 - dead_pixel) * 160
y_start = dead_pixel * 160
y_end = (128 - dead_pixel) * 160
rvalue = 50

# for (i in 1:length(filelist)){
for (i in 1:1){    
        filename <- filelist[i]
        filepath <- file.path(inputpath, filename)
        data <- read.csv(file = filepath)
        
        pattern <- ppp(data$x, data$y, c(x_start, x_end), c(y_start, y_end))
        L_50 <- data$z
        
        X12 <- pattern %mark% L_50
        Z <- Smooth(X12, sigma=5, dimyx=128)
        
        plot(Z, col=topo.colors(128),  drawlabels = F, nlevels = 20, main="smoothed neighbourhood density")
        contour(Z, add=TRUE)
        points(X12, pch=16, cex=0.5)
        
}