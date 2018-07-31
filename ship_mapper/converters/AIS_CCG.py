def convert(file_in, file_out, data_info_file):
    '''
    This is a csv to nc converter for AIS data from the Canadian Coast Guard (Terrestrial)
    
    :param str file_in: Input file (.csv)
    
    :param str file_out: Output file (.nc)
    
    :param str data_info_file: YAML file describing other conversion parameters (.yml)
    
    :return: A netCDF file (.nc) in a format standard for "ship_mapper" 
             containing the original data, but also containing metadata included in the data_info.yml file
    '''
    import pandas as pd
    import numpy as np
    import xarray as xr
    import datetime
    import time
    import yaml

    print(file_in)
    
#    file_in = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\data\\CCG_AIS\\data_original\\CCG_AIS_Dynamic_Data_2017-06-01.csv'
    
    t0 = time.time()
    csv = pd.read_table(file_in, sep=',')
    #csvS = pd.read_table(Sfilename, sep=',')
       
    originTime = datetime.datetime.strptime('1/1/1980 00:00',"%m/%d/%Y %H:%M")
        
    df = pd.DataFrame({'year':csv['year'].values,
                       'month':csv['month'].values,
                       'day':csv['day'].values,
                       'hour':csv['hour'].values,
                       'minute':csv['minute'].values,
                       'second':csv['second'].values})

    timeObject = pd.to_datetime(df)
    
    SeqNum = (timeObject - originTime).astype('timedelta64[s]') / (60*60*24)

    
                
    # Metadata
    dinfo = yaml.load(open(data_info_file, 'r'))
    dinfo['startdate'] = min(timeObject).strftime('%Y-%m-%d %H:%M:%S')
    dinfo['enddate'] = max(timeObject).strftime('%Y-%m-%d %H:%M:%S')
    
    
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
                    'DateTime':(['Dindex'],timeObject),
                    'SeqNum':(['Dindex'],SeqNum),
                    'ID':(['Dindex'],csv['ID']),
                    'AIS_Class':(['Dindex'],csv['AIS_Class']),
                    'Message_Type':(['Dindex'],csv['Message_Type']),
                    'Repeat_Indicator':(['Dindex'],csv['Repeat_Indicator']),
                    'MMSI':(['Dindex'],csv['MMSI']),
                    'Speed_Over_Ground_SOG_knots':(['Dindex'],csv['Speed_Over_Ground_SOG_knots']),
                    'Position_Accuracy':(['Dindex'],csv['Position_Accuracy']),
                    'longitude':(['Dindex'],csv['Longitude_decimal_degrees']),
                    'latitude':(['Dindex'],csv['Latitude_decimal_degrees']),
                    'Course_Over_Ground_COG_degrees':(['Dindex'],csv['Course_Over_Ground_COG_degrees']),
                    'True_heading_HDG_degrees':(['Dindex'],csv['True_heading_HDG_degrees']),
                    'Navigation_Status':(['Dindex'],csv['Navigation_Status']),
                    'TimeStamp_s':(['Dindex'],csv['TimeStamp_s'])},
                coords={'Dindex':(['Dindex'],csv.index)},
                attrs=dinfo)
    
    
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
                'DateTime':{'zlib':True},
                'SeqNum':{'zlib':True},
                'AIS_Class':{'dtype':'S1','zlib':True},
                'Message_Type':{'zlib':True},
                'Repeat_Indicator':{'zlib':True},
                'MMSI':{'zlib':True},
                'Speed_Over_Ground_SOG_knots':{'zlib':True},
                'Position_Accuracy':{'zlib':True},
                'longitude':{'zlib':True},
                'latitude':{'zlib':True},
                'Course_Over_Ground_COG_degrees':{'zlib':True},
                'True_heading_HDG_degrees':{'zlib':True},
                'Navigation_Status':{'zlib':True},
                'TimeStamp_s':{'zlib':True}}
    
    D.to_netcdf(file_out,format='NETCDF4',engine='netcdf4',encoding=encoding)
    
    t1 = time.time()
    print(str((t1-t0)/60))
    
    
    
    return