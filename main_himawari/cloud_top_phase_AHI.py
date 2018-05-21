# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:12:09 2017

@author: red
"""

import numpy as N
import matplotlib.pyplot as plt


def simple_plot(data, title_fig):
    plt.figure()
    img = plt.imshow( data, cmap=plt.cm.spectral)
    plt.colorbar(img)
    plt.title(title_fig)
    
def ice_water_cloud_phase(_CP_, _IR1_, plot = False):
    """ ICE vs others:
        0 : others,
        1 : Ice cloud,
        
        Water vs other:
        0 : others
        1 : others
    """
    
    _data_ = N.copy(_CP_)
    
    # Water1
    mask1 = N.ma.masked_greater(_IR1_.copy(), 285.0).mask
    mask2 = N.ma.masked_less_equal(_CP_.copy(), -0.5).mask
    
    CTP_out = N.ma.masked_array(_data_, mask = mask1 * mask2).filled(N.nan)
    
    _IR1_new = N.ma.masked_array(_IR1_, mask = mask1 * mask2).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_, mask = mask1 * mask2).filled(N.nan)
    
    #simple_plot(CTP_out, "1 : water 1")
    #print "water 1"
    #print N.shape(N.unique(CTP_out))
    
    # ice cloud
    mask9 = N.ma.masked_less_equal(_IR1_new.copy(), 238.0).mask
    mask10 = N.ma.masked_greater_equal(_CP_new.copy(), 0.5).mask
    
    CTP_out= N.ma.masked_array(CTP_out, mask = N.ma.mask_or(mask9, mask10)).filled(1)
    
    _IR1_new = N.ma.masked_array(_IR1_new, mask = N.ma.mask_or(mask9, mask10)).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_new, mask = N.ma.mask_or(mask9, mask10)).filled(N.nan)
    
    #simple_plot(CTP_out, "5 : ice")

    
    # final mask (uncertain2)
    mask11 = ~(N.ma.masked_invalid(_IR1_new.copy()).mask)
    CTP_out = N.ma.masked_array(CTP_out, mask = mask11).filled(N.nan)
    
    
    
    CTP_out_mask = N.ma.masked_invalid(CTP_out).mask
    CTP_water = N.ma.masked_array(N.array(CTP_out_mask,  dtype=int), mask = mask1 * mask2).filled(0)
    CTP_ice = N.ma.masked_invalid(CTP_out).filled(0)
    
    if plot == True:
        simple_plot(CTP_ice, "ice vs. others")
        simple_plot(CTP_water, "water vs. others")
        
    return CTP_ice , CTP_water
    

def cloud_top_phase(_CP_, _IR1_ , plot = False):
    """ 0 : water cloud,
        1 : Ice cloud,
        3 : Uncertain
        2 : Mixed cloud """
    
    _data_ = N.copy(_CP_)
    
    # Water1
    mask1 = N.ma.masked_greater(_IR1_.copy(), 285.0).mask
    mask2 = N.ma.masked_less_equal(_CP_.copy(), -0.5).mask
    
    CTP_out = N.ma.masked_array(_data_, mask = mask1 * mask2).filled(N.nan)
    
    _IR1_new = N.ma.masked_array(_IR1_, mask = mask1 * mask2).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_, mask = mask1 * mask2).filled(N.nan)
    
    #water2
    mask3 = N.ma.masked_greater(_IR1_new.copy(), 238.0).mask
    mask4 = N.ma.masked_less(_CP_new.copy(), -1.0).mask
    
    CTP_out= N.ma.masked_array(CTP_out, mask = mask3 * mask4).filled(0)
    
    _IR1_new = N.ma.masked_array(_IR1_new, mask = mask3 * mask4).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_new, mask = mask3 * mask4).filled(N.nan)
    
    #uncertain1
    mask5 = N.ma.masked_less(_IR1_new.copy(), 268.0).mask * N.ma.masked_greater(_IR1_new.copy(), 238.0).mask
    mask6 = N.ma.masked_greater_equal(_CP_new.copy(), -1.0).mask * N.ma.masked_less(_CP_new.copy(), -0.25).mask
    
    
    CTP_out= N.ma.masked_array(CTP_out, mask = mask5 * mask6).filled(3)
    
    _IR1_new = N.ma.masked_array(_IR1_new, mask = mask5 * mask6).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_new, mask = mask5 * mask6).filled(N.nan)
    

    # mixed cloud
    mask7 = N.ma.masked_less(_IR1_new.copy(), 268).mask * N.ma.masked_greater(_IR1_new.copy(), 238).mask
    mask8 = N.ma.masked_greater_equal(_CP_new.copy(), -0.25 ).mask * N.ma.masked_less(_CP_new.copy(), 0.5).mask
    
    CTP_out= N.ma.masked_array(CTP_out, mask = mask7 * mask8).filled(2)
    
    _IR1_new = N.ma.masked_array(_IR1_new, mask = mask7 * mask8).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_new, mask = mask7 * mask8).filled(N.nan)
    

    # ice cloud
    mask9 = N.ma.masked_less_equal(_IR1_new.copy(), 238.0).mask
    mask10 = N.ma.masked_greater_equal(_CP_new.copy(), 0.5).mask
    
    CTP_out= N.ma.masked_array(CTP_out, mask = N.ma.mask_or(mask9, mask10)).filled(1)
    
    _IR1_new = N.ma.masked_array(_IR1_new, mask = N.ma.mask_or(mask9, mask10)).filled(N.nan)
    _CP_new = N.ma.masked_array(_CP_new, mask = N.ma.mask_or(mask9, mask10)).filled(N.nan)
    

    # final mask (uncertain2)
    mask11 = ~(N.ma.masked_invalid(_IR1_new.copy()).mask)
    CTP_out= N.ma.masked_array(CTP_out, mask = mask11).filled(3)
    
    if plot == True:
        simple_plot(CTP_out, "6 : final")
    return CTP_out
    