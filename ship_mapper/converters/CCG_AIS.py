"""
This is a csv to nc converter for AIS data from the Canadian Coast Guard (Terrestrial)
"""

def convert(file_in,file_out):

    import pandas as pd
    import xarray as xr
    import time

    print(file_in)
    t0 = time.time()
    csv = pd.read_table(file_in, sep=',')
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
                    'ship_id_mmsi':(['Dindex'],csv['MMSI']),
                    'Speed_Over_Ground_SOG_knots':(['Dindex'],csv['Speed_Over_Ground_SOG_knots']),
                    'Position_Accuracy':(['Dindex'],csv['Position_Accuracy']),
                    'longitude':(['Dindex'],csv['Longitude_decimal_degrees']),
                    'latitude':(['Dindex'],csv['Latitude_decimal_degrees']),
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
                'ship_id_mmsi':{'zlib':True},
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