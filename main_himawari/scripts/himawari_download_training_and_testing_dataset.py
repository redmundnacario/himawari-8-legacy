# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 02:27:50 2016

@author: red
Downloads training and testing data for Himawari
757 files to download
20150708 to 20151231

"""

import os
import numpy as N
import datetime
import sys
sys.path.insert(0, '/media/red/SAMSUNG/main/main_himawari')
from himawari_functions import *
from himawari_var import *
from data_extraction import *
from data_preparation import *

path = "/media/red/SAMSUNG/main"
path_home = '/media/red/SAMSUNG/himawari/training_data'
path_himawari='/media/red/SAMSUNG/himawari/training_data/holder'
path_himawari_hdf5 = '/media/red/SAMSUNG/himawari/training_data'

# create path directories
#create_path_directories(path_home) 
#create_path_directories(path_himawari)
#create_path_directories(path_himawari_hdf5)


os.chdir(path_home)
date_list = N.loadtxt('himawari_rest.txt', dtype="S20", delimiter="\t")
#date_list =date_list[:,0]#already one dimension


behind_time = []
for i in date_list:
    year_1 = i[0:4]
    month_1 = i[4:6]
    day_1 = i[6:8]
    hh_1 = i[9:11]
    mm_1 = i[11:13]
    time1a = datetime.datetime(int(year_1),int(month_1),int(day_1),\
    int(hh_1), int(mm_1))
    result_time = time1a + datetime.timedelta(hours=-1)
    behind_time.append(result_time.strftime('%Y%m%d_%H%M'))
behind_time = N.array(behind_time)

full_list_date = []
full_list_date1 = []
for ctr, i in enumerate(date_list):
    date_holder = create_datelist_H8(behind_time[ctr], i, time_interval=600)
    full_list_date.append(date_holder[0][1:])
    full_list_date1.append(date_holder[1][1:])

full_list_date = N.array(full_list_date)
full_list_date1 = N.array(full_list_date1)
full_list_date = N.reshape(full_list_date, (N.shape(date_list)[0],6))
full_list_date1 = N.reshape(full_list_date1, (N.shape(date_list)[0],6))

#os.chdir(path_himawari)
path_cfg1 = "/media/red/SAMSUNG/pears_himawari/config_files/pytroll_config/himawari"
rename_hcfg(path_himawari, path_cfg = path_cfg1)

for i, j in enumerate(date_list):
    path_himawari_hdf5_out = path_himawari_hdf5+"/"+j
    create_path_directories(path_himawari_hdf5_out)#creates directory for output    
    for k in xrange(6):
        if os.path.exists(path_himawari_hdf5_out+'/'+'HS_H08_'+full_list_date[i,k]+'_PH_R20_S030405.hdf5') == True:
            print 'HS_H08_'+full_list_date[i,k]+'_PH_R20_S030405.hdf5 exists'
            continue
        
        download_h8(full_list_date[i,k], full_list_date1[i,k], path_himawari) # downloads the needed data through wget
        
        preparation_himawari(path_himawari)# prepares the data   
        
        whole_preprocess_H8(path_himawari, path_himawari_hdf5_out) # necessary preprocessing methods
        
        os.system("rm "+ path_himawari +"/*")# deletes all files in path_himawari        
        print "all raw files for "+ j +" in " + path_himawari +" have been removed"


os.chdir(path_himawari_hdf5)
os.system("ls -d */ > file_list.log")
#must be 757

