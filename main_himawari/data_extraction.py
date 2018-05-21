# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:17:04 2015

@author: red
"""
import sys
import numpy as N
import os
from util.main_util import progress_bar

from main_himawari.himawari_functions import open_dat,\
                                             get_dat_meta, get_hrit_data,\
                                             get_radiance, save_H8_hdf5
from main_himawari.himawari_var import *


def single_preprocess_H8(number, totals, seg_no,\
                         segment_interest,\
                         hrit_segment_interest,\
                         llcrnrlon = x_ll,\
                         llcrnrlat = y_ll,\
                         urcrnrlon = x_ur,\
                         urcrnrlat = y_ur,\
                         dat_segment = dat_segment,\
                         hrit_list  = hrit_list ,\
                         dat_listnum = dat_listnum, hrit_listb = hrit_listb,\
                         dat_listnuma = dat_listnuma, dat_listnumb = dat_listnumb,\
                         hrit_spa = hrit_spa, hrit_spb = hrit_spb):
                         
                             
                             
    #print "\nEXTRACTING DATA AT SEGMENT: ["+k+"]\n"
    # read metadata
    group_B_meta, group_B_gamma =\
                            get_dat_meta(segment_interest[number],\
                            dat_listnum = dat_listnum, hrit_listb = hrit_listb,\
                            dat_listnuma = dat_listnuma, dat_listnumb = dat_listnumb )
    
    # get hrit data, lon, lat, and time
    group_B_data, group_B_coors, group_B_time =\
                            get_hrit_data(hrit_segment_interest[number],\
                                          llcrnrlon = llcrnrlon,\
                                          llcrnrlat = llcrnrlat,\
                                          urcrnrlon = urcrnrlon,\
                                          urcrnrlat = urcrnrlat,\
                                          hrit_listb = hrit_listb,\
                                          hrit_list  = hrit_list)
    
    # convert to radiance
    #rad = get_radiance( group_B_data, group_B_meta, group_B_gamma )
    rad = get_radiance(group_B_data, group_B_meta, group_B_gamma,\
                       hrit_listb = hrit_listb, hrit_spa = hrit_spa,\
                       hrit_spb = hrit_spb)
    
    h8_data = group_B_data
    h8_radiance = rad
    h8_coordinates = group_B_coors
    h8_metadata = group_B_meta
    #h8_gamma[k] = group_B_gamma
    progress_bar(number, totals, desc = seg_no)
    print "\n"
    return h8_data, h8_radiance, h8_coordinates, h8_metadata


def whole_preprocess_H8(hrit_fnames,\
                        path_input, path_output,\
                        llcrnrlon = x_ll,\
                        llcrnrlat = y_ll,\
                        urcrnrlon = x_ur,\
                        urcrnrlat = y_ur,\
                        dat_segment = dat_segment,\
                        hrit_list  = hrit_list ,\
                        dat_listnum = dat_listnum, hrit_listb = hrit_listb,\
                        dat_listnuma = dat_listnuma, dat_listnumb = dat_listnumb,\
                        hrit_spa = hrit_spa, hrit_spb = hrit_spb):    
    # directories stated in himawari_var: path and path_input
    
    # open DAT and HRIT file list, changes directory to path_input
    file_dat, reso_dat = open_dat(path_input)
    #file_dat, reso_dat, hrit_fname = open_dat_hrit(path_input)
    # open HRIT file list, changes directory to path_input
    #hrit_fname = open_hrit(path_input)
    
    file_dat = N.array(file_dat)
    hrit_fname = N.array(hrit_fnames)
    
    #for i in xrange(N.shape(hrit_fname)[0]):
    #    print file_dat[i], hrit_fname[i]
    
    # get date 
    dates_times = []
    for i in file_dat:
        dates_times.append(i[7:20])
    dates_times = N.array(dates_times)
    dt_unique = N.unique(dates_times)
    
    if N.shape(dt_unique)[0] > 1:
        print "\nToo many timestamps!"
        print dt_unique
        os.sys.exit("Too many timestamps!")
    
    # Extracting metadata from DAT and data from HRIT
    #for h in dt_unique:
        
    
    print "\nData extraction from H8 HRIT : ",dt_unique[0]
    
    #time_ad = N.where(dates_times == h)# can also be used in HRIT
    time_ad = N.where(dates_times == dt_unique[0])# can also be used in HRIT
    time_interest  = file_dat[time_ad[0]]
    
    hrit_list_interest = hrit_fname[time_ad[0]]# hrit list
    segment_interest = []
    hrit_segment_interest = []
    
    for i in dat_segment:
        segment_list = []
        for j in time_interest:
            segment_list.append(j[-8:-6])
        segment_list = N.array(segment_list)
        segment_ad = N.where(segment_list == i)
        
        segment_interest.append(time_interest[segment_ad[0]])
        hrit_segment_interest.append(hrit_list_interest[segment_ad[0]])
        
    segment_interest = N.array(segment_interest)
    hrit_segment_interest = N.array(hrit_segment_interest)  
    
    
    #print segment_interest
    #print hrit_segment_interest
    
    # dictionaries
    data_output ={}
    h8_data = {}
    h8_radiance = {}
    h8_coordinates = {}
    h8_metadata = {}
    #h8_gamma = {}
    
    dat_segment = N.array(dat_segment, dtype = int)
    dat_segment = N.array(dat_segment, dtype = str)
    
    totals = len(dat_segment)
    # read some needed info per segment
    for number , k in enumerate(dat_segment):
        data_output[number] = single_preprocess_H8(number, totals, k,\
                                                   segment_interest,\
                                                   hrit_segment_interest,\
                                                   llcrnrlon = llcrnrlon,\
                                                   llcrnrlat = llcrnrlat,\
                                                   urcrnrlon = urcrnrlon,\
                                                   urcrnrlat = urcrnrlat,\
                                                   dat_segment = dat_segment,\
                                                   hrit_list  = hrit_list ,\
                                                   dat_listnum = dat_listnum,\
                                                   hrit_listb = hrit_listb,\
                                                   dat_listnuma = dat_listnuma,\
                                                   dat_listnumb = dat_listnumb,\
                                                   hrit_spa = hrit_spa,\
                                                   hrit_spb = hrit_spb)
    for number , k in enumerate(dat_segment):
        h8_data[k] = data_output[number][0]
        h8_radiance[k] = data_output[number][1]
        h8_coordinates[k] = data_output[number][2]
        h8_metadata[k] = data_output[number][3]
        

    #h08_gamma = h8_gamma["3"]
    h08_coords = h8_coordinates["3"]
    #h08_time = h
    h08_time = dt_unique[0]
    
    # delete some data
    del h8_coordinates
    
    #combine segments into one data
    h08_data = {}
    h08_radiance = {}
    
    # 1st method
    for k in hrit_listb:
        seg_hold = {}
        seg_hold_rad = {}
        
        for m in dat_segment:
            seg_hold[m] = N.ma.filled(h8_data[m][k], fill_value = 0.0)
            seg_hold_rad[m] = N.ma.filled(h8_radiance[m][k], fill_value = 0.0)
        
        h08_data[k] = sum(seg_hold.values())
        h08_radiance[k] = sum(seg_hold_rad.values())
        
    # delete some data
    del  h8_data, h8_radiance
    
    # save into hdf5 file
    # path_ouput - > where hdf5 file will save
    title = path_output+'/'+'HS_H08_' +dt_unique[0]+ '_PH_R20_S030405'
    
    save_H8_hdf5(title, h08_data, h08_radiance, h08_time, h08_coords,\
                 hrit_listb = hrit_listb)#,h08_gamma)
                 
    return title+'.hdf5'