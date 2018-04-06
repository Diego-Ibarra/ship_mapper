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
    
    print('gridder ----------------------------------------------------------')
    
    import os
    
    file_out = os.path.join(str(info.dirs.gridded_data), info.run_name + '_' + str(info.grid.bin_number)+ '_' + file_name  + '.nc')
    
    if not os.path.isfile(file_out) or overwrite:
        
        # -----------------------------------------------------------------------------
        
        ship_id = info.ship_id
    
        data = data_in
    
        # Make grid
        x = np.linspace(data['longitude'].min(), data['longitude'].max(), num=info.grid.bin_number)
        y = np.linspace(data['latitude'].min(), data['latitude'].max(), num=info.grid.bin_number)

        # Find unique ships
        unis = pd.unique(data[ship_id].values)
#        unis = pd.unique(data['ship_id_vrn'].to_pandas().values)
        print('Number of Unique Ships = ' + str(len(unis)))
        iiix, iiiy = [], []
        counter = 0
        for ship in unis:
            counter += 1
            print('Ship: ' + str(counter) + ' (id:'+ str(ship) + ')')
            
            indxship = (data[ship_id] == ship)
            singleship = data.sel(Dindex=indxship)

            indxtrip = (singleship['SeqNum'].diff('Dindex') > 1) #find > 1-day gaps
            
#            gaps = np.trim_zeros(indxtrip.values*indxtrip['Dindex'].values)
            trip_gaps = indxtrip[indxtrip==True]['Dindex'].values
#            if trip_gaps[0] != 0:
            trip_gaps = np.insert(trip_gaps, 0, 0)
            trip_gaps = np.append(trip_gaps,singleship['Dindex'].values[-1]+1)
                
            
            for k in range(1,len(trip_gaps)):
                
                index_gap = ((singleship['Dindex'] > trip_gaps[k-1]-1) &
                             (singleship['Dindex'] < trip_gaps[k]))
                
                trip = singleship.sel(Dindex=index_gap)
                    
                MinSeqNum = trip['SeqNum'].values.min()
                MaxSeqNum = trip['SeqNum'].values.max() + (1/144)
                
                time_bins = np.arange(MinSeqNum, MaxSeqNum, 1/144) # 1/144 = once every 10 minutes
                
#                print(len(time_bins))
                
                # Loop over each ship's time_bin
                
                for i in range(1,len(time_bins)):
    #                print(i)
                    iix, iiy = [], []
                    indx = ((trip['SeqNum'] > time_bins[i-1]) &
                            (trip['SeqNum'] < time_bins[i]))
                    
                    singleship_bin = trip.sel(Dindex=indx)
                    
#                    print('------------------------------------------------' + str(i))
    #                    print(singleship_bin)
                    
                    num_of_pings = len(singleship_bin['SeqNum'].values)
                    
#                    print(num_of_bins)
                
                    if num_of_pings > 1:
                        for j in range(1,num_of_pings): 
                            # Iterpolate bewtween known points
                            lon1 = singleship_bin['longitude'].values[j-1]
                            lat1 = singleship_bin['latitude'].values[j-1]
                            lon2 = singleship_bin['longitude'].values[j]
                            lat2 = singleship_bin['latitude'].values[j]
                            
                            # Estimate distance and velocity
                            dist = sm.distance(lat1,lon1,lat2,lon2)
                            
                            if dist < (info.filt.speed_high * 1.852 * 1000): # only concidere points less than x km appart
                                
                                x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
                                x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
                                
                                ix, iy = sm.interp2d(x1, y1, x2, y2)
                                
#                                iix.append(x1)
#                                iiy.append(y1)
                                iix.extend(ix)
                                iiy.extend(iy)
                        
                        # add the last location 
                        xend, yend = sm.align_with_grid(x, y, singleship_bin['longitude'].values[j], singleship_bin['latitude'].values[j])

                    iix.append(xend)
                    iiy.append(yend)
                    
                    #drop duplicates
                    df = {}
                    df = pd.DataFrame({'x':iix,'y':iiy}).drop_duplicates(keep='first')
