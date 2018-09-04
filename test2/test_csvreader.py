import os
import csv
dir = '/Volumes/LaCie_DataStorage/xiaochao_wei_STORM imaging/STORM_imaging'
resource_dir = 'resource'
image_dir = '03_testdata'
analysis_dir = 'analysis'
csvfilename = 'cropsize.csv'
csvpath = os.path.join(dir, analysis_dir, csvfilename)

with open(csvpath, 'rb') as csvfile:
    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')
    # Read the header row first (skip this step if there is now header)
    csv_header = next(csvreader)
    # Read each row of data after the header
    dict_list = {}
    for row in csvreader:
        dict_list[row[0]] = row[1:]        
print(csv_header)
print(dict_list)
print(dict_list)
'''
from jarray import array
javaarray = array(csvfile, )
'''