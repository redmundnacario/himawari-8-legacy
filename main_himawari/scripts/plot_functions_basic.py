# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 12:30:40 2015

@author: red
"""

import sys
sys.path.insert(0, '/media/red/SAMSUNG/main/main_radar')
from radar_functions_plot import *

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import cm

from matplotlib import colors
from pylab import *
import datetime
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
import pylab as pl

def pltimshow(data_,cmap = None, vmin=None ,vmax=None):
    plt.figure()
    plt.imshow(data_,cmap=cmap, vmin =vmin, vmax = vmax)
    plt.colorbar(shrink = 0.95)

def mpcolormesh(data_, lon, lat, cmap=None,vmin=None ,vmax=None):  
    plt.figure()
    m =create_basemap()
    m.pcolormesh(lon, lat,data_,cmap=cmap,vmin =vmin, vmax = vmax)
    cb = colorbar()
   
def pltscatter(data_x, data_y):
    plt.figure()
    x = data_x.ravel()
    y = data_y.ravel()
    x1 = N.ma.compressed(x)
    y1 = N.ma.compressed(y)
    plt.scatter(x1, y1, alpha=0.5)

def plthist2d(data_x, data_y):
    plt.figure()
    x = data_x.ravel()
    y = data_y.ravel()
    x1 = N.ma.compressed(x)
    y1 = N.ma.compressed(y)
    plt.hist2d(x1,y1, (50, 50), cmap = cm.gist_heat_r)
    plt.colorbar(shrink = 0.95)