#                    print(len(df['x'].values))
#                    print(df['x'].values)
                    
                    # Append
                    iiix.extend(df['x'].tolist())
                    iiiy.extend(df['y'].tolist())
                    
#                    print('----------------------' + str(len(iiix)))

                
        # Project pings to grid        
        H0, xedges, yedges = np.histogram2d(iiix,iiiy,bins=info.grid.bin_number)
        # Rotate and flip H...
        H0 = np.rot90(H0)
        H0 = np.flipud(H0)
                
        D = xr.Dataset({'ship_density':(['x','y'],H0)},
                coords={'lon':(['x'],x),
                        'lat':(['y'],y)})
                    
    
        # Print NetCDF file
        sm.checkDir(str(info.dirs.gridded_data))
        print('Writting...')
        print('...' + file_out)    
        D.to_netcdf(path=file_out)
    
    return








#
#def gridder(info, data_in, file_name, overwrite=False):
#    
#    print('gridder ----------------------------------------------------------')
#    
#    import os
#    
#    file_out = os.path.join(str(info.dirs.gridded_data), info.run_name + '_' + str(info.grid.bin_number)+ '_' + file_name  + '.nc')
#    
#    if not os.path.isfile(file_out) or overwrite:
#        
#        # -----------------------------------------------------------------------------
#    
#        data = data_in
#    
#        # Make grid
#        x = np.linspace(data['longitude'].min(), data['longitude'].max(), num=info.grid.bin_number)
#        y = np.linspace(data['latitude'].min(), data['latitude'].max(), num=info.grid.bin_number)
#
#        # Find unique ships
#        unis = pd.unique(data['ship_id_vrn'].values)
##        unis = pd.unique(data['ship_id_vrn'].to_pandas().values)
#        print('Number of Unique Ships = ' + str(len(unis)))
#        iiix, iiiy, iiiveloc = [], [], []
#        counter = 0
#        for ship in unis:
#            counter += 1
#            print('Ship: ' + str(counter) + ' (id:'+ str(ship) + ')')
#            singleship = data.sel("data['ship_id_vrn'] == ship")
#            
#            # Loop over each ship
#    #        for i in range(1,len(singleship)):
#            pings_per_ship = len(singleship['longitude'].values)
#            for i in range(1,pings_per_ship):
#                
#                MinSeqNum = singleship['SeqNum'].values.min()
#                MaxSeqNum = singleship['SeqNum'].values.max() + (1/144)
#                
#                time_bins = np.arange(MinSeqNum, MaxSeqNum, 1/144) # 1/144 = once every 10 minutes
#                
#                iix, iiy, iiveloc = [], [], []
#                for j in range(0,len(time_bins)-1):
#                    singleship_bin = singleship.sel("(singleship['SeqNum'] > time_bins[j]) & (singleship['SeqNum'] < time_bins[j+1])")
##                    print(singleship_bin)     
#                
#                    if pings_per_ship > 1:
#                        # Iterpolate bewtween known points
#                        lon1 = singleship_bin['longitude'].values[i-1]
#                        lat1 = singleship_bin['latitude'].values[i-1]
#                        lon2 = singleship_bin['longitude'].values[i]
#                        lat2 = singleship_bin['latitude'].values[i]
#                        
#                        # Estimate distance and velocity
#                        dist = sm.distance(lat1,lon1,lat2,lon2)
#                        
#                        if dist < (info.filt.speed_high * 1.852 * 1000): # only concidere points less than x km appart
##                            elapsed_days = singleship_bin['SeqNum'].values[i] - singleship_bin['SeqNum'].values[i-1]
##                            elapsed_secs = elapsed_days * 86400
##                            veloc = sm.estimate_velocity(elapsed_secs, dist)
#                            
#                            x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
#                            x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
#                            
#                            ix, iy = sm.interp2d(x1, y1, x2, y2)
##                            iveloc = [veloc] * len(ix)
#                            
#                            iix.extend(ix)
#                            iiy.extend(iy)
##                            iiveloc.extend(iveloc)
#                    
#                    # add the last location 
#                    xend, yend = sm.align_with_grid(x, y, singleship_bin['longitude'].values[i], singleship_bin['latitude'].values[i])
##                    elapsed_days = singleship_bin['SeqNum'].values[i] - singleship_bin['SeqNum'].values[i-1]
##                    elapsed_secs = elapsed_days * 86400
##                    veloc = sm.estimate_velocity(elapsed_secs, dist)
#                    iix.append(xend)
#                    iiy.append(yend)
##                    iiveloc.append(veloc)
#                    
#                    #dropping duplicates
#                    df = pd.DataFrame({'x':iix,'y':iiy}).drop_duplicates(keep='first')
#                    
#                
#                # Append
#                iiix.append(df['x'].tolist())
#                iiiy.append(df['y'].tolist())
##                iiiveloc.append(veloc)
#                
#                
#        # Project pings to grid        
#        H0, xedges, yedges = np.histogram2d(iiix,iiiy,bins=info.grid.bin_number)
#        # Rotate and flip H...
#        H0 = np.rot90(H0)
#        H0 = np.flipud(H0)
#                
#        D = xr.Dataset({'ship_density':(['x','y'],H0)},
#                coords={'lon':(['x'],x),
#                        'lat':(['y'],y)})
#                    
#    
##        # Print NetCDF file
##        d = xr.Dataset({'xgridded':(['No_of_points'],iix),
##                        'ygridded':(['No_of_points'],iiy),
##                        'velocgridded':(['No_of_points'],iiveloc)},
##                        coords={'lon':(['grid_length'],x),
##                                'lat':(['grid_length'],y)})
#        
#    #    d.to_netcdf(path=datadir + 'L3_gridded_netCDF\\' + filename + '- Grid' + str(BinNo) + ' - upFilter' + '-' + str(upLim) + '.nc')
#        sm.checkDir(str(info.dirs.gridded_data))
#    
#    #    
#    #    file_out = str(mydirs['gridded_data']) + mydirs['run_name'] + '_' + str(BinNo) + '.nc'
#        
#        print('Writting...')
#        print('...' + file_out)
#        
#        D.to_netcdf(path=file_out)
#    
#    return














