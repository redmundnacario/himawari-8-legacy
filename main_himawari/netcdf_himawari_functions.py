# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 06:25:02 2017

@author: red
"""

from netCDF4 import Dataset
import numpy as N
import os
import datetime
import h5py

from pears_himawari.himawari_var import hrit_listb, x_ll, y_ll, x_ur ,y_ur


# subset: given 4 points, extracts the lat and lon
def subset_h8map(obs_coords, longitude, latitude):
    """ Return x and y address
    """
    same = ((longitude > obs_coords[:,0].min()) & (longitude <= obs_coords[:,0].max()) &\
            (latitude > obs_coords[:,1].min()) & (latitude <= obs_coords[:,1].max()))
    xadd, yadd = N.where(same)[0],N.where(same)[1]

    #xadd.shape, yadd.shape
    xadd, yadd = N.meshgrid(N.unique(xadd),N.unique(yadd))
    return xadd, yadd



# read netcdf
def read_h8_l1_netcdf(h8_file_n_path, x_ll= x_ll, y_ll= y_ll,\
                      x_ur = x_ur, y_ur = y_ur):
    
    #h8_path = "/home/red/Desktop/phl_microsat/task_4"
    #h8_file = "NC_H08_20160901_0000_R21_FLDK.06001_06001.nc"
    
    fh = Dataset(h8_file_n_path, mode = "r")
    
    h08_coords = {}
    h08_coords["Longitude"] = fh.variables["longitude"][:]
    h08_coords["Latitude"] = fh.variables["latitude"][:]
    x_lon, y_lat = N.meshgrid(h08_coords["Longitude"], h08_coords["Latitude"])
    
    obs_coords = N.array([[x_ll,y_ll], [x_ur, y_ur]])
    xadd, yadd = subset_h8map(obs_coords, x_lon, y_lat)
    
    x_lon = x_lon[xadd,yadd]
    y_lat = y_lat[xadd, yadd]
    h08_longitude = x_lon
    h08_latitude = y_lat
    
    data_h8 = {}
                   
    data_h8["B01"] = fh.variables["albedo_01"][:][xadd, yadd]
    data_h8["B02"] = fh.variables["albedo_02"][:][xadd, yadd]
    data_h8["VIS"] = fh.variables["albedo_03"][:][xadd, yadd]
    data_h8["B04"] = fh.variables["albedo_04"][:][xadd, yadd]
    data_h8["B05"] = fh.variables["albedo_05"][:][xadd, yadd]
    data_h8["B06"] = fh.variables["albedo_06"][:][xadd, yadd]
    
    data_h8["IR4"] = fh.variables["tbb_07"][:][xadd, yadd]
    data_h8["IR3"] = fh.variables["tbb_08"][:][xadd, yadd]
    data_h8["B09"] = fh.variables["tbb_09"][:][xadd, yadd]
    data_h8["B10"] = fh.variables["tbb_10"][:][xadd, yadd]
    data_h8["B11"] = fh.variables["tbb_11"][:][xadd, yadd]
    data_h8["B12"] = fh.variables["tbb_12"][:][xadd, yadd]
    data_h8["IR1"] = fh.variables["tbb_13"][:][xadd, yadd]
    data_h8["B14"] = fh.variables["tbb_14"][:][xadd, yadd]
    data_h8["IR2"] = fh.variables["tbb_15"][:][xadd, yadd]
    data_h8["B16"] = fh.variables["tbb_16"][:][xadd, yadd]
    
    # get units
    units = {}
    units["B01"] = str(fh.variables["albedo_01"].units)
    units["B02"] = str(fh.variables["albedo_02"].units)
    units["VIS"] = str(fh.variables["albedo_03"].units)
    units["B04"] = str(fh.variables["albedo_04"].units)
    units["B05"] = str(fh.variables["albedo_05"].units)
    units["B06"] = str(fh.variables["albedo_06"].units)
    
    units["IR4"] = str(fh.variables["tbb_07"].units)
    units["IR3"] = str(fh.variables["tbb_08"].units)
    units["B09"] = str(fh.variables["tbb_09"].units)
    units["B10"] = str(fh.variables["tbb_10"].units)
    units["B11"] = str(fh.variables["tbb_11"].units)
    units["B12"] = str(fh.variables["tbb_12"].units)
    units["IR1"] = str(fh.variables["tbb_13"].units)
    units["B14"] = str(fh.variables["tbb_14"].units)
    units["IR2"] = str(fh.variables["tbb_15"].units)
    units["B16"] = str(fh.variables["tbb_16"].units)
    
    
    # get sun zenith and azimuth angle
    data_h8["SOZ"] = fh.variables["SOZ"][:][xadd, yadd]
    units["SOZ"] = str(fh.variables["SOZ"].units)
    data_h8["SOA"] = fh.variables["SOA"][:][xadd, yadd]
    units["SOA"] = str(fh.variables["SOA"].units)
    
    #time
    timestamp = fh.variables["end_time"][:][0]
    time_offset = fh.variables["end_time"].units.split()[-2:]
    fh.close()
    
    old_time = str(" ".join(time_offset))
    old_time = datetime.datetime.strptime(old_time, "%Y-%m-%d %H:%M:%S")
    h08_time = old_time.toordinal() + timestamp
    h08_time = datetime.datetime.fromordinal(int(h08_time))
    h08_time = datetime.datetime.strftime(h08_time, "%Y%m%d_%H%M")
    
    return data_h8, h08_time, h08_longitude, h08_latitude, units



def save_h8_l1_hdf5(h08_data, h08_time, h08_coords, path_out, \
                    hrit_listb = hrit_listb):
    """ WRITING radar data in HDF5 file per SWEEP

    HS_H08_YYYYMMDD_hhmm_Bbb_FLDK_Rjj_Skkll.DAT
    HS_H08_20150707_2310_PH_R20_S030405.hdf5
    """
    title = "HS_H08_" + h08_time +"_PH_R20_S030405.hdf5"
    savefilename = os.path.join(path_out, title)

    metadata = {}
    metadata['date_time'] = h08_time

    f = h5py.File(savefilename,'w')
    grp = f.create_group('HIMAWARI')
    
    f.create_dataset('HIMAWARI/COORDINATES/longitude/',\
                data = h08_coords["Longitude"], compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/latitude/',\
                data = h08_coords["Latitude"], compression = 'gzip', compression_opts=9)
      
    for k in hrit_listb:
        f.create_dataset('HIMAWARI/DATA/'+k,\
                data = h08_data[k], compression = 'gzip', compression_opts=9)
                
    f.create_dataset('HIMAWARI/ANGLE/SOZ/',\
                data = h08_data["SOZ"], compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/ANGLE/SOA/',\
                data = h08_data["SOA"], compression = 'gzip', compression_opts=9)           
                
    for key in metadata.keys():
        grp.attrs[key] = metadata[key]
    print "\n"+savefilename +" SAVED"
    f.close()
    return title

def read_h8_l1_hdf5(path_file, hrit_listb = hrit_listb):
    f = h5py.File(path_file, 'r')
    
    # get metadata
    h08_metadata = {}
    h08_metadata["date_time"] = f['HIMAWARI'].attrs['date_time']
    
    # get coordinates
    h08_data = {}
    
    h08_data["Longitude"] = N.array(f['HIMAWARI/COORDINATES/longitude'])
    h08_data["Latitude"] = N.array(f['HIMAWARI/COORDINATES/latitude'])
    
    # get data
    for i in hrit_listb:
        h08_data[i] = N.array(f['HIMAWARI/DATA'][i])
        
    h08_data["SOZ"] = N.array(f['HIMAWARI/ANGLE/SOZ'])
    h08_data["SOA"] = N.array(f['HIMAWARI/ANGLE/SOA'])
    
    f.close()
    return h08_data, h08_metadata

#save_h8_l1_hdf5(data_h8, h08_time, h08_coords, h8_path)

#from pears_himawari.himawari_plot_function import plot_img
#
#plot_img(x_lon[xadd,yadd], x_lon[xadd,yadd], y_lat[xadd, yadd], "longitude", "20160901_0000", "longitude_subset", h8_path ,\
#        cmapp = "spectral", vmin =x_ll, vmax = x_ur)
#plot_img(y_lat[xadd,yadd], x_lon[xadd,yadd], y_lat[xadd, yadd], "latitude", "20160901_0000", "latitude_subset", h8_path ,\
#        cmapp = "spectral", vmin =y_ll, vmax = y_ur)

#vis = fh.variables["albedo_03"][:][xadd, yadd]
#fh.close()
#plot_img(vis, x_lon[xadd,yadd], y_lat[xadd, yadd], "albedo", "20160901_0000", "vis_subset", h8_path ,\
#        cmapp = "Greys_r", vmin =vis.min(), vmax = vis.max())
