# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:10:46 2015

@author: red
"""
import numpy as N
import datetime
import os

from himawari_var import *
from mpl_toolkits.basemap import Basemap
import matplotlib as matplot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from custom_cmap import *


def str_date2_object(date_time):
    date_time = datetime.datetime.strptime(date_time, "%Y%m%d_%H%M")
    return date_time

def plot_img(_data_, lon, lat, label, date_time, title , path,\
             cmapp = plt.cm.get_cmap(), vmin= 0, vmax=100, drawcoast = True,\
             click = False,  n_click = 3,\
             llcrnrlon = 112, llcrnrlat = 4, urcrnrlon = 132, urcrnrlat = 24):
    """
    Plots image data in a map with vmin as equal to 0 and vmax equal to 100
    """
    plt.figure(dpi = 300)
    m = Basemap(projection='merc',resolution = 'i',\
                llcrnrlon = llcrnrlon,\
                llcrnrlat = llcrnrlat,\
                urcrnrlon = urcrnrlon,\
                urcrnrlat = urcrnrlat)
                
    if drawcoast == True:
        m.drawcoastlines(linewidth=0.01,color = 'yellow',antialiased=0)
    m.drawparallels(N.arange(0,26, 5),labels= [1,0,0,0,],size = 10, zorder= -10)
    m.drawmeridians(N.arange(110,136,5), labels=[0,0,0,1], size = 10, zorder = -10)
    
    m.pcolormesh(lon,lat, _data_, latlon=True,vmin= vmin, vmax=vmax, cmap=cmapp)
    cb = plt.colorbar(shrink = 0.95)
    cb.set_label(label)
    plt.xlabel("\nLongitude")
    plt.ylabel("Latitude\n\n")
    
    date_time1 = str_date2_object(date_time)
    plt.title(title+": "+str(date_time1)+"\n")
    #plt.show()
    plt.savefig(path+'/'+title+"_"+date_time+".png",bbox_inches = None)
    #plt.close()
    
    if click == True:
        print "please click "+str(n_click)+"x some where in the image"
        pts = plt.ginput(n_click)
        print pts
        x = map(lambda x: x[0] ,pts)
        y = map(lambda y: y[1] ,pts)
        plt.plot(x,y,"o")
        return pts
    
def plot_img_diff(_data_, lon, lat, label, date_time,\
                  title, path, cmapp = plt.cm.get_cmap(),\
                  llcrnrlon = 112, llcrnrlat = 4, urcrnrlon = 132, urcrnrlat = 24):
    """
    Plots image diff
    """
    plt.figure(dpi = 300)
    
    m = Basemap(projection='merc',resolution = 'i',\
                llcrnrlon = llcrnrlon,\
                llcrnrlat = llcrnrlat,\
                urcrnrlon = urcrnrlon,\
                urcrnrlat = urcrnrlat)
                
    m.drawcoastlines(linewidth=0.01,color = 'yellow',antialiased=0)
    m.drawparallels(N.arange(0,26, 5),labels= [1,0,0,0,],size = 10, zorder= -10)
    m.drawmeridians(N.arange(110,136,5), labels=[0,0,0,1], size = 10, zorder = -10)
    
    m.pcolormesh(lon,lat, _data_, latlon = True,\
                 cmap=cmapp,vmin= -(_data_.max()), vmax=_data_.max())
                 
    cb = plt.colorbar(shrink = 0.95)
    cb.set_label(label)
    plt.xlabel("\nLongitude")
    plt.ylabel("Latitude\n\n")
    
    date_time1 = str_date2_object(date_time)
    plt.title(title+": "+str(date_time1)+"\n")
    #m.show()
    plt.savefig(path+'/'+title+"_"+date_time+".png",bbox_inches = None)
    #plt.close()

def plot_rgb_composite(r_data, g_data, b_data, lon, lat, date_time, title,\
                       path, click = False, n_click = 3):
    """
    Plots RGB composite data
    """
    plt.figure(dpi = 300)
    RGB = N.zeros((r_data.shape[0], r_data.shape[1], 3))
    RGB[:,:,0]=  r_data /100
    RGB[:,:,1] = g_data /100
    RGB[:,:,2] = b_data /100
    
    plt.imshow(RGB)
    
    date_time1 = str_date2_object(date_time)
    plt.title(title+": "+str(date_time1)+"\n")
    #plt.show()
    plt.savefig(path+'/'+title+"_"+date_time+".png",bbox_inches = None)
    #plt.close()
    
    if click == True:
        print "please click "+str(n_click)+"x some where in the image"
        pts = plt.ginput(n_click)
        print pts
        x = map(lambda x: x[0] ,pts)
        y = map(lambda y: y[1] ,pts)
        plt.plot(x,y,"o", color = "r")
        return N.array(N.around(N.array(pts)), dtype = N.int)
        
def plot_n_convert_rgb_to_hsv(r_data, g_data, b_data, lon, lat,\
                              date_time, path, plot = False):
    """
    Plots and convert RGB data into HSV
    return HSV data
    """
    
    RGB = N.zeros((r_data.shape[0], r_data.shape[1], 3))
    RGB[:,:,0]=  r_data /100
    RGB[:,:,1] = g_data /100
    RGB[:,:,2] = b_data /100
    
    # convert RGB to HSV
    HSV = matplot.colors.rgb_to_hsv(RGB)
    
    if plot == True:
        # plots hue (different colors)
        plot_img(HSV[:,:,0], lon, lat, "Intensity", date_time, "Hue" , path,\
                cmapp = "jet_r", vmin=0, vmax=1, drawcoast = False)
        # plots Saturation (how dark or light)
        plot_img(HSV[:,:,1], lon, lat, "Intensity",  date_time, "Saturation" , path,\
                 cmapp = "gray_r",\
                 vmin=0, vmax=1, drawcoast = False)             
        # plots Value (white or black)
        plot_img(HSV[:,:,2], lon, lat, "Intensity",  date_time, "Value" , path,\
                 cmapp = "gray",\
                 vmin=0, vmax=1, drawcoast = False)
    return HSV

def plot_simple(_data_, lon, lat, label, date_time, title, path,\
                cmapp = plt.cm.get_cmap(), vmin= 0, vmax=1,\
                click = False, n_click = 3):
    """
    Plots RGB composite data
    """
    plt.figure(dpi = 100)
    plt.imshow(_data_, vmin = vmin, vmax = vmax, cmap = cmapp)
    cb = plt.colorbar(shrink = 0.95)
    cb.set_label(label)
    
    date_time1 = str_date2_object(date_time)
    plt.title(title+": "+str(date_time1)+"\n")
    #plt.show()
    plt.savefig(path+'/'+title+"_"+date_time+".png",bbox_inches = None)
    #plt.close()
    
    if click == True:
        print "please click "+str(n_click)+"x some where in the image"
        pts = plt.ginput(n_click)
        print pts
        x = map(lambda x: x[0] ,pts)
        y = map(lambda y: y[1] ,pts)
        plt.plot(x,y,"o", color = "r")
        return N.array(N.around(N.array(pts)), dtype = N.int)

def scene_selection(_r_data_, _g_data_, _b_data_, longitude, latitude,\
                   date_time, path, n_click = 5):
    
    pts = plot_rgb_composite(_r_data_, _g_data_, _b_data_, longitude, latitude,\
                             date_time, "RGB",\
                             path, click = True, n_click = n_click )
                             
    N.savetxt(os.path.join(path,"center_points.txt"),\
              pts, fmt = "%s", delimiter = "\t")
    return pts

def plot_histogram(_data_, label, date_time, title, path, bins = 20,\
                   style = "line"):
    plt.figure()
    if style == "bar":
        ny, bins_value, pathces = plt.hist(_data_.ravel(), bins = bins,\
                                      histtype = "stepfilled", alpha = 0.5)
    elif style  == "line":
        ny, binEdges = N.histogram(_data_.ravel(), bins = bins)
        bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
        plt.plot(bincenters, ny, "r-", linewidth = 2.5)
        
    plt.title(title+": "+ date_time +"\n")
    plt.xlabel("\n"+label)
    plt.ylabel("Frequency\n")
    #plt.savefig(path+'/'+title+"_"+date_time+"_histogram.png",\
    #            bbox_inches = None)
    #return ny, bins_value, pathces

def plot_mltpl_hist(_data_, label, date_time, title, path, bins = 20,\
                    style = "line"):
    """
    Plots multiple histograms of same data variable with same timestamps but
    with different spatial domains
    
    Input:
    _data_          Data of the same variable  
    bins = 20       No of bins in a histogram
    label           "list of strings"
    date_time       "string"
    title           "string"
    
    Output:
    plots of histograms
    """
    color  = ["b","r","g","c", "m", "y"]
    ###
    plt.figure()
    for i in xrange(N.shape(_data_)[0]):
        if style == "bar":
            plt.hist(_data_[i].ravel(), bins = bins,\
                     histtype = "stepfilled", alpha = 0.3, label = label[i],
                     color = color[i])
        elif style  == "line":
            ny, binEdges = N.histogram(_data_[i].ravel(), bins = bins)
            bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
            plt.plot(bincenters, ny, color = color[i], linewidth = 2.5,\
                     alpha =0.5, label = label[i])
    plt.title(title+": "+ date_time +"\n")
    plt.xlabel("\nValue")
    plt.ylabel("Frequency\n")
    plt.legend()
    #plt.savefig(path+'/'+title+"_"+date_time+"_mltpl_histogram.png",\
    #            bbox_inches = None)

        
    
def plot_img_new(_data_, lon, lat, label, date_time, title , path,\
             cmapp = plt.cm.get_cmap(), vmin= 0, vmax=100, drawcoast = True,\
             click = False,  n_click = 3,\
             llcrnrlon = 112, llcrnrlat = 4, urcrnrlon = 132, urcrnrlat = 24):
    """
    Plots image data in a map with vmin as equal to 0 and vmax equal to 100
    """
    plt.figure(dpi = 300)
    m = Basemap(projection='stere',resolution = 'i',\
                llcrnrlon = llcrnrlon,\
                llcrnrlat = llcrnrlat,\
                urcrnrlon = urcrnrlon,\
                urcrnrlat = urcrnrlat,
                lon_0 = 135,\
                lat_0 = 90)
                
    if drawcoast == True:
        m.drawcoastlines(linewidth=0.01,color = 'yellow',antialiased=0)
    m.drawparallels(N.arange(0,60, 10),labels= [1,0,0,0,],size = 10, zorder= 2, color = "gray", alpha = 0.3)
    m.drawmeridians(N.arange(110,200,10), labels=[0,0,0,1], size = 10, zorder = 2,color = "gray", alpha= 0.3)
    
    m.pcolormesh(lon,lat, _data_, latlon=True,vmin= vmin, vmax=vmax, cmap=cmapp)
    cb = plt.colorbar(shrink = 0.65)
    cb.set_label(label)
    plt.xlabel("\nLongitude")
    plt.ylabel("Latitude\n\n")
    
    date_time1 = str_date2_object(date_time)
    plt.title(title+": "+str(date_time1)+"\n")
    #plt.show()
    plt.savefig(path+'/'+title+"_"+date_time+".png",bbox_inches = None)
    #plt.close()
    
    if click == True:
        print "please click "+str(n_click)+"x some where in the image"
        pts = plt.ginput(n_click)
        print pts
        x = map(lambda x: x[0] ,pts)
        y = map(lambda y: y[1] ,pts)
        plt.plot(x,y,"o")
        return pts
        
        

def grayify_cmap(cmap):
    """Return a grayscale version of the colormap"""
    # CODE FROM:
    # https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/
    # The function will tranform any colormap into a grayscale version of it.
    
    cmap = plt.cm.get_cmap(cmap)
    colors_i = N.linspace(0, 1., 100)
    colors=cmap(colors_i)

    # convert RGBA to perceived greyscale luminance
    # cf. http://alienryderflex.com/hsp.html
    RGB_weight = [0.299, 0.587, 0.114]
    luminance = N.sqrt(N.dot(colors[:, :3] ** 2, RGB_weight))
    Num=100
    rgb=N.zeros((3,Num,3))
    for n in range(3):
        rgb[n,:,0] = N.linspace(0,1,Num)
        rgb[n,:,1] = luminance
        rgb[n,:,2] = luminance
    k=['red', 'green', 'blue']
    data=dict(zip(k,rgb)) 
    my_cmap = matplot.colors.LinearSegmentedColormap("grayify",data)
    return my_cmap
        