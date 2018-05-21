# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 03:04:04 2015

@author: red
"""

import os
import numpy as N
import datetime
import sys
sys.path.insert(0, '/media/red/SAMSUNG/main/main_himawari')
from himawari_functions import *
from himawari_var import *

path_himawari ='/media/red/SAMSUNG/himawari/thunderstorm/case1' 

os.chdir(path_himawari)
print os.getcwd()
dates,dates1 = create_datelist_H8('20150910_1200', '20150910_1200')

#def download_h8(date,_path_):

        
def download_h8(_dates_,_dates1_,_path_):     
    for m, k in enumerate(dat_list):
        for n in dat_segment:
            file_dl = 'HS_H08_'+_dates_+'_'+k+'_FLDK_'+dat_list_reso[m]+'_S'+n+'10.DAT.bz2'
            ftp_site = 'ftp://ftp.ptree.jaxa.jp/jma/hsd'
            wget_c ='wget -c --passive-ftp --ftp-user=rednacky_gmail.com --ftp-password=SP+wari8'
            print "Downloading "+ file_dl
            #print wget_c+' '+ftp_site+ _dates1_ +file_dl
            #print dates1[i]
            #quit()
            os.system(wget_c+' '+ftp_site+ _dates1_ +file_dl)
            list_file_dl.append(file_dl)

    list_file_dl = N.array(list_file_dl)
    print "No. of files downloaded :",N.shape(list_file_dl)[0]# must be 48 files

#wget -c --passive-ftp --ftp-user=rednacky_gmail.com --ftp-password=SP+wari8 ftp://ftp.ptree.jaxa.jp/jma/hsd/201510/18/00/HS_H08_20151018_0000_B01_FLDK_R10_S0510.DAT.bz2
