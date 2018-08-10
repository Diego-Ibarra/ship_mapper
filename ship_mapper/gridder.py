'''
Fucntions that condense a list of "pings" (i.e. vessel positions) into a 2-dimensional grid.


'''


import pandas as pd
import numpy as np
import xarray as xr
import os
import copy
import ship_mapper as sm




def gridder(info, data_in, filename_out, overwrite=False):
    '''
    Counts "pings" inside a grid-cell and computes "Ship minutes per km2"
    
    :param info info: ``info`` object containing metadata
    :param xarray.DataSet data_in: Data
    :param str filename_out: Name of file that will be writen as output
    :param boolean overwrite: If ``True`` older files will be overwritten. If ``False``, only new files will be processed
                              
    .. seealso::
        
        :py:func:`grid_merger <ship_mapper.grid_merger>` 
    '''
    
    print('gridder ---------------------------------------------')
    
    file_out = os.path.join(str(info.dirs.gridded_data), filename_out)
    
    interp_threshold = 40
    
    if not os.path.isfile(file_out) or overwrite:
        
        ship_id = data_in.attrs['ship_id']
    
        data = data_in
    
        # Make grid      
        x = np.arange(info.grid.minlon, info.grid.maxlon, info.grid.bin_size, dtype=np.float64)
        y = np.arange(info.grid.minlat, info.grid.maxlat, info.grid.bin_size, dtype=np.float64)
        
        info.grid.bin_number = (np.ceil((info.grid.maxlon - info.grid.minlon)/info.grid.bin_size),
                                np.ceil((info.grid.maxlat - info.grid.minlat)/info.grid.bin_size))

        # Find unique ships
        unis = pd.unique(data[ship_id].values)
        print('Number of Unique Ships = ' + str(len(unis)))
        
        iix, iiy, iit = [], [], []
        counter = 0

        for ship in unis:
            counter += 1
            print('Ship: ' + str(counter) + ' (id:'+ str(ship) + ')')
            
            indxship = (data[ship_id] == ship)
            singleship = data.sel(Dindex=indxship)
            
            # Determine "trips"
            indxtrip = (singleship['SeqNum'].diff('Dindex') > 1) #find > 1-day gaps
            trip_gaps = indxtrip[indxtrip==True]['Dindex'].values
            trip_gaps = np.insert(trip_gaps, 0, 0)
            trip_gaps = np.append(trip_gaps,singleship['Dindex'].values[-1]+1)
                
            # Loop over trips
            for k in range(1,len(trip_gaps)):
                print('trip = ' + str(k))
                
                index_gap = ((singleship['Dindex'] >= trip_gaps[k-1]) &
                             (singleship['Dindex'] < trip_gaps[k]))
                
                singleship_trip = singleship.sel(Dindex=index_gap)
                
                # Get lat/lons/seqNums
                lons = singleship_trip['longitude'].values.tolist()
                lats = singleship_trip['latitude'].values.tolist()
                seqNums = singleship_trip['SeqNum'].values.tolist()
     
                num_of_pings = len(lons)
                
                if num_of_pings > 1: 
                    
                    for j in range(1,num_of_pings): 
                        lon1 = lons[j-1]
                        lat1 = lats[j-1]
                        lon2 = lons[j]
                        lat2 = lats[j]
                        x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
                        x2, y2 = sm.align_with_grid(x, y, lon2, lat2)

                        # Iterpolate bewtween known points
                        elapsed_days = abs(seqNums[j] - seqNums[j-1])
                        
                        # Estimate distance and velocity
                        dist = sm.distance(lat1,lon1,lat2,lon2)
                        
                        
                        if dist < (interp_threshold * 1.852 * 1000): # knots * knots_to_km/h conversion * km_to_m conversion (= meters)
                            
                            ix, iy = sm.interp2d(x1, y1, x2, y2)
                            
                            minutes_per_cell = elapsed_days / len(ix) * 1440
                            
                            iix.extend(ix)
                            iiy.extend(iy)
                            iit.extend([minutes_per_cell] * len(ix))


        # Project pings to grid     
        H0, xedges, yedges = np.histogram2d(iix,iiy,bins=info.grid.bin_number,
                                            range=[[0, info.grid.bin_number[0]],
                                                   [0, info.grid.bin_number[1]]],
                                                   weights=iit)
        
        ship_density = H0 / info.grid.areas
                
        D = xr.Dataset({'ship_density':(['x','y'],ship_density)},
                coords={'lon':(['x'],x),
                        'lat':(['y'],y)})
    
        # Metadata
        D.attrs = copy.deepcopy(data.attrs)
        # delete irrelevants
        del(D.attrs['ship_id'])
        # add new ones
        D.attrs['minlat'] = info.grid.minlat
        D.attrs['maxlat'] = info.grid.maxlat
        D.attrs['minlon'] = info.grid.minlon
        D.attrs['maxlon'] = info.grid.maxlon
        D.attrs['bin_number'] = info.grid.bin_number
        D.attrs['bin_size'] = info.grid.bin_size
        D.attrs['time_bin'] = info.grid.time_bin
        D.attrs['interpolation'] = 'Linear'
        D.attrs['interp_threshold'] = interp_threshold
        D.attrs['units'] = 'Ship minutes per km$^2$'
        D.attrs['unit_description'] = ('Minutes spent by vessels\n' + 
                                    'inside the area of a gricell\n' + 
                                    '(note it is LOG scale)')
        
        # Print NetCDF file
        sm.checkDir(str(info.dirs.gridded_data))
        print('Writting...')
        print('...' + file_out)    
        D.to_netcdf(path=file_out)
    
    return












