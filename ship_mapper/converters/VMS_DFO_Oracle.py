"""
This is a csv to nc converter for VMS data
"""
import pandas as pd
import numpy as np
import datetime
import xarray as xr
import yaml

import ship_mapper as sm

def convert(file_in, file_out, data_info_file):
    '''
    test
    '''
    #Load data
    print(file_in)
    data = pd.read_csv(file_in, sep=',')
    
    
    # Chores: Create empty lists and counters
    DateTime_list = []
    DateFlag_list = []
    SeqNum_list = []
    error = 0
    originTime = datetime.datetime.strptime('1/1/1980 00:00',"%m/%d/%Y %H:%M")
    
    #Check date-strings and calculate "serial-date" (i.e. SeqNum)
    for i in range(0,len(data)):
        try:
            DateTime_list.append(datetime.datetime.strptime(data['POSITION_UTC_DATE'].values[i],"%Y-%m-%d %H:%M:%S"))
            SeqNum_list.append(sm.elapsed_days(DateTime_list[-1]-originTime))

        except ValueError:
            DateTime_list.append(np.nan)   
            SeqNum_list.append(np.nan)
            DateFlag_list.append(0)
            error += 1


    print('error = ' + str(error))
    
    # Add new columns to DataFrame
    data['DateTime'] = pd.Series(DateTime_list)
    data['SeqNum'] = pd.Series(SeqNum_list)
    data['DateFlag'] = pd.Series(DateFlag_list)

    
    
    # STAGE 2 - Calculate Apparent Speed
    data['AppSpeed'] = np.nan
    data.sort_values(by=['SeqNum'],inplace=True)
    data = data.reset_index(drop=True)
    
    # Chores: create empty lists
    VRN = []
    LATITUDE = []
    LONGITUDE = []
    POSITION_UTC_DATE = []
    DateTime = []
    SeqNum = []
    DateFlag = []
    ElapsedDistance = []
    ElapsedDays = []
    ApparentSpeed = []
    
    
    # Find unique ships
    unis = pd.unique(data['VR_NUMBER'])
    print('Number of Unique Ships = ' + str(len(unis)))
    
    # Loop over each ship
    counter = 0
    for ship in unis:
        counter += 1
        print('Ship: ' + str(counter) + '('+ str(ship) + ')')
        singleship = data[data['VR_NUMBER'] == ship]
    
        # Note that the first point of each ship is not counted
        for i in range(1,len(singleship)):
            
            # Don't process ship track with only one point 
            if len(singleship) > 1:
                idx1 = singleship.index[i-1]
                idx2 = singleship.index[i]
                
                # Time
                DateTime.append(data['DateTime'][idx2])
                ElapsedDays.append(sm.elapsed_days(DateTime[-1]-data['DateTime'][idx1]))
                
                # Get lat/lons
                lon1 = singleship['LONGITUDE'][idx1]
                lat1 = singleship['LATITUDE'][idx1]
                lon2 = singleship['LONGITUDE'][idx2]
                lat2 = singleship['LATITUDE'][idx2]
                                
                # Estimate elapsed distance and apperent speed
                ElapsedDistance.append(sm.distance(lat1,lon1,lat2,lon2))
                if ElapsedDays[-1] > 0:
                    ApparentSpeed.append(sm.estimate_velocity(ElapsedDays[-1] * 86400, ElapsedDistance[-1]))
                else:
                    ApparentSpeed.append(np.nan)
    
                # Done! Append extra information to lists
                VRN.append(int(singleship['VR_NUMBER'][idx2]))
                LATITUDE.append(singleship['LATITUDE'][idx2])
                LONGITUDE.append(singleship['LONGITUDE'][idx2])
                POSITION_UTC_DATE.append(singleship['POSITION_UTC_DATE'][idx2])
                SeqNum.append(singleship['SeqNum'][idx2])
                DateFlag.append(singleship['DateFlag'][idx2])
                
    dinfo = yaml.load(open(data_info_file, 'r'))
    
    D = xr.Dataset({'ship_id_vrn':(['Dindex'],VRN),
                    'latitude':(['Dindex'],LATITUDE),
                    'longitude':(['Dindex'],LONGITUDE),
                    'DateTime':(['Dindex'],DateTime),
                    'SeqNum':(['Dindex'],SeqNum),
                    'ApparentSpeed':(['Dindex'],ApparentSpeed)},

                coords={'Dindex':(['Dindex'],pd.Series(VRN).index)},
                attrs=dinfo)
    
    
    encoding = {}
    encoding = {'ship_id_vrn':{'zlib':True},
                'latitude':{'zlib':True},
                'longitude':{'zlib':True},
                'DateTime':{'zlib':True},
                'SeqNum':{'zlib':True},
                'ApparentSpeed':{'zlib':True}}
    
    D.to_netcdf(file_out,format='NETCDF4',engine='netcdf4',encoding=encoding)
    
    
    
    print('Good!')
    return









