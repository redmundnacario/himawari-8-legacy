# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 13:26:58 2015

@author: red
"""
# import all functions
import os
import numpy as N
import ahisf_reader
import datetime
from himawari_var import *
import h5py
import glob
import subprocess

# pyrpoj
import pyproj
from mpop.satellites import GeostationaryFactory
from mpop.projector import get_area_def
#from mpop.utils import debug_on
#debug_on()

from deco import synchronized, concurrent
from util.main_util import progress_bar, check_internet



def create_path_directories(dire):
    if os.path.exists(dire) == False:
        os.system("mkdir "+dire)
    else:
        print dire+ " exists"

def rename_hcfg(path_input, path_cfg = path_cfg):
    """
    Renames the directory where the temporaty data will be saved
    """
    os.chdir(path_cfg)
    _file_= open('Himawari-8.cfg','r')
    file_content = []
    for i, line in enumerate(_file_):
        file_content.append(line)
    _file_.close()
    file_content = N.array(file_content)
    print file_content[29]+ " replaced by:  "
    file_content[29] = "dir = '"+path_input+"'"+"\n"
    print file_content[29]
    
    # rewrite
    _file_ = open(os.path.join(path_cfg,'Himawari-8.cfg'), "w")
    for i in file_content:
        _file_.write(i)
    _file_.close()
    
def open_dat(directory):
    """
    Reads list of DAT and HRIT files
    """
    os.chdir(directory)
    #print "Current directory: " +directory
    print "\nScanning Himawari 8 DAT files"
    
    _file_ = glob.glob("*.DAT")
    
    _file_list_ = []
    _file_reso_ = []
    for i, line in enumerate(_file_):
        _file_list_.append(line.split()[0])
        _file_reso_.append(line.split()[0][31:33])
    
    _file_list_ = N.array(_file_list_, dtype = str)
    _file_reso_ = N.array(_file_reso_, dtype = str)
    return _file_list_, _file_reso_
    
def open_dat_hrit(directory):
    """
    Reads list of DAT and HRIT files
    """
    os.chdir(directory)
    print "\nCurrent directory: " +directory
    print "Scanning Himawari-8 DAT files\n"
    
    _file_ = glob.glob("*.DAT")
    
    _file_list_ = []
    _file_reso_ = []
    for i, line in enumerate(_file_):
        _file_list_.append(line.split()[0])
        _file_reso_.append(line.split()[0][31:33])
        
    print "Current directory: " +directory
    print "Scanning Himawari 8 HRIT files"
    
    _file_ = glob.glob("IMG*")
    
    hrit_file = []
    for i, line in enumerate(_file_):
        hrit_file.append(line.split()[0])
    
    return _file_list_, _file_reso_, hrit_file



def single_downsample_dat(file_reso, file_list, counter, totals):
    if file_reso == '10':
        #print 'Downsampling '+ file_list[counter]+' into 2 km'
        #print "\n"
        #os.system('downsample '+ file_list[counter])
    
        proc = subprocess.Popen(['downsample '+ file_list[counter]],\
                            stdout = subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        #print "program output:", out
        progress_bar(counter, totals, desc = file_list[counter]+' into 2 km',\
                     def_total = 10)
        os.system('rm '+ file_list[counter])
        
    elif file_reso == '05':
        #print 'Downsampling '+ file_list[counter]+' into 1 km'
        #print "\n"
        #os.system('downsample '+ file_list[counter])
    
        proc = subprocess.Popen(['downsample '+ file_list[counter]],\
                            stdout = subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        #print "program output:", out                             
        progress_bar(counter, totals, desc = file_list[counter]+' into 1 km',\
                     def_total = 10)
        os.system('rm '+ file_list[counter])

    else:
        print "\nH8 DAT file beyond 2  km resolution : " + file_list[counter] 
        quit()

def downsample_dat(file_reso, file_list):
    #print "Downsampling"
    file_reso = N.array(file_reso, dtype =str)
    file_list = N.array(file_list, dtype =str)
    
    index = N.where(file_reso != '20')[0]
    nfile_reso = file_reso[index]
    nfile_list = file_list[index]
    
    print 'H8 DAT files already in 2 km resolution :'+ str(len(file_list) - len(index))
    
    totals = len(index)
    
    for ctr,i in enumerate(nfile_reso):
        single_downsample_dat(i, nfile_list, ctr, totals)
        
        


def single_hisd2hrit(file_h8, counter, totals):
    #os.system('hisd2hrit '+ file_h8)
    proc = subprocess.Popen(['hisd2hrit '+ file_h8],\
                            stdout = subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    #print "program output:", out
    
    progress_bar(counter, totals, desc = file_h8)
    

def hisd2hrit(file_list, directory):
    totals = len(file_list)
    
    for ctr, i in enumerate(file_list):
        single_hisd2hrit(i, ctr, totals)

def open_hrit(directory):
    os.chdir(directory)
    #print "Current directory: " +directory
    print "\nScanning Himawari 8 HRIT files"
    
    _file_ = glob.glob("IMG_DK*")
    
    hrit_file = []
    for i, line in enumerate(_file_):
        hrit_file.append(line.split()[0])
    
    hrit_file = N.array(hrit_file, dtype = str)
    return hrit_file
    
    

def get_dat_meta(batch_data,dat_listnum = dat_listnum, hrit_listb = hrit_listb,\
                 dat_listnuma = dat_listnuma, dat_listnumb = dat_listnumb ):
    # read metadata in DAT file
    sample_data = ahisf_reader.ahisf(batch_data)
    for k in batch_data:
        sample_data.read_band(k)
    
    grp_B_meta = {}
    grp_B_gamma = {}
    for ctr, k in enumerate(dat_listnum):
        #print dat_listnum
        #print ctr, k
        grp_B_gamma[hrit_listb[ctr]] = sample_data._header[k]["block5"]["central_wave_length"][0]
        if k in dat_listnuma:
            calibration = {}
            calibration['coeff_rad2albedo_conversion']= sample_data._header[k]["calibration"]['coeff_rad2albedo_conversion'][0]
            grp_B_meta[hrit_listb[ctr]] = calibration
        elif k in dat_listnumb:
            calibration = {}
            for coeff in constant_b:
                calibration[coeff] = sample_data._header[k]["calibration"][coeff][0]
            grp_B_meta[hrit_listb[ctr]] = calibration
    # close read metadata
    del sample_data
    return grp_B_meta, grp_B_gamma

def get_hrit_data(batch_data,\
                  llcrnrlon = x_ll, llcrnrlat = y_ll,\
                  urcrnrlon = x_ur, urcrnrlat = y_ur,\
                  hrit_listb = hrit_listb , hrit_list  = hrit_list):
    # reproject lat lon points                
    llcrnrlon, llcrnrlat = HS_proj(llcrnrlon, llcrnrlat)
    urcrnrlon, urcrnrlat = HS_proj(urcrnrlon, urcrnrlat)                  
                      
    # get time hrit (common time)
    time_ = batch_data[0][12:24]
    
    grp_B_time = {}
    grp_B_time['time'] = time_
    
    year_ = batch_data[0][12:16]
    month_ = batch_data[0][16:18]
    day_ = batch_data[0][18:20]
    hh_ = batch_data[0][20:22]
    mm_ = batch_data[0][22:24]
    
    t = (datetime.datetime(int(year_), int(month_), int(day_), int(hh_), int(mm_)))
    global_data = GeostationaryFactory.create_scene("Himawari-", "8","ahi", t)
    global_data.load(hrit_listb, area_extent=(llcrnrlon, llcrnrlat,\
                                              urcrnrlon, urcrnrlat))
    #print global_data
    
    # get longitude, latitude
    lon_geos, lat_geos = global_data[hrit_list[0]].area.get_lonlats()
    
    grp_B_coors = {}
    grp_B_coors["Longitude"] = lon_geos
    grp_B_coors["Latitude"] = lat_geos
    
    # get data from bands 1 to 16
    grp_B_data = {}
    for k in hrit_listb:
        #print "Extracting  reflectance/BT data from Band "+k
        grp_B_data[k] = global_data[k].data
    # close read data
    del global_data
    return grp_B_data, grp_B_coors, grp_B_time


def get_radiance(data, meta, gamma, hrit_listb = hrit_listb, hrit_spa = hrit_spa,\
                 hrit_spb = hrit_spb):
    radiance = {}
    for k in hrit_listb:
        #print "Extracting radiance data from Band " +k
        if k in hrit_spa:
            radiance[k] = (data[k]) / (meta[k]['coeff_rad2albedo_conversion'])
            #print radiance[k].max(), radiance[k].min()
        elif k in hrit_spb:
            var1 = meta[k]['c0_tb2rad_conversion']
            var2 = meta[k]['c1_tb2rad_conversion'] * data[k]
            var3 = meta[k]['c2_tb2rad_conversion'] * (data[k]**2)
            Te = var1 + var2 + var3
            
            H__ = meta[k]['planck_constant']
            C__ = meta[k]['speed_of_light']
            K__ = meta[k]['boltzmann_constant']
            gamma__ = gamma[k] * 1e-6
            
            r_var1 = ( 2 * H__ * ( C__**2 ) )/ gamma__**5
            r_var2 = 1/( N.exp( ( H__ * C__ ) / ( K__ * gamma__* Te ) ) - 1 )
            radiance[k] = r_var1 * r_var2
            #print radiance[k].max(), radiance[k].min()
    return radiance
    
def save_H8_hdf5(title, h08_data, h08_radiance, h08_time, h08_coords, \
                 hrit_listb = hrit_listb):#,h08_gamma): central wavelength removed
    """ WRITING radar data in HDF5 file per SWEEP"""
    savefilename = title+'.hdf5'
    #create a metadata for the output
    metadata = {}
    metadata['date_time'] = h08_time
    #metadata['Central_wavelength'] = 
    f = h5py.File(savefilename,'w')
    grp = f.create_group('HIMAWARI')
    
    f.create_dataset('HIMAWARI/COORDINATES/longitude/',\
                data = h08_coords["Longitude"], compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/latitude/',\
                data = h08_coords["Latitude"], compression = 'gzip', compression_opts=9)
    #f.create_dataset('HIMAWARI/CENTRAL_WAVELENGTH/',\
    #            data = h08_gamma, compression = 'gzip')
      
    for k in hrit_listb:
        f.create_dataset('HIMAWARI/DATA/'+k,\
                data = h08_data[k], compression = 'gzip', compression_opts=9)
        f.create_dataset('HIMAWARI/RADIANCE/'+k,\
                data = h08_radiance[k], compression = 'gzip', compression_opts=9)
    for key in metadata.keys():
        grp.attrs[key] = metadata[key]
    print "\n"+savefilename +" SAVED"
    f.close()
    
def read_h8_hdf5(title, hrit_listb = hrit_listb):
    """ Reading Himawari HDF5 file """
    f = h5py.File(title, 'r')
    
    # get metadata
    date_time = f['HIMAWARI'].attrs['date_time']
    # get coordinates
    longitude = N.array(f['HIMAWARI/COORDINATES/longitude'])
    latitude = N.array(f['HIMAWARI/COORDINATES/latitude'])
    # get data
    h08_data = {}
    h08_radiance = {}
    for i in hrit_listb:
        print i
        h08_data[i] = (N.array(f['HIMAWARI/DATA'][i]))
        h08_radiance[i] = (N.array(f['HIMAWARI/RADIANCE'][i]))
    f.close()
    print "Reading "+ title
    return h08_data, h08_radiance, longitude, latitude, date_time

def open_hdf(directory):
    os.chdir(directory)
    print "Current directory: " +directory
    print "Scanning Himawari 8 HDF5 files"
   
    _file_ = glob.glob("*.hdf5")
   
    _file_list_ = []
    for i, line in enumerate(_file_):
        _file_list_.append(line.split()[0])
    _file_.close()
    return _file_list_
    
def subset_center_point(data,center_lon, center_lat, radius, grid_x, grid_y):
    right_lon = center_lon + (radius/111.)
    left_lon = center_lon - (radius/111.)
    up_lat = center_lat + (radius/111.)
    down_lat = center_lat - (radius/111.)
    """Creates Philippine mask"""
    same = ~((grid_x > left_lon)&(grid_x < right_lon)&(grid_y > down_lat )&(grid_y < up_lat))
    index_x, index_y = N.where((grid_x > left_lon)&(grid_x < right_lon)&(grid_y > down_lat )&(grid_y < up_lat))
    map_masked = N.ma.MaskedArray(data, mask =same)
    map_subset = data[ N.min(index_x):N.max(index_x) , N.min(index_y):N.max(index_y) ]
    lon_subset = grid_x[ N.min(index_x):N.max(index_x) , N.min(index_y):N.max(index_y) ]
    lat_subset = grid_y[ N.min(index_x):N.max(index_x) , N.min(index_y):N.max(index_y) ]
    return map_masked, map_subset, lon_subset, lat_subset
    
def create_datelist_H8(start, end, time_interval=3600):
    """ Creates list of dates of himawari
        > start:    start date
        > end : end date
        > time interval:    dtype = integer
                            unit = seconds
                            default = 3600 sec
    """
    #start = '20140601'
    year_1 = start[0:4]
    month_1 = start[4:6]
    day_1 = start[6:8]
    hh_1 = start[9:11]
    mm_1 = start[11:13]
    
    year_2 = end[0:4]
    month_2 = end[4:6]
    day_2 = end[6:8]
    hh_2= end[9:11]
    mm_2 = end[11:13]
    #end = '20140930'
    
    #Generate series of dates up to final date
    _dates_ = []
    _dates2_ = []
    ref_date = datetime.datetime(int(year_1),int(month_1),int(day_1),\
                int(hh_1), int(mm_1))
    terminal_date = datetime.datetime(int(year_2),int(month_2),int(day_2),\
                int(hh_2), int(mm_2))
    actual_date = 0
    t = 0
    #print ref_date
    while actual_date != terminal_date :
        actual_date = ref_date +datetime.timedelta(0, int(t)*time_interval)
        _dates_.append(actual_date.strftime('%Y%m%d_%H%M'))
        #_dates1_.append(actual_date.strftime('/%Y/%m/%d/'))
        _dates2_.append(actual_date.strftime('/%Y%m/%d/%H/'))
        t = t+1
        #print actual_date, terminal_date
    _dates_ = N.array(_dates_,dtype='|S13')
    #_dates1_ = N.array(_dates1_,dtype='|S12')
    _dates2_ = N.array(_dates2_,dtype='|S14')
    return _dates_, _dates2_

def change_datetime_format(date_time,sec_include =False):
    year_1 = date_time[0:4]
    month_1 = date_time[4:6]
    day_1 = date_time[6:8]
    hh_1 = date_time[9:11]
    mm_1 = date_time[11:13]
    ss_1 = "00"
    
    if sec_include == True:
        ss_1 = date_time[13:15]
        
    ref_date = datetime.datetime(int(year_1),int(month_1),int(day_1),\
        int(hh_1), int(mm_1), int(ss_1))
    return ref_date
    
def radar_himawari_time( radar_time, himawari_time ):
    time_before = []
    time_after = []
    for i in radar_time:
        time_before_tmp = []
        time_after_tmp = []
        for j in himawari_time:
            diff = (j - i).total_seconds()
            
            if N.sign(diff) == -1.0:
                
                time_before_tmp.append(abs(diff))
            elif N.sign(diff) == 1.0:
                
                time_after_tmp.append(abs(diff))
            else:
                print i
                time_before_tmp.append(abs(diff))
                time_after_tmp.append(abs(diff))
        time_before.append(i - datetime.timedelta(0,int(min(time_before_tmp))))
        time_after.append(i + datetime.timedelta(0,int(min(time_after_tmp))))
    return time_before, time_after


@concurrent( processes =3 )
def single_download(combi, counter, totals,\
                    _dates_, _dates1_, path_out,\
                    dat_list = dat_list,\
                    dat_list_reso = dat_list_reso,\
                    user_name = "rednacky_gmail.com",\
                    user_password = "SP+wari8",\
                    proxy_switch = "off" ):
    
    # H8 filename  to download
    #print combi
    #print _dates_, dat_list[ combi[0] ], dat_list_reso[ combi[0] ], combi[1]
    file_dl = 'HS_H08_'+ _dates_ +'_'+ combi[0] +\
              '_FLDK_'+  combi[1]  +'_S'+ combi[2] +'10.DAT.bz2'
              
    ftp_site = 'ftp://ftp.ptree.jaxa.jp/jma/hsd'
    wget_c = "wget -o download.log -c "+\
             "--directory-prefix="+ path_out +" "+\
             "--tries=5 --read-timeout=20 "+\
             "--passive-ftp --ftp-user="+ user_name +" "+\
             "--ftp-password="+ user_password +" "+\
             "-e use_proxy="+ proxy_switch +" "
    #-o download.log 
    # command
    #print wget_c + ftp_site + _dates1_ + file_dl
    out = os.system(wget_c + ftp_site + _dates1_ + file_dl)
    progress_bar(counter, totals, desc = file_dl)
    
    # checks if data exist
    if out == 0:
        indicator = os.path.exists(os.path.join(path_out,file_dl))
        if indicator == True:
            return file_dl
        else:
            os.sys.exit("Data downloaded but missing: "+ file_dl)
            
    else:
#        print"\n\n\tRetry download. Data download unsuccesfull: "+ file_dl
#        internet = check_internet()
#        if internet == True:
#            print "\tConnected to the internet but data cannot be downloaded."
        return N.nan


@synchronized
def download_h8(_dates_, _dates1_, path_out, dat_list = dat_list, dat_segment = dat_segment,\
                dat_list_reso = dat_list_reso,\
                user_name = "rednacky_gmail.com", user_password = "SP+wari8",\
                proxy_switch = "off" ):
    """
    use to download himawari data
    input:
        _dates_ : w/ format '%Y%m%d_%H%M'
        _dates1_ : w/ format '/%Y%m/%d/%H/'
        
    ouput:
        none
    """
    print "\n"
    print "Downloading Himawari-8 data :\t",_dates_
    
    start_time = datetime.datetime.now()
    
    combinations = []
    for m, k in enumerate(dat_list):
        for n in dat_segment:
            #print [ dat_list[m], dat_list_reso[m], n ]
            combinations.append([ dat_list[m], dat_list_reso[m], n ])
            
    combinations = N.array(combinations)
    total = len(combinations)
    
    list_file_dl = {}
    for ctr, i in enumerate(combinations):
        list_file_dl[ctr]  = single_download(i, ctr, total,\
                                             _dates_, _dates1_, path_out,\
                                             dat_list = dat_list,\
                                             dat_list_reso = dat_list_reso)            

    list_file_dl = N.array(list_file_dl.values(), dtype = str)
    
    time1 = datetime.datetime.now()
    print "\n\n\tNo. of files downloaded :", N.shape(list_file_dl)[0]# must be 48 files
    print('\n\n\tDuration of H8 download: {}'.format(time1 - start_time))

    return list_file_dl