def gridder_pingsPerCell(info, data_in, file_name, overwrite=False):
    '''
    Counts "pings" inside a gridcell and computes "No. of vessels within grid-cell"
    '''
    
    print('gridder_pingsPerCell ----------------------------')
    
    file_out = os.path.join(str(info.dirs.gridded_data), file_name)
    
    interp_threshold = 40
    
    if not os.path.isfile(file_out) or overwrite:
        
        ship_id = data_in.attrs['ship_id']
    
        data = data_in
    
        # Make grid       
        x = np.arange(info.grid.minlon, info.grid.maxlon, info.grid.bin_size, dtype=np.float64)
        y = np.arange(info.grid.minlat, info.grid.maxlat, info.grid.bin_size, dtype=np.float64)
        
        info.grid.bin_number = (np.ceil((info.grid.maxlon - info.grid.minlon)/info.grid.bin_size),
                                np.ceil((info.grid.maxlat - info.grid.minlat)/info.grid.bin_size))

        # Find unique ships
        unis = pd.unique(data[ship_id].values)
        print('Number of Unique Ships = ' + str(len(unis)))
        
        iiix, iiiy = [], []
        counter = 0

        for ship in unis:
            counter += 1
            print('Ship: ' + str(counter) + ' (id:'+ str(ship) + ')')
            
            indxship = (data[ship_id] == ship)
            singleship = data.sel(Dindex=indxship)
            
                     
            # Determine "trips"
            indxtrip = (singleship['SeqNum'].diff('Dindex') > 1) #find > 1-day gaps
            trip_gaps = indxtrip[indxtrip==True]['Dindex'].values
            trip_gaps = np.insert(trip_gaps, 0, 0)
            trip_gaps = np.append(trip_gaps,singleship['Dindex'].values[-1]+1)
                
            # Loop over trips
            for k in range(1,len(trip_gaps)):
                print(k)
                
                index_gap = ((singleship['Dindex'] >= trip_gaps[k-1]) &
                             (singleship['Dindex'] < trip_gaps[k]))
                
                singleship_trip = singleship.sel(Dindex=index_gap)
                
                # Split data into "time_bins"
                time_bin = 1/144#info.grid.bin_size / (60*24) # units are converted to: days
                
                MinSeqNum = singleship_trip['SeqNum'].values.min()
                MaxSeqNum = singleship_trip['SeqNum'].values.max() + time_bin
                
                time_bins = np.arange(MinSeqNum, MaxSeqNum, time_bin) # 1/144 = once every 10 minutes
                
                # Loop over each ship's time_bin
                for i in range(1,len(time_bins)):
                    iix, iiy = [], []
                    
                    indx = ((singleship_trip['SeqNum'] >= time_bins[i-1]) &
                            (singleship_trip['SeqNum'] <= time_bins[i]))
             
                    
                    singleship_trip_bin = singleship_trip.sel(Dindex=indx)

                    # Get lat/lons
                    lons = singleship_trip_bin['longitude'].values.tolist()
                    lats = singleship_trip_bin['latitude'].values.tolist()
                    
                    #Insert last bin's lat/lon
                    if i > 1 and len(lons) > 0:
                        lons.insert(0, last_lon)
                        lats.insert(0, last_lat)
                    
                    num_of_pings = len(lons)
                    
                
                    if num_of_pings == 0:
                        pass
                    elif num_of_pings == 1:
                        lon2 = lons[0]
                        lat2 = lats[0]
                        x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
                        iix.append(x2)
                        iiy.append(y2) 
                    elif num_of_pings > 1: 
                        for j in range(1,num_of_pings): 
                            # Iterpolate bewtween known points
                            lon1 = lons[j-1]
                            lat1 = lats[j-1]
                            lon2 = lons[j]
                            lat2 = lats[j]
                            
                            # Estimate distance and velocity
                            dist = sm.distance(lat1,lon1,lat2,lon2)
                            
                            if dist < (interp_threshold * 1.852 * 1000): # knots * knots_to_km/h conversion * km_to_m conversion (= meters)
                                
                                x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
                                x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
                                
                                ix, iy = sm.interp2d(x1, y1, x2, y2)
                                
                                iix.extend(ix)
                                iiy.extend(iy)                   

                                           
                    #drop duplicates
                    df = {}
                    df = pd.DataFrame({'x':iix,'y':iiy}).drop_duplicates(keep='last')
                    
                    # Append
                    iiix.extend(df['x'].tolist())
                    iiiy.extend(df['y'].tolist())
                    
                    #Save last lat/lon
                    if len(lats) > 0:
                        last_lat = lats[-1]
                        last_lon = lons[-1]

                
        # Project pings to grid        
        H0, xedges, yedges = np.histogram2d(iiix,iiiy,bins=info.grid.bin_number,
                                            range=[[0, info.grid.bin_number[0]],
                                                   [0, info.grid.bin_number[1]]])
