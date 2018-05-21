# -*- coding: utf-8 -*-
"""
Created on Sat May 14 04:27:14 2016

@author: red
"""

import h5py
import numpy as N
import os

def write_cloudmask_hdf5(_data_, path , longitude, latitude, date_time):
    savefilename = os.path.join(path, "H8_"+ date_time +"_cloud_mask.hdf5")
    #create a metadata for the output
    metadata = {}
    metadata['date_time'] = date_time
    #metadata['Central_wavelength'] = 
    f = h5py.File(savefilename,'w')
    grp = f.create_group('HIMAWARI')
    
    f.create_dataset('HIMAWARI/COORDINATES/longitude/',\
                data = longitude, compression = 'gzip',compression_opts=9)
    f.create_dataset('HIMAWARI/COORDINATES/latitude/',\
                data = latitude, compression = 'gzip', compression_opts=9)
    f.create_dataset("HIMAWARI/CLOUD_MASK/",\
                data = _data_, compression = 'gzip')
                
    for key in metadata.keys():
        grp.attrs[key] = metadata[key]
    print savefilename +" SAVED"
    f.close()
    
def read_cloudmask_hdf5(path):
    """ Reading Himawari HDF5 file """
    f = h5py.File(path, 'r')
    # get metadata
    date_time = f['HIMAWARI'].attrs['date_time']
    # get coordinates
    longitude = N.array(f['HIMAWARI/COORDINATES/longitude'])
    latitude = N.array(f['HIMAWARI/COORDINATES/latitude'])
    # get data
    cloud_mask  = N.array(f["HIMAWARI/CLOUD_MASK/"])
    f.close()
    print "Reading "+ os.path.basename(path)
    return cloud_mask, longitude, latitude, date_time