#
#def gridder(info, data_in, file_name, overwrite=False):
#    
#    print('gridder ----------------------------------------------------------')
#    
#    import os
#    
#    file_out = os.path.join(str(info.dirs.gridded_data), info.run_name + '_' + str(info.grid.bin_number)+ '_' + file_name  + '.nc')
#    
#    if not os.path.isfile(file_out) or overwrite:
#        
#        # -----------------------------------------------------------------------------
#    
#        data = data_in
#    
#        # Make grid
#        x = np.linspace(data['longitude'].min(), data['longitude'].max(), num=info.grid.bin_number)
#        y = np.linspace(data['latitude'].min(), data['latitude'].max(), num=info.grid.bin_number)
#
#        # Find unique ships
#        unis = pd.unique(data['ship_id_vrn'].values)
##        unis = pd.unique(data['ship_id_vrn'].to_pandas().values)
#        print('Number of Unique Ships = ' + str(len(unis)))
#        iix, iiy, iiveloc = [], [], []
#        counter = 0
#        for ship in unis:
#            counter += 1
#            print('Ship: ' + str(counter) + ' (id:'+ str(ship) + ')')
#            singleship = data.sel("data['ship_id_vrn'] == ship")
#            
#            # Loop over each ship
#    #        for i in range(1,len(singleship)):
#            pings_per_ship = len(singleship['longitude'].values)
#            for i in range(1,pings_per_ship):
#                if pings_per_ship > 1:
#                    # Iterpolate bewtween known points
#                    lon1 = singleship['longitude'].values[i-1]
#                    lat1 = singleship['latitude'].values[i-1]
#                    lon2 = singleship['longitude'].values[i]
#                    lat2 = singleship['latitude'].values[i]
#                    
#                    # Estimate distance and velocity
#                    dist = sm.distance(lat1,lon1,lat2,lon2)
#                    
#                    if dist < (info.filt.speed_high * 1.852 * 1000): # only concidere points less than x km appart
#                        elapsed_days = singleship['SeqNum'].values[i] - singleship['SeqNum'].values[i-1]
#                        elapsed_secs = elapsed_days * 86400
#                        veloc = sm.estimate_velocity(elapsed_secs, dist)
#                        
#                        x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
#                        x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
#                        
#                        ix, iy = sm.interp2d(x1, y1, x2, y2)
#                        iveloc = [veloc] * len(ix)
#                        
#                        iix.extend(ix)
#                        iiy.extend(iy)
#                        iiveloc.extend(iveloc)
#                
#                # add the last location 
#                xend, yend = sm.align_with_grid(x, y, singleship['longitude'].values[i], singleship['latitude'].values[i])
#                elapsed_days = singleship['SeqNum'].values[i] - singleship['SeqNum'].values[i-1]
#                elapsed_secs = elapsed_days * 86400
#                veloc = sm.estimate_velocity(elapsed_secs, dist)
#                iix.append(xend)
#                iiy.append(yend)
#                iiveloc.append(veloc)
#                
#                
#        # Project pings to grid        
#        H0, xedges, yedges = np.histogram2d(iix,iiy,bins=info.grid.bin_number)
#        # Rotate and flip H...
#        H0 = np.rot90(H0)
#        H0 = np.flipud(H0)
#                
#        D = xr.Dataset({'ship_density':(['x','y'],H0)},
#                coords={'lon':(['x'],x),
#                        'lat':(['y'],y)})
#                    
#    
##        # Print NetCDF file
##        d = xr.Dataset({'xgridded':(['No_of_points'],iix),
##                        'ygridded':(['No_of_points'],iiy),
##                        'velocgridded':(['No_of_points'],iiveloc)},
##                        coords={'lon':(['grid_length'],x),
##                                'lat':(['grid_length'],y)})
#        
#    #    d.to_netcdf(path=datadir + 'L3_gridded_netCDF\\' + filename + '- Grid' + str(BinNo) + ' - upFilter' + '-' + str(upLim) + '.nc')
#        sm.checkDir(str(info.dirs.gridded_data))
#    
#    #    
#    #    file_out = str(mydirs['gridded_data']) + mydirs['run_name'] + '_' + str(BinNo) + '.nc'
#        
#        print('Writting...')
#        print('...' + file_out)
#        
#        D.to_netcdf(path=file_out)
#    
#    return



