#        # Rotate and flip H...
#        H0 = np.rot90(H0)
#        H0 = np.flipud(H0)
                
        D = xr.Dataset({'ship_density':(['x','y'],H0)},
                coords={'lon':(['x'],x),
                        'lat':(['y'],y)})
                    
        # Metadata
        D.attrs = copy.deepcopy(data.attrs)
        # delete irrelevants
        del(D.attrs['ship_id'])
        # add new ones
        D.attrs['minlat'] = info.grid.minlat
        D.attrs['maxlat'] = info.grid.maxlat
        D.attrs['minlon'] = info.grid.minlon
        D.attrs['maxlon'] = info.grid.maxlon
        D.attrs['bin_number'] = info.grid.bin_number
        D.attrs['bin_size'] = info.grid.bin_size
        D.attrs['time_bin'] = info.grid.time_bin
        D.attrs['interpolation'] = 'Linear'
        D.attrs['interp_threshold'] = interp_threshold
        D.attrs['units'] = 'No. of vessels within grid-cell'
        D.attrs['unit_description'] = ('Number of vessels inside\n' + 
                                    'a gridcell within the time range of\n' + 
                                    'observations (note it is LOG scale)')
        
        # Print NetCDF file
        sm.checkDir(str(info.dirs.gridded_data))
        print('Writting...')
        print('...' + file_out)    
        D.to_netcdf(path=file_out)
    
    return










def grid_merger(info, files=None, filename_out='auto'):
    '''
    Combines several gridded files into one
    '''
    
    from datetime import datetime
    
    print('grid_merger ---------------------------------------------')

    
    if files == None:
        all_files = sm.get_all_files(info.dirs.gridded_data)
    else:
        all_files = files
    
    # Process 1st grid
    data0 = xr.open_dataset(all_files[0])
    H0 = data0['ship_density'].values
   

    startdate = datetime.strptime(data0.attrs['startdate'], '%Y-%m-%d %H:%M:%S')
    enddate = datetime.strptime(data0.attrs['enddate'], '%Y-%m-%d %H:%M:%S')
    
    #Pre-build metadata
    metadata = data0.attrs
    

    # Process the rest of the grid files
    for file_in in all_files[1:]:
        try:
            print(file_in)
            dataX = xr.open_dataset(file_in)
            startdate = min(startdate, datetime.strptime(dataX.attrs['startdate'], '%Y-%m-%d %H:%M:%S'))
            enddate = max(enddate, datetime.strptime(dataX.attrs['enddate'], '%Y-%m-%d %H:%M:%S'))
            H = dataX['ship_density'].values
            H0 = H0 + H
        except:
            pass
            
    # Create dataset
    D = xr.Dataset({'ship_density':(['x','y'],H0)},
            coords={'lon':(['x'],data0['lon'].values),
                    'lat':(['y'],data0['lat'].values)})
    
    #Save metadata
    D.attrs = metadata
    D.attrs['startdate']=startdate.strftime('%Y-%m-%d %H:%M:%S')
    D.attrs['enddate']=enddate.strftime('%Y-%m-%d %H:%M:%S')
    
    # Save merged file
    sm.checkDir(str(info.dirs.merged_grid))
  
    
    if filename_out == 'auto':
        filename_OUT = 'merged_grid.nc'
    else:
        filename_OUT = filename_out
        
    file_out = os.path.join(str(info.dirs.merged_grid), filename_OUT)
    D.to_netcdf(path=file_out)
    
    data0.close()
    
    print('Merging completed!')
    
    return D



        
