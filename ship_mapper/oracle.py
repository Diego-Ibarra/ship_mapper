import cx_Oracle
import datetime
import numpy as np
import xarray as xr
import pandas as pd

import ship_mapper as sm

def download_vms(info, startdate, enddate):
    '''
    Downloads VMS data from oracle database
    
    Attributes:
        info (info): ``info`` object containing metadata
    
        startdate (datetime): Start date
    
        enddate (datetime): End date
        
    Returns:
        .cvs file
    
    '''

    import csv
    import os

    
    # Make new empty file
    
    startdate_str = startdate.strftime('%Y-%m-%d %H:%M:%S')
    enddate_str = enddate.strftime('%Y-%m-%d %H:%M:%S')
    
    sm.checkDir(info.dirs.data_original)
    
    settings = sm.load_settings(info)
    
    FILE=open(os.path.join(info.dirs.data_original,'vms_autoDownloaded.csv'),"w",newline='');
    output=csv.writer(FILE, dialect='excel')
    output.writerow(['VR_NUMBER','LATITUDE','LONGITUDE','POSITION_UTC_DATE'])
    
    # Get data
    MyDNS = cx_Oracle.makedsn('VSNSBIOXP74.ENT.DFO-MPO.CA', 1521, sid=None, service_name='PTRAN.ENT.DFO-MPO.CA')
    db = cx_Oracle.connect(user=settings.ORACLE_USER, password=settings.ORACLE_PASSWORD, dsn=MyDNS)
    cursor = db.cursor()
    
    query = ("select VR_NUMBER,LATITUDE,LONGITUDE,POSITION_UTC_DATE"
             "              from MFD_OBFMI.VMS_ALL"
             "              WHERE POSITION_UTC_DATE> to_date('" + startdate_str + "','YYYY-MM-DD HH24:MI:SS')"
             "              AND POSITION_UTC_DATE <= to_date('" + enddate_str + "','YYYY-MM-DD HH24:MI:SS')"
             "              AND (LATITUDE > " + str(info.grid.minlat) + " AND LATITUDE < " + str(info.grid.maxlat) + ")"
             "              AND (LONGITUDE >" + str(info.grid.minlon) + " AND LONGITUDE < " + str(info.grid.maxlon) + ")")
    
    cursor.execute(query)
    
    for row in cursor:
        output.writerow(row)
    cursor.close()
    db.close()
    FILE.close()
    print("END of extraction")
    return




