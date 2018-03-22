# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 12:47:55 2018

@author: IbarraD
"""
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean

#NCdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\NC_Data\\'
NCdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\NC_Data_Trim\\'

d0 = xr.open_dataset(NCdatadir + 'CCG_AIS_Static_Data_2017-07-01.nc')

#minlat = 41
#maxlat = 48
#minlon = -71
#maxlon = -55
minlat = 44.2
maxlat = 45.4
minlon = -63.5
maxlon = -61.1

# Create map
m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,
            llcrnrlon=minlon, urcrnrlon=maxlon,resolution='h')

# Create grid for mapping
xx,yy = m(d0['lon'].values,d0['lat'].values)

H0, xedges, yedges = np.histogram2d(d0['xgridded'].values,d0['ygridded'].values,bins=len(d0['lat']))
# Rotate and flip H...
H0 = np.rot90(H0)
H0 = np.flipud(H0)


import os
for filename in os.listdir(NCdatadir):
    if filename.endswith(".nc"):
        print(filename)
        d = xr.open_dataset(NCdatadir + filename)
        H, xedges, yedges = np.histogram2d(d['xgridded'].values,d['ygridded'].values,bins=len(d['lat']))
        # Rotate and flip H...
        H = np.rot90(H)
        H = np.flipud(H)
#        np.add(H0,H)
        H0 = H0 + H
        print(str(H0.max()))


 
# Mask zeros
Hmasked = np.ma.masked_where(H0==0,H0)
 
# Log H for better display
Hmasked = np.log10(Hmasked)
 
m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,llcrnrlon=minlon, urcrnrlon=maxlon,resolution='f')
# Make map
fig = plt.figure()
#cs = m.pcolor(xx,yy,Hmasked, cmap=plt.get_cmap('jet'),vmin=0, vmax=3.4)
cs = m.pcolor(xx,yy,Hmasked, cmap=cmocean.cm.dense,vmin=0, vmax=3.4)
#cs = m.pcolor(xx,yy,Hmasked, cmap=cmocean.cm.speed)
#cs = m.pcolor(xx,yy,Hmasked, cmap=cmocean.cm.solar_r)
m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
#plt.title('AIS Vessels density (' + str(BinNo,) + ' grid) from ' + filename)
plt.title('CCG_AIS__Data Density for 2017 (May to Nov)')
cbar = plt.colorbar(extend='both')
cbar.ax.set_xlabel('Density \n log(ships)')

