# -*- coding: utf-8 -*-
"""
Downloads himawari data specified on the list 
created based from time of radar data w/ sweep level 2.

Created on Sun Dec 13 19:06:48 2015
@author: red
"""

import os
import numpy as N
import datetime
import sys

from main_himawari.himawari_functions import download_h8, rename_hcfg
from main_himawari.himawari_var import *
from main_himawari.data_extraction import whole_preprocess_H8
from main_himawari.data_preparation import preparation_himawari, open_list_datbz2, check_datbz_files

import time

# directory
path = "/media/red/SAMSUNG/main"
path_himawari='/media/red/SAMSUNG/himawari/ty_lando/case2'
path_himawari_hdf5 = '/media/red/SAMSUNG/himawari/ty_lando/case2_hdf5'

# read list of himawari data to download
#dates, dates1 = N.loadtxt(path+'/himawari_to_dl.txt', dtype="S20", delimiter="\t")
#_dates_ : w/ format '%Y%m%d_%H%M'
#_dates1_ : w/ format '/%Y%m/%d/%H/'

# sample
dates = ["20150708_0000"]
dates1  = ["/201507/08/00/"]


path_out = "/media/red/SAMSUNG/himawari/sample_data/sample_ty_lando/20150708_0000"
path_himawari_hdf5_out = "/media/red/SAMSUNG/himawari/sample_data/sample_ty_lando"

# prerequisites
rename_hcfg(path_out, path_cfg = path_cfg)

for i, j in enumerate(dates):
#    file_dl = download_h8(j, dates1[i],\
#                    path_out, dat_list = dat_list, dat_segment = dat_segment,\
#                    dat_list_reso = dat_list_reso) # downloads the needed data through wget
    datbz_fnames = open_list_datbz2(path_out)
        
    # double checks data if downloaded
    datbz_fnames_final = check_datbz_files(datbz_fnames, j,\
                                           dat_list = dat_list,\
                                           dat_segment = dat_segment,\
                                           dat_list_reso = dat_list_reso)
                    
    hrit_fnames = preparation_himawari(j, datbz_fnames_final, path_out)
    
    print "\n"
    print len(hrit_fnames)
    print "\n"
    
    final_out_filename = whole_preprocess_H8(hrit_fnames,\
                                             path_out,\
                                             path_himawari_hdf5_out,\
                                             llcrnrlon = x_ll,\
                                             llcrnrlat = y_ll,\
                                             urcrnrlon = x_ur,\
                                             urcrnrlat = y_ur,\
                                             dat_segment = dat_segment,\
                                             hrit_list  = hrit_list ,\
                                             dat_listnum = dat_listnum,\
                                             hrit_listb = hrit_listb,\
                                             dat_listnuma = dat_listnuma,\
                                             dat_listnumb = dat_listnumb,\
                                             hrit_spa = hrit_spa,\
                                             hrit_spb = hrit_spb)

#print hrit_fnames
#print len(hrit_fnames)





    
