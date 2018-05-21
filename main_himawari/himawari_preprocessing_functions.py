import os
import numpy as N
import datetime
from geopy.distance import vincenty
import h5py
import glob

from main_himawari.himawari_preprocessing_var import tagx, tagy, tag_range,\
                                                     BTD_BT_listb
from pears_himawari.himawari_var import hrit_list                                                   
from main_himawari.himawari_functions import read_h8_hdf5

from deco import concurrent
from util.main_util import progress_bar

from main_himawari.netcdf_himawari_functions import read_h8_l1_netcdf
from main_radar.initial_values_radar_functions import h08_lon, h08_lat, h08_lon_ph, h08_lat_ph
from scipy.interpolate import griddata

# General function for making list of Himawari HDF data



def open_h8_hdf(directory, mode = "default"):
    """
    Makes list of Himawari hdf5 data in a dricetory
    Input:
    directory       Path of Himawari hdf5 data
    mode            
                    *_PH_R20_S030405.hdf5               "default". First level data
                    *_PH_R20_S030405_BTD_BT.hdf5        "PH". Second Level
                    *_TAG_R20_S030405_BTD_BT.hdf5       "TAG". Second Level
        
    Return:
    _file_list_     File list
    """
    
    os.chdir(directory)
    print "\nCurrent directory: " +directory
    print "Scanning Himawari 8 HDF5"
    print "Mode: "+mode
    print "\n"
    
    if mode == "default":
        _file_ = glob.glob("*_PH_R20_S030405.hdf5")
    elif mode == "PH":
        _file_ = glob.glob("*_PH_R20_S030405_BTD_BT.hdf5")
    elif mode == "TAG":
        _file_ = glob.glob("*_TAG_R20_S030405_BTD_BT.hdf5")
    else:
        os.sys.exit("Error: Type of file \""+mode+"\" not found")
        
    _file_list_ = []
    for i, line in enumerate(_file_):
        _file_list_.append(line.split()[0])
    
    return _file_list_
    
    
    
