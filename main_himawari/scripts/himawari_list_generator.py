# -*- coding: utf-8 -*-
"""
# list generator
> creates list of hdf5 files to be downloaded
  based from the time of radar hdf5 files
Created on Sun Dec 13 14:14:20 2015
@author: red
"""
import os
import numpy as N
import datetime
import sys
sys.path.insert(0, '/media/red/SAMSUNG/main/main_himawari')
from himawari_functions import *
from himawari_var import *

path = "/media/red/SAMSUNG/main"
#path_himawari ='/media/red/SAMSUNG/himawari/thunderstorm/case1'
#path_radar = '/media/red/SAMSUNG/radar/tagaytay/thunderstorm/hdf5_case1'
path_himawari ='/media/red/SAMSUNG/himawari/ty_lando/case2'
path_radar = '/media/red/SAMSUNG/radar/tagaytay/ty_lando/hdf5_case2'

os.chdir(path_himawari)
print os.getcwd()
# for 10min interval, 60 sec  x  10 min  = 600 sec
dates,dates1 = create_datelist_H8('20151018_0000', '20151019_0000',time_interval= 600)
dates1 = [] 
for i in dates:
    # convert time into datetime.datetime format
    dates1.append(change_datetime_format(i,sec_include =False))
dates1 = N.array(dates1)

# opening radar hdf5 list w/o changing directory
radar_file_list = open_hdf(path_radar)
radar_time_list = []
# get time labels from title
for i in radar_file_list:
    # convert time into datetime.datetime format
    radar_time_list.append(change_datetime_format(i[4:19],sec_include =True))
radar_time_list = N.array(radar_time_list)

# get time from himawari close to time from radar
time_before, time_after = radar_himawari_time( radar_time_list, dates1 )

# concatenate lists, get unique values of time
time_H8_all = time_before + time_after
time_H8_all = N.array(time_H8_all)
time_H8_all = N.unique(time_H8_all)

time_H8_all1 = []
time_H8_all2 = []
for i in time_H8_all:
    time_H8_all1.append(i.strftime('%Y%m%d_%H%M'))
    time_H8_all2.append(i.strftime('/%Y%m/%d/%H/'))
N.savetxt(path+'/himawari_to_dl.txt',(time_H8_all1, time_H8_all2), fmt ="%s", delimiter="\t")


    
          
            
    


    