def getWKT_PRJ (epsg_code):
    '''
    Downloads and returns geospatial parameters given an epsg code
    
    :param str epsg_code: Code referring to an entry in the EPSG Geodetic Parameter Dataset,
                          which is a collection of definitions of coordinate reference
                          systems and coordinate transformations
                          
    :return: geospatial parameters
    
    :rtype: projection object
                          
    '''
    import urllib.request
    wkt = urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    wkt_bytes = wkt.read()
    wkt_decoded = wkt_bytes.decode("utf8")
    remove_spaces = wkt_decoded.replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output



def mergedgrid_to_shp(info, file_in=None):
    '''
    Converts a gridded file into a shapefile
    
    :param info info: ``info`` object containing metadata
    '''
    import shapefile
    
    print('mergedgrid_to_shp ------------------------------------------------')
    
    # Load data
    if file_in == None:
        file_in = os.path.join(str(info.dirs.merged_grid),'merged_grid.nc')
    
    d = xr.open_dataset(file_in)
    
    
    w = shapefile.Writer()
    w.field('Vessel Density', 'C')
  
    
    for i in range(0,len(d['lon'].values)-1):
        print(i)
        for j in range(0,len(d['lat'].values)-1):     
            lon1 = float(d['lon'].values[i])
            lat1 = float(d['lat'].values[j])
            lon2 = float(d['lon'].values[i+1])
            lat2 = float(d['lat'].values[j+1])
            density = float(d['ship_density'].values[i,j])
            
            if density > 0:
                w.poly(parts=[[[lon1,lat1],[lon2,lat1],[lon2,lat2],[lon1,lat2],[lon1,lat1]]])
                w.record(density)
    
    shapefile_name = os.path.join(str(info.dirs.shapefiles),info.project_name)

    w.save(shapefile_name)
    
    prj = open(shapefile_name + '.prj', 'w')
    epsg = getWKT_PRJ(info.grid.epsg_code)
    prj.write(epsg)
    prj.close()
    return
    




def calculate_gridcell_areas(info):
    '''
    Calculates the area of each of the grid-cells in the domain (in km^2)
    
    :param info info: ``info`` object WITHOUT `info.grid.areas`
    
    :return: ``info`` object WITH `info.grid.areas`
    
    :rtype: info
    '''
    import ship_mapper as sm
    
    print('Calculating grid-cell areas........................')
    
    x = np.arange(info.grid.minlon, info.grid.maxlon, info.grid.bin_size, dtype=np.float64)
    y = np.arange(info.grid.minlat, info.grid.maxlat, info.grid.bin_size, dtype=np.float64)
    
    u = np.empty((len(x)+1,))
    v = np.empty((len(y)+1,))
    areas = np.empty((len(x),len(y)))
    
    for i in range(1,len(x)):
        u[i] = x[i] - ((x[i] - x[i-1])/2)
    u[0] = x[0] - ((x[1] - x[0])/2)
    u[-1] = x[-1] + ((x[-1] - x[-2])/2)
    
    for i in range(1,len(y)):
        v[i] = y[i] - ((y[i] - y[i-1])/2)
    v[0] = y[0] - ((y[1] - y[0])/2)
    v[-1] = y[-1] + ((y[-1] - y[-2])/2)
    
    for i in range(0,len(x)):
        for j in range(0,len(y)):
            # areas = ((a+b)/2)*h
            a = sm.distance(v[j+1],u[i],v[j+1],u[i+1])/1000 #divided by 1000 to convert to km
            b = sm.distance(v[j],u[i],v[j],u[i+1])/1000 #divided by 1000 to convert to km
            h = sm.distance(v[j],x[i],v[j+1],x[i])/1000 #divided by 1000 to convert to km
            areas[i,j] = ((a + b)/2)*h
            
        info.grid.areas = areas
    
    return info











