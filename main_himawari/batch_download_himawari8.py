# -*- coding: utf-8 -*-
"""
Created on Fri May 13 12:58:42 2016

@author: red
"""
import numpy as N
import os
import sys

from main_himawari.himawari_functions import create_path_directories, download_h8
from main_himawari.data_preparation import open_list_datbz2, preparation_himawari, check_datbz_files
from main_himawari.data_extraction import whole_preprocess_H8
from main_himawari.himawari_var import *

import datetime

def batch_download_h8(_date_,\
                      path_himawari,\
                      path_himawari_hdf5,\
                      dat_list = dat_list,\
                      llcrnrlon = x_ll,\
                      llcrnrlat = y_ll,\
                      urcrnrlon = x_ur,\
                      urcrnrlat = y_ur,\
                      dat_segment = dat_segment,\
                      dat_list_reso = dat_list_reso,\
                      hrit_list  = hrit_list ,\
                      dat_listnum = dat_listnum,
                      hrit_listb = hrit_listb,\
                      dat_listnuma = dat_listnuma,
                      dat_listnumb = dat_listnumb,\
                      hrit_spa = hrit_spa,\
                      hrit_spb = hrit_spb,
                      create_fd_internal = True):
    """
    This function is used for batch doawnloading of Himawari8 data
    
    Inputs:
    _date_                          list of Date and time stamp of data to download.
                                    Can be hourly, or daily.
    path_himawari                   Directory where to save temporary files.
    path_himawari_hdf5              Directory for Final data product. 
    dat_list = dat_list             * see himawari var, if not stated then default
    dat_segment = dat_segment       * see himawari var, if not stated then default
    dat_list_reso = dat_list_reso   * see himawari var, if not stated then default
    hrit_list  = hrit_list          * see himawari var, if not stated then default
    dat_listnum = dat_listnum       * see himawari var, if not stated then default
    hrit_listb = hrit_listb         * see himawari var, if not stated then default
    dat_listnuma = dat_listnuma     * see himawari var, if not stated then default
    dat_listnumb = dat_listnumb     * see himawari var, if not stated then default
    hrit_spa = hrit_spa             * see himawari var, if not stated then default
    hrit_spb = hrit_spb             * see himawari var, if not stated then default
    """
    
    
    date_obj = [datetime.datetime.strptime(i,"%Y%m%d_%H%M") for i in _date_]
    date_obj1 = N.array([datetime.datetime.strftime(i,"/%Y%m/%d/%H/") for i in date_obj])
    
    final_out_filename_list = []
    path_himawari_hdf5_out_list = []
    for i, j in enumerate(_date_):
        start_time = datetime.datetime.now()
        
        print "\n"
        print "="*80
        
        # if True, creates a subdirectory within default directory to store h8 data
        if create_fd_internal == True:
            path_himawari_hdf5_out = os.path.join(path_himawari_hdf5, j)
        elif create_fd_internal == False:
            path_himawari_hdf5_out = path_himawari_hdf5
        else:
            os.sys.exit("Create folder internal or external options not given by user.")
            
        # if ouput directory does not exist
        if os.path.exists(path_himawari_hdf5_out) == False:
            create_path_directories(path_himawari_hdf5_out)#creates directory for output
        
        file_name_if_dl = "HS_H08_"+ j +"_PH_R20_S030405.hdf5"
        
        #print os.path.join(path_himawari_hdf5_out, file_name_if_dl)
        # if processed himawari data for ceratin date is already downloaded, skip timestamp
        if os.path.exists(os.path.join(path_himawari_hdf5_out, file_name_if_dl)) == True:
            print "\n"
            print file_name_if_dl, 'exists'
            final_out_filename_list.append(file_name_if_dl)
            path_himawari_hdf5_out_list.append(path_himawari_hdf5_out)
            continue
            
        #  downloads the needed data through wget
        dat_bz = download_h8(j, date_obj1[i], path_himawari,\
                            dat_list = dat_list,\
                            dat_segment = dat_segment,\
                            dat_list_reso = dat_list_reso)
                    
        # Checks the downloaded H8 list
        # If datalist is empty, skip timestamp and append on list
        if dat_bz[0] == "nan":
                path_himawari_hdf5_out_list.append(str(N.nan))
                final_out_filename_list.append(str(N.nan))
                
                print "\n"
                print "Skipping "+j
                print "Removing temporary data on "+path_himawari
                os.system("rm "+os.path.join(path_himawari,"*"))
                continue
        
        datbz_fnames = open_list_datbz2(path_himawari)
            
        # double checks data if downloaded
        datbz_fnames_final = check_datbz_files(datbz_fnames, j,\
                                               dat_list = dat_list,\
                                               dat_segment = dat_segment,\
                                               dat_list_reso = dat_list_reso)
        
                           
        if datbz_fnames_final[0] == "nan":
                path_himawari_hdf5_out_list.append(str(N.nan))
                final_out_filename_list.append(str(N.nan))
                
                print "\nSkipping "+j
                print "Removing temporary data on "+path_himawari
                os.system("rm "+os.path.join(path_himawari,"*"))
                continue
        
        # downsample and HRIT conversion
        hrit_fnames = preparation_himawari(j, datbz_fnames_final, path_himawari)
        
        # necessary preprocessing methods
        final_out_filename = whole_preprocess_H8(hrit_fnames,\
                                                 path_himawari,\
                                                 path_himawari_hdf5_out,\
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
        
        os.system("rm "+os.path.join(path_himawari,"*"))# deletes all files in path_himawari        
        print "\nTemporary files are deleted in "+ path_himawari
        
        # summary list
        final_out_filename_list.append(final_out_filename)
        path_himawari_hdf5_out_list.append(path_himawari_hdf5_out)
        
        time1 = datetime.datetime.now()
        print('\n\n\tDuration of whole process: {}'.format(time1 - start_time))

        
    return path_himawari_hdf5_out_list, final_out_filename_list
