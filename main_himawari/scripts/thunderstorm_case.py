# -*- coding: utf-8 -*-
"""
1. Open radar data
    > pre-process
    > grid
Created on Tue Dec  8 22:44:01 2015
@author: red
"""
# importing functions from different folder
import sys
sys.path.insert(0, '/media/red/SAMSUNG/main/main_radar')
sys.path.insert(0, '/media/red/SAMSUNG/main/main_himawari')
from radar_preprocessing_functions import *
from rainfall_retrieval_functions import *
from radar_functions_plot import *
from himawari_functions import *
from plot_functions_basic import *


# directories of radar data
#path_radar = '/media/red/SAMSUNG/radar/tagaytay/ty_lando'
path_radar = '/media/red/SAMSUNG/radar/tagaytay/thunderstorm/hdf5_case1'
# directory of himawari
#path_himawari = '/media/red/SAMSUNG/himawari/ty_lando'
path_himawari = '/media/red/SAMSUNG/himawari/thunderstorm'

# read hdf5 radar data
#   change directory then open list of hdf5
file_list = open_list_radar_hdf5(path_radar)

variables_da1, date, time, attr = read_hdf5_radar(file_list[22])
#radar data
#variables_da1['ZH_PIA']

# read himawari data
#   change directory then open list of hdf5
file_list_H = open_hdf(path_himawari)
h08_data, h08_radiance, lon_geos, lat_geos, date_time = read_h8_hdf5(file_list_H[0])

#   subset data
map_masked, map_subset,lon_subset, lat_subset = subset_center_point(h08_data['B14'],attr['coords'][0], attr['coords'][1], 120,lon_geos,lat_geos)
#       BTD IR3 - IR1  or 6.2 microns - 10.4 micron #convectivity
IR_diff_2 = h08_data["IR3"] - h08_data["IR1"]
map_masked, IR_diff_2,lon_subset, lat_subset = subset_center_point(IR_diff_2,attr['coords'][0], attr['coords'][1], 120,lon_geos,lat_geos)
#       BTD IR2 - IR1 or 12.3 - 10.4 #water vapor sensitivity
IR_diff = h08_data["IR2"] - h08_data["IR1"]
map_masked, IR_diff, lon_subset, lat_subset = subset_center_point(IR_diff,attr['coords'][0], attr['coords'][1], 120,lon_geos,lat_geos)

#pltimshow(map_subset,cmap =pl.cm.jet_r)
#pltimshow(h08_data['IR1'],vmin =h08_data['IR1'].min() , vmax = h08_data['IR1'].max())
#pltimshow(IR_diff_2)
#pltimshow(IR_diff)



# georeference the radar data
rlon, rlat, ralt = georef_radar(attr['coords'],attr['ranges'], attr['azimuths'], attr['elevs'])
gridded_radar = grid_map(variables_da1['ZH_PIA'],lon_subset, lat_subset, attr['coords'], rlon, rlat)
gridded_radar = N.ma.masked_invalid(gridded_radar )
#mpcolormesh(gridded_radar, lon_subset, lat_subset)
#
mpcolormesh(map_subset, lon_subset, lat_subset,cmap =pl.cm.jet_r)
mpcolormesh(IR_diff_2, lon_subset, lat_subset)
mpcolormesh(IR_diff, lon_subset, lat_subset)
#,vmin =h08_data['B14'].min() , vmax =h08_data['B14'].max() )

# cmask himawari
map_subset_1 = N.ma.array(map_subset, mask = gridded_radar.mask )
IR_diff_2 = N.ma.array(IR_diff_2, mask = gridded_radar.mask )
IR_diff = N.ma.array(IR_diff, mask = gridded_radar.mask )
#mpcolormesh(map_subset_1, lon_subset, lat_subset,cmap =pl.cm.jet_r)
#mpcolormesh(IR_diff_2 , lon_subset, lat_subset,cmap =pl.cm.jet)
#mpcolormesh(IR_diff, lon_subset, lat_subset,cmap =pl.cm.jet)
#,vmin =h08_data['B14'].min() , vmax =h08_data['B14'].max() )

# lowest rainfall rate
lower_limit = zr.z2r(trafo.idecibel(gridded_radar.min()))

# scatter plot BT vs Zh
#pltscatter(map_subset_1, gridded_radar)
#plthist2d(map_subset_1, gridded_radar)
#pltscatter(IR_diff_2, gridded_radar)
#plthist2d(IR_diff_2, gridded_radar)
#pltscatter(IR_diff, gridded_radar)
#plthist2d(IR_diff, gridded_radar)