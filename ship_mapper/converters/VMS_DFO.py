import pandas as pd
import numpy as np
import datetime
import xarray as xr
import yaml

import ship_mapper as sm

def convert(file_in, file_out, data_info_file):
    '''
    This is a csv to nc converter for VMS data
    
    :param str file_in: Input file (.csv)
    
    :param str file_out: Output file (.nc)
    
    :param str data_info_file: YAML file describing other conversion parameters (.yml)
    
    :return: A netCDF file (.nc) in a format standard for "ship_mapper" 
             containing the original data, but also containing metadata included in the data_info.yml file
    '''
    #Load data
    data = pd.read_html(file_in)[0]
    new_header = data.iloc[0]
    data = data[1:] #take the data less the header row
    data.columns = new_header #set the header row as the df header
    
    data.LONGITUDE = data.LONGITUDE.astype(float)
    data.LATITUDE = data.LATITUDE.astype(float)
    
    
    # Chores: Create empty lists and counters
    DateTime_list = []
    DateFlag_list = []
    SeqNum_list = []
    error = 0
    originTime = datetime.datetime.strptime('1/1/1980 00:00',"%m/%d/%Y %H:%M")
    
    #Check date-strings and calculate "serial-date" (i.e. SeqNum)
    for i in range(0,len(data)):
        try:
            DateTime_list.append(datetime.datetime.strptime(data['POSITION DATE (UTC)'].values[i],"%b %d %Y %H:%M %Z"))
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
    SPEED_KNOTS = []
    DateTime = []
    SeqNum = []
    DateFlag = []
    ElapsedDistance = []
    ElapsedDays = []
    ApparentSpeed = []
    
    
    # Find unique ships
    unis = pd.unique(data['VESSEL VRN'])
    print('Number of Unique Ships = ' + str(len(unis)))
    
    # Loop over each ship
    counter = 0
    for ship in unis:
        counter += 1
        print('Ship: ' + str(counter) + '('+ str(ship) + ')')
        singleship = data[data['VESSEL VRN'] == ship]
    
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
                VRN.append(int(singleship['VESSEL VRN'][idx2]))
                LATITUDE.append(singleship['LATITUDE'][idx2])
                LONGITUDE.append(singleship['LONGITUDE'][idx2])
                POSITION_UTC_DATE.append(singleship['POSITION DATE (UTC)'][idx2])
                SPEED_KNOTS.append(singleship['SPEED (KNOTS)'][idx2])
                SeqNum.append(singleship['SeqNum'][idx2])
                DateFlag.append(singleship['DateFlag'][idx2])
                


    # Metadata
    dinfo = yaml.load(open(data_info_file, 'r'))
    dinfo['startdate'] = min(DateTime).strftime('%Y-%m-%d %H:%M:%S')
    dinfo['enddate'] = max(DateTime).strftime('%Y-%m-%d %H:%M:%S')
    
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




if __name__ == '__main__':
    
#    sm.bulk_convert_to_nc(__file__)
    
    
    converter = 'VMS_DFO'
    path_to_data_in = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\data\\VMS_2012_DFO\\data_original'
    sm.bulk_convert_to_nc(converter, path_to_data_in=path_to_data_in, overwrite=True)

    








