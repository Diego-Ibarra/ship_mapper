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

#    print(file_in)
    
#    file_in = '/home/diego/data/AIS_SAT_2017/data_original/Dynamic_Data/SAT_AIS_Dynamic_Data_2017-03-01-00.csv'
#    file_out = '/home/diego/data/AIS_SAT_2017/data_nc/SAT_AIS_Dynamic_Data_2017-03-01-00.nc'
#    data_info_file = '/home/diego/data/AIS_SAT_2017/data_info.yaml'
    
    t0 = time.time()
           
    originTime = datetime.datetime.strptime('1/1/1980 00:00',"%m/%d/%Y %H:%M")
    
    # Dynamic Data ------------------------------------------------------------
    csv = pd.read_table(file_in, sep=',')
    #csvS = pd.read_table(Sfilename, sep=',')

        
    df = pd.DataFrame({'year':csv['year'].values,
                       'month':csv['month'].values,
                       'day':csv['day'].values,
                       'hour':csv['hour'].values,
                       'minute':csv['minute'].values,
                       'second':csv['second'].values})

    timeObject = pd.to_datetime(df)
    
    SeqNum = (timeObject - originTime).astype('timedelta64[s]') / (60*60*24)

    
    # Static Data -------------------------------------------------------------
    file_in_static = file_in.replace('Dynamic','Static')
    csvS = pd.read_table(file_in_static, sep=',', encoding = "ISO-8859-1")
    
    dfStat = pd.DataFrame({'year':csvS['year'].values,
                           'month':csvS['month'].values,
                           'day':csvS['day'].values,
                           'hour':csvS['hour'].values,
                           'minute':csvS['minute'].values,
                           'second':csvS['second'].values})
    
    timeObjectStat = pd.to_datetime(dfStat)
    
    SeqNumS = (timeObjectStat - originTime).astype('timedelta64[s]') / (60*60*24)
    
    # -------------------------------------------------------------------------
    
                
    # Metadata
    #hack: to fix location of data_info.yaml
    data_info_file = data_info_file.replace('data_original/','')
    
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
                    'TimeStamp_s':(['Dindex'],csv['TimeStamp_s']),
                    'Region_S':(['Sindex'],csvS['Region']),
                    'Station_Location_S':(['Sindex'],csvS['Station_Location']),
                    'AIS_Channel_S':(['Sindex'],csvS['AIS_Channel']),
                    'year_S':(['Sindex'],csvS['year']),
                    'month_S':(['Sindex'],csvS['month']),
                    'day_S':(['Sindex'],csvS['day']),
                    'hour_S':(['Sindex'],csvS['hour']),
                    'minute_S':(['Sindex'],csvS['minute']),
                    'second_S':(['Sindex'],csvS['second']),
                    'TimeZone_S':(['Sindex'],csvS['TimeZone']),
                    'AIS_Class_S':(['Sindex'],csvS['AIS_Class']),
                    'Message_Type_S':(['Sindex'],csvS['Message_Type']),
                    'Repeat_Indicator_S':(['Sindex'],csvS['Repeat_Indicator']),
                    'MMSI_S':(['Sindex'],csvS['MMSI']),
                    'IMO_number_S':(['Sindex'],csvS['IMO_number']),
                    'Call_Sign_S':(['Sindex'],csvS['Call_Sign']),
                    'Vessel_Name_S':(['Sindex'],csvS['Vessel_Name']),
                    'Type_of_Ship_and_Cargo':(['Sindex'],csvS['Type_of_Ship_and_Cargo']),
                    'Dimension_to_Bow_meters_S':(['Sindex'],csvS['Dimension_to_Bow_meters']),
                    'Dimension_to_Stern_meters_S':(['Sindex'],csvS['Dimension_to_Stern_meters']),
                    'Dimension_to_Port_meters_S':(['Sindex'],csvS['Dimension_to_Port_meters']),
                    'Dimension_to_Starboard_meters_S':(['Sindex'],csvS['Dimension_to_Starboard_meters']),
                    'Vessel_Length_meters_S':(['Sindex'],csvS['Vessel_Length_meters']),
                    'Vessel_Width_meters_S':(['Sindex'],csvS['Vessel_Width_meters']),
                    'Draught_decimeters_S':(['Sindex'],csvS['Draught_decimeters']),
                    'Destination_S':(['Sindex'],csvS['Destination'])},
                coords={'Dindex':(['Dindex'],csv.index),'Sindex':(['Sindex'],csvS.index)},
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
                'TimeStamp_s':{'zlib':True},
                'Region_S':{'dtype':'S1','zlib':True},
                'Station_Location_S':{'zlib':True},
                'AIS_Channel_S':{'dtype':'S1','zlib':True},
                'year_S':{'zlib':True},
                'month_S':{'zlib':True},
                'day_S':{'zlib':True},
                'hour_S':{'zlib':True},
                'minute_S':{'zlib':True},
                'second_S':{'zlib':True},
                'TimeZone_S':{'dtype':'S3','zlib':True},
                'AIS_Class_S':{'dtype':'S1','zlib':True},
                'Message_Type_S':{'dtype':'str','zlib':True},
                'Repeat_Indicator_S':{'dtype':'str','zlib':True},
                'MMSI_S':{'dtype':'u4','zlib':True},
                'IMO_number_S':{'dtype':'str','zlib':True},
                'Call_Sign_S':{'dtype':'str','zlib':True},
                'Vessel_Name_S':{'dtype':'str','zlib':True},
                'Type_of_Ship_and_Cargo':{'dtype':'i1','zlib':True},
                'Dimension_to_Bow_meters_S':{'dtype':'i1','zlib':True},
                'Dimension_to_Stern_meters_S':{'dtype':'i1','zlib':True},
                'Dimension_to_Port_meters_S':{'dtype':'i1','zlib':True},
                'Dimension_to_Starboard_meters_S':{'dtype':'i1','zlib':True},
                'Vessel_Length_meters_S':{'dtype':'i1','zlib':True},
                'Vessel_Width_meters_S':{'dtype':'i1','zlib':True},
                'Draught_decimeters_S':{'dtype':'i1','zlib':True},
                'Destination_S':{'dtype':'str','zlib':True},}
    
    # hack to fix location of file_out
    file_out = file_out.replace('Dynamic_Data/','')
    
    
    D.to_netcdf(file_out,format='NETCDF4',engine='netcdf4',encoding=encoding)
    
    t1 = time.time()
    print(str((t1-t0)/60))
    
    
    
    return