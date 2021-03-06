library(spatstat)
library(ggplot2)
library(dplyr)

# parameters
nchannel = 2
region = 3

# define input folders
# path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
# analysis_dir = 'analysis_20190308'
# sub_dir = 'tstorm'
# inp_dir = 'csvdata_crop'

args <- commandArgs(TRUE)
print(args)
# define input folders
path = as.character(args[1])
analysis_dir = as.character(args[2])
sub_dir = as.character(args[3])
inp_dir = as.character(args[4])
# parameters
nchannel = as.integer(args[5])
region = as.integer(args[6])

# create input path
ippath <- file.path(path, analysis_dir, sub_dir, inp_dir)
print(ippath)

# define output folders
op_dir = as.character(args[7])
opkest_dir = as.character(args[8])

# define output folders
# op_dir = 'spacial_test'
# opkest_dir = 'spacialdata_local'
# opbi_dir = 'spacialdata_local_bi'

opkest_path = file.path(path, analysis_dir, op_dir, opkest_dir)
# opbi_path = file.path(path, analysis_dir, op_dir, opbi_dir)

# create filelist

for (c in 1:nchannel){
        print(c)
        if (!file.exists(file.path(opkest_path, c))){
                dir.create(file.path(opkest_path, c), recursive =T)
        }
        # if (!file.exists(file.path(opbi_path, c))){
        #         dir.create(file.path(opbi_path, c), recursive =T)
        # }
        
}

# import cropsize.csv
par_dir = 'par'
crop_filename = 'cropsize.csv'
croppath = file.path(path, analysis_dir, par_dir, crop_filename)
data = read.csv2(croppath, sep = ",")
data = tbl_df(data)
print(data)

data_mod = mutate(data, filename = paste(name, '_r',img, '.csv', sep = ''))
print(data_mod)

# create filelist
filelist <- list.files(ippath)
print(filelist)
ippathlist <- vector()
oppathkest_list <- vector()
# oppathbi_list <- vector()
for (c in 1:nchannel){
        filelist_temp = list.files(file.path(ippath, c))
        ippathlist_temp = file.path(ippath, c, filelist_temp)
        ippathlist = c(ippathlist, ippathlist_temp)
        oppathkest_temp = file.path(opkest_path, c, filelist_temp)
        oppathkest_list = c(oppathkest_list, oppathkest_temp)
        # oppathbi_temp = file.path(opbi_path, c, gsub('.csv', '.rda', filelist_temp))
        # oppathbi_list = c(oppathbi_list, oppathbi_temp)
}

print(ippathlist)
print(oppathkest_list)
# print(oppathbi_list)

# process data
for (i in 1:length(ippathlist)){
        # for(i in c(1)){
        filepath = ippathlist[i]
        filename = basename(ippathlist[i])
        print(filepath)
        print(filename)
        
        # define region of interest
        region = data_mod[data_mod$filename == filename, ]
        region = data.frame(region)
        print(region)
        
        dead_pixel = 0
        x_start = (dead_pixel + region[1, 'x']) * 160
        x_end = region[1, 'dx'] * 160 + x_start
        y_start = (dead_pixel + region[1, 'y']) * 160
        y_end = region[1, 'dy'] * 160 + y_start
        rmax = 3000
        rvalue = 50
        
        print(x_start)
        print(x_end)
        print(y_start)
        print(y_end)
        
        data = read.csv(file = filepath)
        
        max_sample_size = 7000
        
        # data sampling
        print(nrow(data))
        set.seed(1947)
        if (nrow(data) > max_sample_size){
                sample_row <- sample(1:nrow(data), max_sample_size)
                print(length(sample_row))
                data = data[sample_row, ]
        }
        
        # print(sample_row)
        

        # create pattern
        pattern = ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
        
        # run analysis for localL,
        L_50 <- localL(pattern, correction = "best", rvalue = rvalue)
        print('done')
        
        x <- pattern$x
        y <- pattern$y
        z <- L_50
        
        outputdata_temp <- data.frame(x, y, z)
        
        # outputcsvpath_tmp <- file.path(outputdatapath, filename)
        # write.csv(outputdata_temp, file = outputcsvpath_tmp, quote = F, row.names = FALSE)
        write.csv(outputdata_temp, file = oppathkest_list[i], quote = F, row.names = FALSE)
        # save(outputdata_temp, file = oppathbi_list[i])

        
}      


# ==============================================================================

# 
# filelist <- list.files(inputpath)
# print(filelist)
# pathlist <- vector()
# for (c in nchannel){
#         filelist_temp <- list.files(file.path(inputpath, c))
# 
#         pathlist_temp = file.path(inputpath, c, filelist_temp)
#         pathlist <- c(pathlist, pathlist_temp)
# 
# }
# print(pathlist)
# print(basename(pathlist))
# 
# ###!!!!!!!!!!!!!!!!offset required!!!!!!!!!!!!!!!!!!######
# # define region of interest
# x_frame_size = 30
# y_frame_size = 30
# dead_pixel = 3
# x_start = dead_pixel * 160
# x_end = (x_frame_size - dead_pixel) * 160
# y_start = dead_pixel * 160
# y_end = (y_frame_size - dead_pixel) * 160
# rvalue = 50
# 
# # process data
# for (i in 1:length(pathlist)){
# # for(i in c(1)){
#         filepath <- pathlist[i]
#         filename <- basename(pathlist[i])
# 
#         data <- read.csv(file = filepath)
#         print(nrow(data))
#         set.seed(1947)
#         sample_row <- sample(1:nrow(data), 7000)
#         # print(sample_row)
#         print(length(sample_row))
#         data <- data[sample_row, ]
# 
#         # create pattern
#         pattern <- ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))
# 
#         # run analysis for localL,
#         L_50 <- localL(pattern, correction = "best", rvalue = rvalue)
#         print('done')
# 
#         x <- pattern$x
#         y <- pattern$y
#         z <- L_50
# 
#         outputdata_temp <- data.frame(x, y, z)
# 
#         outputcsvpath_tmp <- file.path(outputdatapath, filename)
#         write.csv(outputdata_temp, file = outputcsvpath_tmp, quote = F, row.names = FALSE)
# 
#         # outputbipath_tmp <- file.path(outputbipath, filename)
#         # save(outputbipath, file = gsub('.csv', '.rda', outputbipath_tmp))
# 
#         # pattern <- ppp(data$x, data$y, c(x_start, x_end), c(y_start, y_end))
#         # L_50 <- data$z
# 
#         # X12 <- pattern %mark% L_50
#         # Z <- Smooth(X12, sigma=3, dimyx=256)
#         #
#         # plot(Z, col=topo.colors(128),  drawlabels = F, nlevels = 20, main="smoothed neighbourhood density")
#         # # contour(Z, add=TRUE)
#         # points(X12, pch=16, cex=0.5)
#         #
# }