def save_H8_level2_hdf5(pathtosave, h08_BTD_BT, h08_time, h08_longitude, h08_latitude, mode = "PH",\
                        h8_lvl1 = False):
    """
    WRITES BTD and BT from Himawari, can also write subsetted data(mode:TAG)
    
    Input:
    pathtosave      Path where to save output
    h08_BTD_BT      Himawari 8 data
    h08_time        date time
    h08_longitude         Longitude
    h08_latitude         Latitude
    mode            "PH" or "TAG"
    
    Ouput:
    "HS_H08_"+h08_time+"_"+mode+"_R20_S030405_BTD_BT.hdf5"
    """
    savefilename = "HS_H08_"+h08_time+"_"+mode+"_R20_S030405_BTD_BT.hdf5"
    #print "Writing "+ savefilename
    savefilename2 = pathtosave+"/"+savefilename
    #create a metadata for the output
    metadata = {}
    metadata['date_time'] = h08_time 
    f = h5py.File(savefilename2,'w')
    grp = f.create_group('HIMAWARI')
    
    f.create_dataset('HIMAWARI/COORDINATES/longitude/',\
                data = h08_longitude, compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/latitude/',\
                data = h08_latitude, compression = 'gzip', compression_opts=9)
      
    for k in BTD_BT_listb:
        f.create_dataset('HIMAWARI/BTD_BT/'+k,\
                data = h08_BTD_BT[k], compression = 'gzip', compression_opts=9)
        #print "Saving : "+k+" in filename: "+savefilename
                
    if h8_lvl1 == True:
        for k in hrit_list:
            f.create_dataset('HIMAWARI/DATA/'+k,\
                    data = h08_BTD_BT[k], compression = 'gzip', compression_opts=9)
                    
    for key in metadata.keys():
        grp.attrs[key] = metadata[key]
    #print savefilename2+" saved"
    f.close()
    
def read_h8_hdf5_level1(title, hrit_listb = hrit_list):
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
    
def read_h8_level2_hdf5(title, h8_lvl1 = False):
    """
    Reading Himawari HDF5 file
    """
    #print "REading : "+ os.path.basename(title)
    f = h5py.File(title, 'r')
    
    # get metadata
    h08_time = f['HIMAWARI'].attrs['date_time']
    # get coordinates
    h08_longitude = N.array(f['HIMAWARI/COORDINATES/longitude'])
    h08_latitude = N.array(f['HIMAWARI/COORDINATES/latitude'])
    # get data
    h08_BTD_BT= {}
    for i in BTD_BT_listb:
        h08_BTD_BT[i] = (N.array(f['HIMAWARI/BTD_BT'][i]))
        
    if h8_lvl1 == True:
        for i in hrit_list:
            h08_BTD_BT[i] = (N.array(f['HIMAWARI/DATA'][i]))
            
    f.close()
    return h08_BTD_BT, h08_longitude, h08_latitude, h08_time



def convert_BTD_BT(date_list, file_list, path_to_open, path_to_save, mode ="PH",\
                   tagx = tagx, tagy = tagy, tag_range = tag_range,\
                   h8_lvl1 = False, h8_data_type = "default",\
                   interpolate_lon_lat = True, replace = False):
    """
    Write Himawari 8 data into BTD and BT data
    
    Input:
    path_to_open    Path where to input data is located
    path_to_save    Path where to save ouput data
    mode            "PH" or "TAG"
    
    Ouput:
    "HS_H08_"+h08_time+"_"+mode+"_R20_S030405_BTD_BT.hdf5"
    """

    # make lists of file
    #file_list_H = open_h8_hdf(path_to_open, mode = "default")
    # make lists of path
    #file_list_H_open = [path_to_open+"/"+i for i in file_list_H]
    # reads and process the data
    totals = len(file_list)
    print "\n"
    print "="*75
    print mode, os.path.basename(path_to_open)
    print "\n"
    
    for ctr, i in enumerate(file_list):
        sdate_time  = date_list[ctr]
        sample_fout = os.path.join(path_to_save,\
                                   "HS_H08_"+ sdate_time +"_"+mode+\
                                   "_R20_S030405_BTD_BT.hdf5" )
                                   
        if os.path.exists(sample_fout) == True:
            if replace == True:
                print ctr, sdate_time, "replacing."
            else:
                print ctr, sdate_time, "exists."
                continue
        else:
            print "\n"
            print ctr, sdate_time, os.path.basename(i)
            print "\n"

        if h8_data_type == "default":
            print i
            h08_data, h08_radiance, lon_geos, lat_geos, date_time = read_h8_hdf5_level1(i)
            
        elif h8_data_type == "netcdf":
            
            try:
                h08_data, date_time, lon_geos, lat_geos, units = read_h8_l1_netcdf(i)
            except IOError:
                print "\n"
                print  ctr, sdate_time, os.path.basename(i),"is corrupted"
                print "\n"
                continue
            
            if interpolate_lon_lat == True:
                for j in hrit_list:
                    #print j
                    h08_data[j] = interpolate_data(h08_data[j], lon_geos, lat_geos, h08_lon_ph, h08_lat_ph)      
                lon_geos = h08_lon_ph
                lat_geos = h08_lat_ph
                
#        if os.path.exists(path_to_save+"/HS_H08_"+date_time+"_"+mode+"_R20_S030405_BTD_BT.hdf5") == True and mode == "PH":
#            print "HS_H08_"+date_time+"_"+mode+"_R20_S030405_BTD_BT.hdf5 exists ==================="
#            continue
#        del h08_radiance
        
        # Get H8 split window
        BTD_BT = get_H8_IR_split_window(h08_data)

        # save into separate file
        if mode == "PH":
            
            if h8_lvl1 == True:
                for j in hrit_list:
                    BTD_BT[j] = h08_data[j]
            
            save_H8_level2_hdf5(path_to_save, BTD_BT, sdate_time, lon_geos, lat_geos,\
                                mode = mode, h8_lvl1 = h8_lvl1)
            # test if save georef point is the same as to other points
            # <> edit
            progress_bar(ctr, totals, desc = "PH"+" " +os.path.basename(path_to_open)+\
                                             " "+ i, def_total=10)
        elif mode == "TAG":
            # get index address
            index_x, index_y = subset_square(tagx, tagy, tag_range, lon_geos, lat_geos)
            # get lon and lat
            map_subset_lon = get_subset_points(lon_geos, index_x, index_y)
            map_subset_lat =  get_subset_points(lat_geos, index_x, index_y)
            #print N.shape(map_subset_lon)
            # write subset data
            
            map_subset = {}
            for j in BTD_BT_listb:
                map_subset[j] = get_subset_points(BTD_BT[j], index_x, index_y)
                
            if h8_lvl1 == True:
                for j in hrit_list:
                    map_subset[j] = get_subset_points(h08_data[j], index_x, index_y)
                
            save_H8_level2_hdf5(path_to_save, map_subset, sdate_time, map_subset_lon,\
                                map_subset_lat, mode = mode, h8_lvl1 = h8_lvl1)
                                
            progress_bar(ctr, totals, desc = "TAG"+" " +os.path.basename(path_to_open)+\
                                             " "+ os.path.basename(i), def_total=10)
        else:
            os.sys.exit("Error: Creating H8 file\""+mode+"\" not found")
        
def get_H8_IR_split_window(h08_data):
    """
    Input:
    h08_data : Dictionary of Himawari-8 data
    
    Return:
    BTD_BT : Dictionary of IR split windows (unit KELVIN)
    """
    BTD_BT = {}
    BTD_BT["CTH1"] = h08_data["IR3"]- h08_data["IR1"]
    BTD_BT["CTH2"] = h08_data["IR3"]- h08_data["B10"]
    BTD_BT["CTH3"] = h08_data["B16"]- h08_data["IR1"]
    BTD_BT["CTH4"] = h08_data["B12"]- h08_data["B16"]
    BTD_BT["CTH5"] = h08_data["IR1"]
    #COT
    BTD_BT["COT1"] = h08_data["IR1"]- h08_data["IR2"]
    BTD_BT["COT2"] = h08_data["B11"]- h08_data["IR2"]
    #CP
    BTD_BT["CP"] = h08_data["B11"]- h08_data["IR1"]
    #CWP
    BTD_BT["CWP1"] = h08_data["IR4"]- h08_data["IR1"]
    BTD_BT["CWP2"] = h08_data["IR4"]- h08_data["B10"]
    return BTD_BT



def save_georef_points(label, h08_longitude, h08_latitude, binary_map, pathtosave):
    """
    WRITING data of regular grid points Longitude and Latitude from Himawari 8
    data.
    label
    h08_longitude         Longitude data
    h08_latitude         Latitude data
    binary_map      Created nask map
    pathtosave      Path where to save ouput data
    """
    print "saving : "+ label +" georef points"
    savefilename = "HS_H08_GEOREF_POINTS_"+label+"_R20_S030405.hdf5"
    savefilename2 = pathtosave+"/"+savefilename
    f = h5py.File(savefilename2,'w')
    f.create_group('HIMAWARI')
    f.create_dataset('HIMAWARI/MASK/MASK_TAGAYTAY',\
                data = binary_map, compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/longitude/',\
                data = h08_longitude, compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/latitude/',\
                data = h08_latitude, compression = 'gzip', compression_opts=9)
    f.close()
    
    
    
def read_georef_points(title):
    """ 
    Reading Himawari HDF5 geroref pointsf data 
    """
    
    #print "REading : "+ os.path.basename(title)
    f = h5py.File(title, 'r')
    # get coordinates
    binary_map = N.array(f['HIMAWARI/MASK/MASK_TAGAYTAY'])
    h08_longitude = N.array(f['HIMAWARI/COORDINATES/longitude'])
    h08_latitude = N.array(f['HIMAWARI/COORDINATES/latitude'])
    f.close()
    return h08_longitude, h08_latitude, binary_map



def subset_square(center_lon, center_lat, radius, grid_x, grid_y):
    """
    Creating first a square grid before subsetting into circle
    
    Input:
    center_lon      Longitude of a point
    center_lat      Latitude of a point
    radius          
    grid_x
    grid_y
    
    Return:
    index_x, index_y    Array address where conditions are True
    """
    
    print "Subsetting a map into square"
    
    right_lon = center_lon + ((radius+10)/111.)
    left_lon = center_lon - ((radius+10)/111.)
    up_lat = center_lat + ((radius+10)/111.)
    down_lat = center_lat - ((radius+10)/111.)
    index_x, index_y = N.where((grid_x > left_lon) & (grid_x < right_lon) & (grid_y > down_lat ) & (grid_y < up_lat))
    return index_x, index_y
    
    
    
def get_subset_points(data, index_x, index_y):
    """
    Part two of subset square 
    After getting the indexes inside the square, the data can be accessed

    Input:
    data            Data to be subset
    index_x         Lon indices
    index_y         lat indices
    
    Return
    map_subset      Subsetted map
    """
    
    map_subset = data[ N.min(index_x):N.max(index_x) , N.min(index_y):N.max(index_y) ]
    return map_subset



def create_mask_TAGAYTAY_circle(map_subset_lon, map_subset_lat,\
                                center_lon, center_lat, radius_range):
    """
    Subsets into circle with TAGAYTAY as center
    
    Input:
    grid_data           Himawari 8 data
    map_subset_lon      Himawari 8 subsetted square georef longitude values
    map_subset_lat      Himawari 8 subsetted square georef latitude values
    center_lon          Radar station longitude 
    center_lat          Radar station latitude
    radius_range        Radar station range
    
    Return:
    grid_data           Himawari 8 data within radius range of radar
    binary              Himawari 8 binary data 1 -> mask, 0 -> needed data
    """
    
    print "Extracting binary map  (circle) : TAGAYTAY"
    map_subset_lon1 = map_subset_lon.flatten()
    map_subset_lat1 = map_subset_lat.flatten()
    
    dist1 = []
    binary = []
    
    for i in xrange(N.shape(map_subset_lon1)[0]):
        dist = vincenty((map_subset_lat1[i], map_subset_lon1[i]), (center_lat, center_lon)).kilometers
        dist1.append(dist)
        # 120 - 1 = 119 km !!! OUTER LIMIT of RADAR RANGE !!!
        if dist <= (radius_range - 1.0):
            binary.append(0)
        else:
            binary.append(1)
            
    dist1 = N.array(dist1)
    binary = N.array(binary)
    dist1 = dist1.reshape(N.shape(map_subset_lon)[0],N.shape(map_subset_lon)[1])
    binary = binary.reshape(N.shape(map_subset_lon)[0],N.shape(map_subset_lon)[1])
    index_x, index_y = N.where(binary == 1)
    #grid_data[index_x, index_y] = N.nan
    return binary
    

def interpolate_data(_data_, lon_source, lat_source, target_lon, target_lat):
    """ """
    x_source = N.ravel(lon_source)
    y_source = N.ravel(lat_source)
    point_source = N.column_stack([x_source, y_source])
    data_source = N.ravel(_data_)
    new_data = griddata(point_source, data_source, (target_lon, target_lat))
    new_data = N.ma.masked_invalid(new_data).filled(N.nan)
    return new_data