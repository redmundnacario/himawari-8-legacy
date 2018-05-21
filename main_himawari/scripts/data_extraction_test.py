# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 09:44:41 2016

@author: red
"""
import os
import sys
sys.path.insert(0,'/media/red/SAMSUNG/main/main_himawari')
from himawari_functions import open_dat, downsample_dat, hisd2hrit

path_input = '/media/red/SAMSUNG/himawari/training_data/holder'

file_list, file_reso = open_dat(path_input)



downsample_dat(file_reso,file_list)
downsample_dat(file_reso,file_list)

hisd2hrit(file_list, path_input)