from himawari_plot_function import *
from save_cloud_mask import write_cloudmask_hdf5

import numpy as N


def pears_create_cloud_mask(h08_data,longitude, latitude, date_time,\
                            path_himawari_hdf5_out,\
                            llcrnrlon = x_ll,\
                            llcrnrlat = y_ll,\
                            urcrnrlon = x_ur,\
                            urcrnrlat = y_ur):

    #Distribute data into variables
    band_01 = h08_data["B01"]
    band_02 = h08_data["B02"]
    band_03 = h08_data["VIS"]
    band_04 = h08_data["B04"]
    
    # plot RGB
    plot_rgb_composite(band_03, band_02, band_01, longitude, latitude,\
                       date_time, " Himawari8_RGB_image", path_himawari_hdf5_out)
    # False color
    plot_rgb_composite(band_04, band_02, band_01, longitude, latitude,\
                       date_time, " Himawari8_False_color_image", path_himawari_hdf5_out)                     
    
    # plot mask
    cloud_mask2 = N.ma.masked_greater_equal(band_03, 26.26)
    plot_simple(cloud_mask2, longitude, latitude, "Reflectance", date_time,\
                "Cloud_mask", path_himawari_hdf5_out,\
                cmapp = plt.cm.get_cmap(), vmin= 0, vmax=100)
    
    # binarized mask
    bin_cloud_mask = cloud_mask2.mask
    plot_img(bin_cloud_mask, longitude, latitude, "" ,date_time, "Binarized_cloud_mask",\
             path_himawari_hdf5_out,\
             cmapp = "Greys_r", vmin= 0, vmax=1, drawcoast = True,
             llcrnrlon = llcrnrlon,\
             llcrnrlat = llcrnrlat,\
             urcrnrlon = urcrnrlon,\
             urcrnrlat = urcrnrlat)
             
    # write cloud mask
    write_cloudmask_hdf5(bin_cloud_mask, path_himawari_hdf5_out,\
                         longitude, latitude, date_time)