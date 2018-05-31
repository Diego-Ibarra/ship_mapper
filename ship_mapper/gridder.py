# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:19:49 2018

@author: IbarraD
"""
 

import pandas as pd
import numpy as np
import xarray as xr
import os
import copy
import ship_mapper as sm

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



def gridder(info, data_in, filename_out, overwrite=False):
    
    print('gridder ---------------------------------------------')
    
    file_out = os.path.join(str(info.dirs.gridded_data), filename_out)
    
    interp_threshold = 40
    
    if not os.path.isfile(file_out) or overwrite:
        
        print('^^^^^^^^^^^^^^^^^^^^^^^')
        print(data_in.attrs)
        
        ship_id = data_in.attrs['ship_id']
    
        data = data_in
    
        # Make grid
#        x = np.linspace(info.grid.minlon, info.grid.maxlon, num=info.grid.bin_number)
#        y = np.linspace(info.grid.minlat, info.grid.maxlat, num=info.grid.bin_number)
        
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
#        D = sm.write_info2data(D,info)
        
#        # MAP --------------------------------------------------------------
#        import matplotlib.pyplot as plt
#        from mpl_toolkits.basemap import Basemap
##        minlat = data['latitude'].values.min()
##        maxlat = data['latitude'].values.max()
##        minlon = data['longitude'].values.min()
##        maxlon = data['longitude'].values.max()
#        minlat = info.grid.minlat
#        maxlat = info.grid.maxlat
#        minlon = info.grid.minlon
#        maxlon = info.grid.maxlon
#        
#        m = Basemap(projection='mill', llcrnrlat=minlat,urcrnrlat=maxlat,
#        llcrnrlon=minlon, urcrnrlon=maxlon,resolution='i')
#        
#        xdots, ydots = m(singleship['longitude'].values,singleship['latitude'].values) 
#                
#        cs = m.scatter(xdots,ydots,1,marker='.',color='r', zorder=15)
#        
#        # ------------
##        x = np.linspace(minlon, maxlon, num=info.grid.bin_number)
##        y = np.linspace(minlat, maxlat, num=info.grid.bin_number)
#
#        xx, yy = m(x,y)
#
#        print(H0)
#        Hmasked = np.ma.masked_where(H0<1,H0)
#
#        cs2 = m.pcolor(xx,yy,Hmasked,cmap=plt.get_cmap('copper_r'),alpha=0.5, zorder=10)
#        cbar = plt.colorbar(extend='both')
#        m.drawcoastlines(linewidth=0.5,zorder=25)
#    #    
#        plt.show()
#        # MAP --------------------------------------------------------------
        
        # Print NetCDF file
        sm.checkDir(str(info.dirs.gridded_data))
        print('Writting...')
        print('...' + file_out)    
        D.to_netcdf(path=file_out)
    
    return



def grid_merger(info, files=None, filename_out='auto'):
    
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
    import urllib.request
    wkt = urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    wkt_bytes = wkt.read()
    wkt_decoded = wkt_bytes.decode("utf8")
    remove_spaces = wkt_decoded.replace(" ","")
    output = remove_spaces.replace("\n", "")
    return output



def mergedgrid_to_shp(info, file_in=None):
    
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
    




def calculate_gridcell_areas(info):
    '''
    Output in km^2
    '''
    import ship_mapper as sm
    
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
        
#        import matplotlib.pyplot as plt
#        lons, lats = np.meshgrid(y,x)
#        plt.pcolormesh(lats, lons, areas)
#        plt.colorbar()
#        plt.show()
    
    return info











