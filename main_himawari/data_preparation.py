# -*- coding: utf-8 -*-
"""
main_process
Read Dat file
then Convert to HRIT
Created on Sun Nov 15 17:32:48 2015
@author: red
"""
import os
import sys
import glob
import numpy as N
import datetime
import subprocess

from himawari_functions import open_dat, downsample_dat, hisd2hrit, open_hrit
from himawari_var import *

from deco import synchronized, concurrent
from util.main_util import progress_bar



def dat_bz2_generator(_dates_, dat_list = dat_list, dat_segment = dat_segment,\
                         dat_list_reso = dat_list_reso):
    datbz_list = []
    # Checks unzip bz2 data
    for m, k in enumerate(dat_list):
        for n in dat_segment:
            datbz_list.append('HS_H08_'+_dates_+'_'+k+'_FLDK_'+dat_list_reso[m]+'_S'+n+'10.DAT.bz2')
    datbz_list = N.array(datbz_list)
    return datbz_list



def open_list_datbz2(directory):
    """
    Reads list of DAT.bz files
    """
    os.chdir(directory)
    #print "\nCurrent directory: " +directory
    print "\nScanning downloaded Himawari-8 DAT.bz files temporarily stored on"
    print directory
    
    _file_ = glob.glob("*.bz2")
    
    _file_list_ = []

    for i, line in enumerate(_file_):
        _file_list_.append(line.split()[0])
        
    return _file_list_
    
    

def check_datbz_files(datbz_fnames, _dates_,\
                      dat_list = dat_list, dat_segment = dat_segment,\
                      dat_list_reso = dat_list_reso):
                          
    # Generates dat bz 2 list
    datbz_list = dat_bz2_generator(_dates_,\
                                    dat_list = dat_list,\
                                    dat_segment = dat_segment,\
                                    dat_list_reso = dat_list_reso)
    
    actual = N.shape(datbz_fnames)[0]
    expected = N.shape(datbz_list)[0]
    
    
    if (actual == expected) == False:
        if actual < expected:
            
            # check missing
            missing = []
            for ctr ,i in enumerate(datbz_fnames):
                if (i in datbz_list) == False:
                    missing.append(i)
            missing = N.array(missing)
            print "Missing bz data:"
            for i in missing:
                print "\t"+i
            # download
            return N.array([str(N.nan)])
            
        elif actual > expected:
            print "\nSomething's wrong with DAT.bz files"
            os.sys.exit("Something's wrong with DAT.bz files")
    else:
        return datbz_list
        
        
@concurrent(processes = 3)
def single_bunzip_h8(datbz_fname, counter, totals):
    #out = os.system("bunzip2 -q "+ datbz_fname)
    proc = subprocess.Popen(["bunzip2 -q "+ datbz_fname],\
                            stdout = subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    progress_bar(counter, totals, desc = datbz_fname )
    #print out
    #return out

@synchronized
def batch_bunzip_h8(datbz_fnames_final):
    #out = {}
    total = len(datbz_fnames_final)
    
    #print datbz_fnames_final
    
    for ctr, i in enumerate(datbz_fnames_final):
        single_bunzip_h8(i, ctr, total)
        
    # checks bunzip
    #for i in out.values():
    #    if i != 0:
    #        print "\nSomething's wrong with unzipping "+i+"\n"
    #        os.sys.exit("Something's wrong with unzipping "+i)
            
                          
    
def preparation_himawari(_date_, datbz_fnames_final, path_input):
    
    print "\n"
    print "HIMAWARI-8 DATA PREPARATION : ", _date_
    
    # Go to temporary directory
    # unzip all
    os.chdir(path_input)
    
    # Bunzip downloaded H8 dat.bz files
    #os.system('for i in ls *.bz2; do bunzip2 $i; echo $i ;done')
    print "\n1.) Unzipping Himawari-8 data"
    start_time = datetime.datetime.now()
    
    batch_bunzip_h8(datbz_fnames_final)
    
    time1 = datetime.datetime.now()
    print('\n\n\tDuration of Data Unzipping: {}\n'.format(time1 - start_time))
    
    # directories stated in himawari_var: path and path_input
    
    file_list, file_reso = open_dat(path_input)
    #os.chdir(path) # current path is in path_input
        
    # path to Downsampling  DAT file
    start_time = datetime.datetime.now()
    
    print "\n2.) Downsampling Himawari-8 data"
    downsample_dat(file_reso,file_list)# downsampling dat file: 0.5km to 1km, 1km to 2km
    file_list, file_reso = open_dat(path_input)# update list
    
    downsample_dat(file_reso,file_list)# downsampling dat file again: 1km to 2km
    file_list, file_reso = open_dat(path_input)# update list
    
    time1 = datetime.datetime.now()
    print('\n\n\tDuration of Downsampling: {}'.format(time1 - start_time))
    
    # converts to HRIT format
    #os.system('ls IMG_DK01* > temp_hrit.log')
    print "\n3.) Converting Himawari-8 DAT to HRIT"
    hisd2hrit(file_list, path_input)
    time2 = datetime.datetime.now()
    
    #Assess Speed
    print('\n\n\tDuration of HRIT Conversion: {}\n'.format(time2 - time1))
    
    hrit_fnames = open_hrit(path_input)
    return hrit_fnames
        
    

