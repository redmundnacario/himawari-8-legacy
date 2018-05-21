# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 16:51:11 2016

@author: red
"""

import numpy as N
import pyproj
import os
import sys
sys.path.insert(0,"/media/red/SAMSUNG/main/main_himawari")# to be edited
from himawari_functions import rename_hcfg, create_path_directories, download_h8, read_h8_hdf5
from himawari_plot_function import plot_img

import datetime
path_himawari_hdf5 = '/media/red/SAMSUNG/pears_himawari/himawari8_files'
hrit_listb = N.array(["VIS", "B05", "IR1"])

# 2016-02-13T06:03:06Z
_date_ = N.array(["20160213_1010"])
path_himawari_hdf5_out = os.path.join(path_himawari_hdf5, _date_[0])
file_name_if_dl = "HS_H08_"+ _date_[0] +"_PH_R20_S030405.hdf5"
print os.path.join(path_himawari_hdf5_out, file_name_if_dl)

h08_data, h08_radiance, longitude, latitude, date_time = read_h8_hdf5(os.path.join(path_himawari_hdf5_out,\
                                                                file_name_if_dl), hrit_listb = hrit_listb)
del h08_radiance
print h08_data.keys()

#Distribute data
band_03 = h08_data["VIS"]
band_05 = h08_data["B05"]
band_13 = h08_data["IR1"]

print band_03.min(), band_03.max()

plot_img(band_03, longitude, latitude, "Reflectance", "Red Band" , "gray",\
            vmin = band_03.min(), vmax= band_03.max() )

