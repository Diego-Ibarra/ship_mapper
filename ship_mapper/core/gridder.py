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
    
        data = data_in
    
        # Make grid
        x = np.linspace(data['longitude'].min(), data['longitude'].max(), num=info.grid.bin_number)
        y = np.linspace(data['latitude'].min(), data['latitude'].max(), num=info.grid.bin_number)

        # Find unique ships
        unis = pd.unique(data['ship_id_vrn'].values)
#        unis = pd.unique(data['ship_id_vrn'].to_pandas().values)
        print('Number of Unique Ships = ' + str(len(unis)))
        iix, iiy, iiveloc = [], [], []
        counter = 0
        for ship in unis:
            counter += 1
            print('Ship: ' + str(counter) + ' (id: '+ str(ship) + ')')
            singleship = data.sel("data['ship_id_vrn'] == ship")
            
            # Loop over each ship
    #        for i in range(1,len(singleship)):
            pings_per_ship = len(singleship['longitude'].values)
            for i in range(1,pings_per_ship):
                if pings_per_ship > 1:
                    # Iterpolate bewtween known points
                    lon1 = singleship['longitude'].values[i-1]
                    lat1 = singleship['latitude'].values[i-1]
                    lon2 = singleship['longitude'].values[i]
                    lat2 = singleship['latitude'].values[i]
                    
                    # Estimate distance and velocity
                    dist = sm.distance(lat1,lon1,lat2,lon2)
                    
                    if dist < (info.filt.speed_high * 1.852 * 1000): # only concidere points less than x km appart
                        elapsed_days = singleship['SeqNum'].values[i] - singleship['SeqNum'].values[i-1]
                        elapsed_secs = elapsed_days * 86400
                        veloc = sm.estimate_velocity(elapsed_secs, dist)
                        
                        x1, y1 = sm.align_with_grid(x, y, lon1, lat1)
                        x2, y2 = sm.align_with_grid(x, y, lon2, lat2)
                        
                        ix, iy = sm.interp2d(x1, y1, x2, y2)
                        iveloc = [veloc] * len(ix)
                        
                        iix.extend(ix)
                        iiy.extend(iy)
                        iiveloc.extend(iveloc)
                
                # add the last location 
                xend, yend = sm.align_with_grid(x, y, singleship['longitude'].values[i], singleship['latitude'].values[i])
                elapsed_days = singleship['SeqNum'].values[i] - singleship['SeqNum'].values[i-1]
                elapsed_secs = elapsed_days * 86400
                veloc = sm.estimate_velocity(elapsed_secs, dist)
                iix.append(xend)
                iiy.append(yend)
                iiveloc.append(veloc)
                
                
        # Project pings to grid        
        H0, xedges, yedges = np.histogram2d(iix,iiy,bins=info.grid.bin_number)
        # Rotate and flip H...
        H0 = np.rot90(H0)
        H0 = np.flipud(H0)
                
        D = xr.Dataset({'ship_density':(['x','y'],H0)},
                coords={'lon':(['x'],x),
                        'lat':(['y'],y)})
                    
    
#        # Print NetCDF file
#        d = xr.Dataset({'xgridded':(['No_of_points'],iix),
#                        'ygridded':(['No_of_points'],iiy),
#                        'velocgridded':(['No_of_points'],iiveloc)},
#                        coords={'lon':(['grid_length'],x),
#                                'lat':(['grid_length'],y)})
        
    #    d.to_netcdf(path=datadir + 'L3_gridded_netCDF\\' + filename + '- Grid' + str(BinNo) + ' - upFilter' + '-' + str(upLim) + '.nc')
        sm.checkDir(str(info.dirs.gridded_data))
    
    #    
    #    file_out = str(mydirs['gridded_data']) + mydirs['run_name'] + '_' + str(BinNo) + '.nc'
        
        print('Writting...')
        print('...' + file_out)
        
        D.to_netcdf(path=file_out)
    
    return






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















