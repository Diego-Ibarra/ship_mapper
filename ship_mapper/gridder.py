# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:19:49 2018

@author: IbarraD
"""


import pandas as pd
import numpy as np
import xarray as xr
import os
import ship_mapper as sm


def gridder(info, data_in, file_name, overwrite=False):
    
    print('gridder ---------------------------------------------')
    
    file_out = os.path.join(str(info.dirs.gridded_data), info.run_name + '_' + str(info.grid.bin_number)+ '_' + file_name  + '.nc')
    
    if not os.path.isfile(file_out) or overwrite:
        
        ship_id = info.ship_id
    
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
                
                index_gap = ((singleship['Dindex'] >= trip_gaps[k-1]) &
                             (singleship['Dindex'] < trip_gaps[k]))
                
                singleship_trip = singleship.sel(Dindex=index_gap)
                
                # Split data into "time_bins"
                bin_size = 1/144 # 1/144 = once every 10 minutes
                
                MinSeqNum = singleship_trip['SeqNum'].values.min()
                MaxSeqNum = singleship_trip['SeqNum'].values.max() + bin_size
                
                time_bins = np.arange(MinSeqNum, MaxSeqNum, bin_size) # 1/144 = once every 10 minutes
                
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
                            
                            if dist < (40 * 1.852 * 1000): # knots * knots_to_km/h conversion * km_to_m conversion (= meters)
                                
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



def grid_merger(info, files=None):
    
    print('grid_merger ---------------------------------------------')
    
    if files == None:
        all_files = sm.get_all_files(info.dirs.gridded_data)
    else:
        all_files = files
    
    # Process 1st grid
    data0 = xr.open_dataset(all_files[0])
    H0 = data0['ship_density'].values

    # Process the rest of the grid files
    for file_in in all_files[1:]:
        H = xr.open_dataset(file_in)['ship_density'].values
        H0 = H0 + H
            
    # Create dataset
    D = xr.Dataset({'ship_density':(['x','y'],H0)},
            coords={'lon':(['x'],data0['lon'].values),
                    'lat':(['y'],data0['lat'].values)})
            
    # Save merged file
    sm.checkDir(str(info.dirs.merged_grid))
    file_out = os.path.join(str(info.dirs.merged_grid), 'merged_grid.nc')
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
    
















