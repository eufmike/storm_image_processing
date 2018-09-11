library(spatstat)

path <- '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis'
inputfilder = 'csvdata_sliced'

inputpath <- file.path(path, analysis_dir, inputfilder)
print(inputpath)

filelist <- list.files(inputpath, full.names = T)
print(filelist)

dead_pixel = 3
x_start = dead_pixel * 160
x_end = (128 - dead_pixel) * 160
y_start = dead_pixel * 160
y_end = (128 - dead_pixel) * 160
rmax = 1000

# for (i in filelist){
for(i in c(1)){
        filepath <- filelist[i]
        data <- read.csv(file = filepath)
        pattern <- ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
        resultKest <- Kest(pattern, rmax = rmax)
        r <- resultKest$r
        K <- resultKest$border
        
        resultLest <- Lest(pattern, rmax = rmax)
        r <- resultLest$r
        L <- resultLest$border
        
        H <- L - r
        
        
}      

summary(pattern)
plot(r, K)
plot(r, L)
plot(r, H)