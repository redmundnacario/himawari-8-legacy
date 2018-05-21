# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 06:27:09 2017

@author: red
"""
import numpy as N
import os
from main_himawari.netcdf_himawari_functions import read_h8_l1_netcdf
from main_himawari.himawari_preprocessing_functions import get_H8_IR_split_window,\
                                                           get_subset_points, subset_square,\
                                                           interpolate_data
from main_himawari.himawari_preprocessing_var import tagx, tagy, tag_range,\
                                                     BTD_BT_listb
from main_radar.initial_values_radar_functions import h08_lon, h08_lat, h08_lon_ph, h08_lat_ph


# read a h8_netcdf file
path_h8 = ("/media/red/SAMSUNG/spatial_temporal_matching/radar/h8_testing_data/sample_h8_netcdf")
h8_file = "NC_H08_20160804_1200_R21_FLDK.06001_06001.nc"

data_h8, h08_time, h8_net_lon, h8_net_lat, units = read_h8_l1_netcdf(os.path.join(path_h8, h8_file))


# convert to BTD/BT
#h8_BTD_BT = get_H8_IR_split_window(data_h8)
#tag_x = 121.022216796875
#tag_y = 14.142129898071289
#tag_range = 120.0
#index_x, index_y = subset_square(tag_x, tag_y, tag_range, h8_net_lon, h8_net_lat)
#map_subset = get_subset_points(data_h8["IR1"], index_x, index_y)#sample data
#map_subset_lon = get_subset_points(h8_net_lon, index_x, index_y)
#map_subset_lat = get_subset_points(h8_net_lat, index_x, index_y)


# interpolate map from h8_netcdf coordinate to the default coordinate
new_data = interpolate_data(data_h8["IR1"], h8_net_lon, h8_net_lat, h08_lon_ph, h08_lat_ph)

# plot
from main_radar.radar_functions_plot_v2 import *

def mpcolormesh(data_, lon, lat, cmap=None,vmin=None ,vmax=None):  
    plt.figure()
    
    #m =create_basemap()
    m = Basemap(resolution = 'h', llcrnrlon = 114.0, llcrnrlat = 4.0, \
                urcrnrlon =136.0, urcrnrlat = 24.0)
    m.drawcoastlines()
    m.pcolormesh(lon, lat,data_,cmap=cmap,vmin =vmin, vmax = vmax)
    cb = plt.colorbar(shrink = 0.60)
    
    
mpcolormesh(N.ma.masked_invalid(new_data), h08_lon_ph, h08_lat_ph)
#mpcolormesh(map_subset, map_subset_lon, map_subset_lat)
mpcolormesh(data_h8["IR1"], h8_net_lon, h8_net_lat)



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
