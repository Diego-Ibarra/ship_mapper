print('Diego!!')

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
    import cx_Oracle
    import csv
    import os
    import ship_mapper as sm
    
    # Make new empty file
    
    startdate_str = startdate.strftime('%Y-%m-%d %H:%M:%S')
    enddate_str = enddate.strftime('%Y-%m-%d %H:%M:%S')
    
    sm.checkDir(info.dirs.data_original)
    
    FILE=open(os.path.join(info.dirs.data_original,'vms_autoDownloaded.csv'),"w",newline='');
    output=csv.writer(FILE, dialect='excel')
    output.writerow(['VR_NUMBER','LATITUDE','LONGITUDE','POSITION_UTC_DATE'])
    
    # Get data
    MyDNS = cx_Oracle.makedsn('VSNSBIOXP74.ENT.DFO-MPO.CA', 1521, sid=None, service_name='PTRAN.ENT.DFO-MPO.CA')
    db = cx_Oracle.connect(user='test', password='test',dsn=MyDNS)
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