# -*- coding: utf-8 -*-
"""
Constant values/intial values
Created on Wed Nov 18 11:51:41 2015

@author: red
"""
import numpy as N
import pyproj
import os

# directories
#path_input ='/home/red/Desktop/remote_sensing_project/ty_lando/files/20151018/standard_format'
#path_input ='/media/red/SAMSUNG/himawari/thunderstorm/case1'
#path_ouput = '/media/red/SAMSUNG/himawari/ty_lando/'
#path_output = '/media/red/SAMSUNG/himawari/thunderstorm'
# directory of Himawari-8.cfg file
def get_dir_this_script():
    dir_script = os.path.dirname(os.path.realpath(__file__))
    return dir_script

#path_cfg = '/home/red/pytroll/mpop-pre-master/etc/himawari'
path_cfg = os.path.join(get_dir_this_script(),"config_files/himawari")
#print path_cfg

os.environ["PPP_CONFIG_DIR"] = path_cfg

# lists
segments = N.array(["03","04","05"])# used in data_extracion.py
segmentsb = N.array(["3","4","5"])# used in data_extraction.py

dat_list = N.array(["B01","B02","B03","B04","B05","B06","B07","B08","B09",\
                    "B10","B11","B12","B13","B14","B15","B16"])
dat_list_reso =N.array(["R10","R10","R05","R10","R20","R20","R20","R20","R20",\
                    "R20","R20","R20","R20","R20","R20","R20"]) 
dat_segment = N.array(["03","04","05"])
                    
dat_listnum = N.array(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16"])

# VIS and NIR Bands
dat_lista = N.array(["B01","B02","B03","B04","B05","B06"])
dat_listnuma = N.array(["1","2","3","4","5","6"])
# IR bands
dat_listb = N.array(["B07","B08","B09","B10","B11","B12","B13","B14","B15","B16"])
dat_listnumb = N.array(["7","8","9","10","11","12","13","14","15","16"])

hrit_list = N.array(["B01","B02","VIS","B04","B05","B06","IR4","IR3","B09",\
                    "B10","B11","B12","IR1","B14","IR2","B16"])# official use
                    
# used in data_extraction.py
hrit_listb = ["B01","B02","VIS","B04","B05","B06","IR4","IR3","B09",\
                    "B10","B11","B12","IR1","B14","IR2","B16"]# official use
                    
                    
hrit_spa = N.array(["B01","B02","VIS","B04","B05","B06"])
hrit_spb = N.array(["IR4","IR3","B09","B10","B11","B12","IR1","B14","IR2","B16"])

constant_a = ['coeff_rad2albedo_conversion']
constant_b = ['c0_rad2tb_conversion', 'c1_rad2tb_conversion','c2_rad2tb_conversion',\
    'c0_tb2rad_conversion','c1_tb2rad_conversion','c2_tb2rad_conversion',\
    'speed_of_light', 'planck_constant','boltzmann_constant']

                    
# dictionaries
                    
# get ROI
#HS_proj = pyproj.Proj("+proj=geos +lon_0=123 +a=6378137.0 +b=6356752.3 +h=42164000.0")
HS_proj = pyproj.Proj("+proj=geos +a=6378169.00 +b=6356583.80 +h=35785831.0 +lon_0=140.7")
x_ll = 115.0
y_ll = 5.0
x_ur = 130.0
y_ur = 23
x1,y1= HS_proj(x_ll,y_ll)
x2,y2 = HS_proj(x_ur,y_ur)

#c0_rad2tb = sample_data._header[num]["calibration"]['c0_rad2tb_conversion'][0]
#c1_rad2tb = sample_data._header[num]["calibration"]['c1_rad2tb_conversion'][0]
#c2_rad2tb = sample_data._header[num]["calibration"]['c2_rad2tb_conversion'][0]
#c0_tb2rad = sample_data._header[num]["calibration"]['c0_tb2rad_conversion'][0]
#c1_tb2rad = sample_data._header[num]["calibration"]['c1_tb2rad_conversion'][0]
#c2_tb2rad = sample_data._header[num]["calibration"]['c2_tb2rad_conversion'][0]
#c = sample_data._header[num]["calibration"]['speed_of_light'][0]
#planck_c = sample_data._header[num]["calibration"]['planck_constant'][0]
#b_z = sample_data._header[num]["calibration"]['boltzmann_constant'][0]
