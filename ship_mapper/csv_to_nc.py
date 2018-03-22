# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 09:02:20 2018

@author: IbarraD
"""
import pandas as pd
import numpy as np
import xarray as xr
import os
import time


Ddatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\Dynamic_Data\\'
Sdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\Static_Data\\'
NCdatadir = 'C:\\Users\\IbarraD\\Documents\\AIS_data_Angelia\\NC_Data\\'


for file in os.listdir(Ddatadir):
    
    dateName = file[21:-4]
    Dfilename = Ddatadir + 'CCG_AIS_Dynamic_Data_' + dateName + '.csv'
    Sfilename = Sdatadir + 'CCG_AIS_Static_Data_' + dateName + '.csv'
    NCfilename= NCdatadir + 'CCG_AIS_Static_Data_' + dateName + '.nc'

    print(Dfilename)
    t0 = time.time()
    csv = pd.read_table(Dfilename, sep=',')
    #csvS = pd.read_table(Sfilename, sep=',')
    
    
    D = xr.Dataset({'Region':(['Dindex'],csv['Region']),
                    'Station_Location':(['Dindex'],csv['Station_Location']),
                    'AIS_Channel':(['Dindex'],csv['AIS_Channel']),
                    'year':(['Dindex'],csv['year']),
                    'month':(['Dindex'],csv['month']),
                    'day':(['Dindex'],csv['day']),
                    'hour':(['Dindex'],csv['hour']),
                    'minute':(['Dindex'],csv['minute']),
                    'second':(['Dindex'],csv['second']),
                    'TimeZone':(['Dindex'],csv['TimeZone']),
                    'ID':(['Dindex'],csv['ID']),
                    'AIS_Class':(['Dindex'],csv['AIS_Class']),
                    'Message_Type':(['Dindex'],csv['Message_Type']),
                    'Repeat_Indicator':(['Dindex'],csv['Repeat_Indicator']),
                    'MMSI':(['Dindex'],csv['MMSI']),
                    'Speed_Over_Ground_SOG_knots':(['Dindex'],csv['Speed_Over_Ground_SOG_knots']),
                    'Position_Accuracy':(['Dindex'],csv['Position_Accuracy']),
                    'Longitude_decimal_degrees':(['Dindex'],csv['Longitude_decimal_degrees']),
                    'Latitude_decimal_degrees':(['Dindex'],csv['Latitude_decimal_degrees']),
                    'Course_Over_Ground_COG_degrees':(['Dindex'],csv['Course_Over_Ground_COG_degrees']),
                    'True_heading_HDG_degrees':(['Dindex'],csv['True_heading_HDG_degrees']),
                    'Navigation_Status':(['Dindex'],csv['Navigation_Status']),
                    'TimeStamp_s':(['Dindex'],csv['TimeStamp_s'])},
                coords={'Dindex':(['Dindex'],csv.index)})
    
    
    encoding = {}
    encoding = {'Region':{'dtype':'S1','zlib':True},
                'Station_Location':{'zlib':True},
                'AIS_Channel':{'dtype':'S1','zlib':True},
                'year':{'zlib':True},
                'month':{'zlib':True},
                'day':{'zlib':True},
                'minute':{'zlib':True},
                'second':{'zlib':True},
                'TimeZone':{'dtype':'S3','zlib':True},
                'AIS_Class':{'dtype':'S1','zlib':True},
                'Message_Type':{'zlib':True},
                'Repeat_Indicator':{'zlib':True},
                'MMSI':{'zlib':True},
                'Speed_Over_Ground_SOG_knots':{'zlib':True},
                'Position_Accuracy':{'zlib':True},
                'Longitude_decimal_degrees':{'zlib':True},
                'Latitude_decimal_degrees':{'zlib':True},
                'Course_Over_Ground_COG_degrees':{'zlib':True},
                'True_heading_HDG_degrees':{'zlib':True},
                'Navigation_Status':{'zlib':True},
                'TimeStamp_s':{'zlib':True}}
    
    D.to_netcdf(NCfilename,format='NETCDF4',engine='netcdf4',encoding=encoding)
    
    t1 = time.time()
    print(str((t1-t0)/60))
