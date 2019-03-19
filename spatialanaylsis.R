library(spatstat)
library(ggplot2)
library(dplyr)

# parameters
nchannel = 2
region = 3

# define input folders
path = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
analysis_dir = 'analysis_20190308'
sub_dir = 'tstorm'
inp_dir = 'csvdata_crop'
# create input path
ippath <- file.path(path, analysis_dir, sub_dir, inp_dir)
print(ippath)

# define output folders
op_dir = 'spacial_test'
opkest_dir = 'spacialdata'
opbi_dir = 'spacialdata_bi'

opkest_path = file.path(path, analysis_dir, op_dir, opkest_dir)
opbi_path = file.path(path, analysis_dir, op_dir, opbi_dir)

for (c in 1:nchannel){
        print(c)
        if (!file.exists(file.path(opkest_path, c))){
                dir.create(file.path(opkest_path, c), recursive =T)
        }
        if (!file.exists(file.path(opbi_path, c))){
                dir.create(file.path(opbi_path, c), recursive =T)
        }
        
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


#data_crop = data[data$name == '2018_06_18_w1',]
#print(data_crop)



# create filelist
filelist <- list.files(inputpath)
print(filelist)
ippathlist <- vector()
oppathkest_list <- vector()
oppathbi_list <- vector()
for (c in 1:nchannel){
        filelist_temp = list.files(file.path(ippath, c))
        ippathlist_temp = file.path(ippath, c, filelist_temp)
        ippathlist = c(ippathlist, ippathlist_temp)
        oppathkest_temp = file.path(opkest_path, c, filelist_temp)
        oppathkest_list = c(oppathkest_list, oppathkest_temp)
        oppathbi_temp = file.path(opbi_path, c, gsub('.csv', '.rda', filelist_temp))
        oppathbi_list = c(oppathbi_list, oppathbi_temp)
}

print(ippathlist)
print(oppathkest_list)
print(oppathbi_list)


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
        
        print(x_start)
        print(x_end)
        print(y_start)
        print(y_end)
        
        data = read.csv(file = filepath)

        # create pattern
        pattern = ppp(data$x..nm., data$y..nm., c(x_start, x_end), c(y_start, y_end))

        # run analysis
        resultKest = Kest(pattern, rmax = rmax)
        r = resultKest$r
        K_r = resultKest$border
        L_r = sqrt(K_r/pi)
        H_r = L_r - r
        outputdata_temp = data.frame(
                r = r,
                K_r = K_r,
                L_r = L_r,
                H_r = H_r
        )
        write.csv(outputdata_temp, file = oppathkest_list[i], quote = F)
        save(outputdata_temp, file = oppathbi_list[i])
                 
}      

