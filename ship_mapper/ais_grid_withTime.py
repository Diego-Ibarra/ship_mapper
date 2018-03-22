# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 08:50:32 2018

@author: IbarraD
"""

import pandas as pd
import numpy as np
import xarray as xr
import vms
import AIS_map as mapper
import time
import os
from datetime import datetime

Ddatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\Dynamic_Data\\'
Sdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\Static_Data\\'
NCdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\NC_Data_TimeBinned\\'
NCtrimdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\NC_Data_Trim\\'
PNGdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\PNGs\\'

minlat = 44.2
maxlat = 45.4
minlon = -63.5
maxlon = -61.1

lat_bnds, lon_bnds = [minlat,maxlat], [minlon,maxlon]

BinNo = 1000

#for day in range(1,2):
#for day in range(1,10):
for file in os.listdir(Ddatadir):
    
    file = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\Dynamic_Data\\CCG_AIS_Dynamic_Data_2017-12-31.csv'
    
    dateName = file[21:-4]
        
    Dfilename = 'CCG_AIS_Dynamic_Data_' + dateName + '.csv'
    Sfilename = 'CCG_AIS_Static_Data_' + dateName + '.csv'
    NCfilename = 'CCG_AIS_Static_Data_' + dateName + '.nc'
    
    fullname = NCdatadir + NCfilename
    
    print(fullname)

    D = xr.open_dataset(fullname)

    indx = ((D['Longitude_decimal_degrees']>  minlon) &
            (D['Longitude_decimal_degrees']<= maxlon) &
            (D['Latitude_decimal_degrees']>  minlat) &
            (D['Latitude_decimal_degrees']<= maxlat))
    
    
    Dtrim = D.sel(Dindex=indx)
    
    # Find unique ships
    unis = np.unique(D['MMSI'][indx].values)
    print('Number of Unique Ships = ' + str(len(unis)))

    # Make grid
    x = np.linspace(minlon, maxlon, num=BinNo)
    y = np.linspace(minlat, maxlat, num=BinNo)
    
    iix, iiy = [], []
    counter = 0
    for ship in unis:
#    for ship in [unis[385],]:
        counter += 1
        print('Ship: ' + str(counter) + '('+ str(ship) + ')')
        singleship = Dtrim.sel(Dindex=(Dtrim['MMSI'] == ship))
        pings = len(singleship.Dindex)
        
        charar = np.chararray((1, pings))
        charar[:] = '-'
        
        
#        year1 = np.char.array(singleship['year'].values) + \
#                charar + \
#                np.char.array(singleship['month'].values) + \
#                charar + \
#                np.char.array(singleship['day'].values) + \
#                charar + \
#                np.char.array(singleship['hour'].values) + \
#                charar + \
#                np.char.array(singleship['minute'].values) + \
#                charar + \
#                np.char.array(singleship['second'].values)            
#                
#        d = pd.to_datetime(pd.Series(year1[0]))
#                
#        year2 = singleship['year'].values[-1]
#        month1 = singleship['month'].values[0]
#        month2 = singleship['month'].values[-1]
#        day1 = singleship['day'].values[0]
#        day2 = singleship['day'].values[-1]
#        year1 = singleship['year'].values[0]
#        year2 = singleship['year'].values[-1]
#        year1 = singleship['year'].values[0]
#        year2 = singleship['year'].values[-1]
        
        df = pd.DataFrame({'year':singleship['year'].values,
                           'month':singleship['month'].values,
                           'day':singleship['day'].values,
                           'hour':singleship['hour'].values,
                           'minute':singleship['minute'].values,
                           'second':singleship['second'].values})
    
        time1 = pd.to_datetime(df)
    
        # Loop over each ship
        for i in range(1,pings):
            if pings > 1:
                
                timeStamp = pd.to_datetime(singleship['year'].values,
                                     singleship['month'].values,
                                     singleship['day'].values,
                                     singleship['hour'].values,
                                     singleship['minute'].values,
                                     singleship['second'].values)
                
                # Iterpolate bewtween known points
                lon1 = singleship['Longitude_decimal_degrees'].values[i-1]
                lat1 = singleship['Latitude_decimal_degrees'].values[i-1]
                lon2 = singleship['Longitude_decimal_degrees'].values[i]
                lat2 = singleship['Latitude_decimal_degrees'].values[i]
                
                distance = vms.distance(lat1,lon1,lat2,lon2)
                
                if distance < 5000: #meters
                    x1, y1 = vms.align_with_grid(x, y, lon1, lat1)
                    x2, y2 = vms.align_with_grid(x, y, lon2, lat2)
                    
                    ix, iy = vms.interp2d(x1, y1, x2, y2)
                    iix.extend(ix)
                    iiy.extend(iy)


            # add the last location 
            xend, yend = vms.align_with_grid(x, y,
                                             singleship['Longitude_decimal_degrees'].values[i],
                                             singleship['Latitude_decimal_degrees'].values[i])
            iix.append(xend)
            iiy.append(yend)
            
    # Save to nc file
    d = xr.Dataset({'xgridded':(['No_of_points'],iix),
                    'ygridded':(['No_of_points'],iiy)},
                    coords={'lon':(['grid_length'],x),
                            'lat':(['grid_length'],y)})
    
    d.to_netcdf(path=NCtrimdatadir + NCfilename)