def filter_by_gear(info, dataIn, startdate, enddate, gearcode_sheet=None):
    '''
    Filters data by gear type
    '''
    
    print('Filtering by gearcode ..............................')
    
    settings = sm.load_settings(info)
    
    startdate_minus1_str = (startdate - datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    enddate_plus1_str = (enddate + datetime.timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')
    
    MyDNS = cx_Oracle.makedsn('VSNSBIOXP74.ENT.DFO-MPO.CA', 1521, sid=None, service_name='PTRAN.ENT.DFO-MPO.CA')
    db = cx_Oracle.connect(user=settings.ORACLE_USER, password=settings.ORACLE_PASSWORD,dsn=MyDNS)
    
    # Get gear-type
    #Create additional comlumn in data
    dummyarray = np.empty((len(dataIn['latitude'].values),))
    dummyarray[:] = np.nan
    
    dummyDataArray = xr.DataArray(dummyarray,name='NARW_CODE',coords=[dataIn['Dindex'],],dims=['Dindex',])
    
    md = dataIn.attrs
    dataIn = xr.merge([dataIn,dummyDataArray])
    dataIn.attrs = md
    
    gear_codes = pd.read_excel(gearcode_sheet)
    narw_codes = gear_codes['GEAR_CODE'][gear_codes['NARW RISK']==1]
    
    unis = pd.unique(dataIn['ship_id_vrn'])
    print('Number of Unique Ships = ' + str(len(unis)))
    
    for ship in unis:
        print('Ship=' + str(ship))
        cursor = db.cursor()
        
        query = ("SELECT MARFISSCI.MARFIS_HAIL_OUT.VR_NUMBER,"
                 "MARFISSCI.MARFIS_HAIL_OUT.LICENCE_NO,"
                 "MARFISSCI.MARFIS_HAIL_OUT.SAILED_DATE_TIME,"
                 "MARFISSCI.MARFIS_HAIL_OUT.EST_LANDED_DATE,"
                 "MARFISSCI.MARFIS_HAIL_OUT.SPECIES_CODE,"
                 "MARFISSCI.LICENCES.SPECIES_CODE AS SPECIES_CODE1,"
                 "MARFISSCI.LICENCE_GEARS.GEAR_CODE"
                 "              FROM MARFISSCI.LICENCE_GEARS"
                 "              INNER JOIN MARFISSCI.MARFIS_HAIL_OUT"
                 "              ON MARFISSCI.MARFIS_HAIL_OUT.LICENCE_NO = MARFISSCI.LICENCE_GEARS.LICENCE_ID"
                 "              INNER JOIN MARFISSCI.LICENCES"
                 "              ON MARFISSCI.MARFIS_HAIL_OUT.LICENCE_NO        = MARFISSCI.LICENCES.LICENCE_ID"
                 "              WHERE MARFISSCI.MARFIS_HAIL_OUT.VR_NUMBER      = " + str(ship) + 
                 "              AND MARFISSCI.MARFIS_HAIL_OUT.EST_LANDED_DATE  > to_date('" + startdate_minus1_str + "','YYYY-MM-DD HH24:MI:SS')"
                 "              AND MARFISSCI.MARFIS_HAIL_OUT.EST_LANDED_DATE <= to_date('" + enddate_plus1_str + "','YYYY-MM-DD HH24:MI:SS')")
        
        
        cursor.execute(query)
        
        ho_licence = []
        ho_sailed_time = []
        ho_est_landed_time = []
        ho_species = []
        ho_species2 = []
        ho_gear = []
        first_est_landed_time = []
        narw_risk = []
        for row in cursor:
            if first_est_landed_time == row[3]:
                ho_licence[-1].append(int(row[1]))
                ho_species[-1].append(row[4])
                ho_species2[-1].append(row[5])
                ho_gear[-1].append(row[6])
                if row[6] in narw_codes.values and not narw_risk[-1]:
                    narw_risk[-1]=True
            else:
                ho_licence.append([int(row[1])])
                ho_sailed_time.append(row[2])
                ho_est_landed_time.append(row[3])
                ho_species.append([row[4]])
                ho_species2.append([row[5]])
                ho_gear.append([row[6]])
                if row[6] in narw_codes.values:
                    narw_risk.append(True)
                else:
                    narw_risk.append(False)
                first_est_landed_time = row[3]
    
    
        # Copy NARF_Codes to data
        for i in range(1,len(narw_risk)):
       
            startdate = ho_sailed_time[i-1]
            enddate = ho_sailed_time[i]
            
            mask = (dataIn['ship_id_vrn'].values==ship) & (dataIn['DateTime'].values > np.datetime64(startdate)) & (dataIn['DateTime'].values <= np.datetime64(enddate))
            
            dataIn['NARW_CODE'][mask] = narw_risk[0]
        
        try:
            #Do left tail
            mask = (dataIn['ship_id_vrn'].values==ship) & (dataIn['DateTime'].values > np.datetime64(ho_sailed_time[0]))
            dataIn['NARW_CODE'][mask] = narw_risk[0]
        except:
            pass
    
        try:
            #Do right tail
            mask = (dataIn['ship_id_vrn'].values==ship) & (dataIn['DateTime'].values <=  np.datetime64(ho_sailed_time[-1]))
            dataIn['NARW_CODE'][mask] = narw_risk[-1]   
        except:
            pass
    
    
    db.close()
    
    
    # Further filter data by speed
    indx = (dataIn['NARW_CODE'] == True )
    
    dataOut = dataIn.sel(Dindex=indx)
    
    #TODO: Add comment to data attrs
    #info.sidebar.included_vessel_types = 'Fixed gear'
    
    return dataOut