def grid_merger(info, files=None):
    
    print('grid_merger ------------------------------------------------------')
    
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
    
    print('Merging completed!')
    
    return D

#def grid_merger(info, files=None):
#    
#    if files == None:
#        all_files = sm.get_all_files(info.dirs.gridded_data)
#    else:
#        all_files = files
#    
#    # Process 1st grid
#    d = xr.open_dataset(all_files[0])
#    H0, xedges, yedges = np.histogram2d(d['xgridded'].values,d['ygridded'].values,bins=len(d['lat']))
#    # Rotate and flip H...
#    H0 = np.rot90(H0)
#    H0 = np.flipud(H0)
#    
#    # Process the rest of the grid files
#    for file_in in all_files[1:] :
#        d = xr.open_dataset(file_in)
#        H, xedges, yedges = np.histogram2d(d['xgridded'].values,d['ygridded'].values,bins=len(d['lat']))
#        # Rotate and flip H...
#        H = np.rot90(H)
#        H = np.flipud(H)
#        # Add new matrix (H) to summed matrix (H0) 
#        H0 = H0 + H
#            
#    # Create dataset
#    D = xr.Dataset({'ship_density':(['x','y'],H0)},
#            coords={'lon':(['x'],d['lon'].values),
#                    'lat':(['y'],d['lat'].values)})
#            
#    # Save merged file
#    sm.checkDir(str(info.dirs.merged_grid))
#    file_out = os.path.join(str(info.dirs.merged_grid), 'merged_grid.nc')
#    D.to_netcdf(path=file_out)
#    
#    return D















