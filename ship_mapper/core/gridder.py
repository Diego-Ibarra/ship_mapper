# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 09:19:49 2018

@author: IbarraD
"""


import pandas as pd
import numpy as np
import xarray as xr
import ship_mapper as sm


def gridder(info, data_in):
    print('Gridding...')
    # -----------------------------------------------------------------------------

    data = data_in

    # Make grid
    x = np.linspace(data['longitude'].min(), data['longitude'].max(), num=info.grid.bin_number)
    y = np.linspace(data['latitude'].min(), data['latitude'].max(), num=info.grid.bin_number)
    
    
    # Find unique ships
    unis = pd.unique(data['ship_id_vrn'])
    print('Number of Unique Ships = ' + str(len(unis)))
    iix, iiy, iiveloc = [], [], []
    counter = 0
    for ship in unis:
        counter += 1
        print('Ship: ' + str(counter) + '('+ str(ship) + ')')
        singleship = data.sel("data['ship_id_vrn'] == ship")
        
        print('****************************************************************')
        print(len(singleship['longitude'].values))
        
        # Loop over each ship
#        for i in range(1,len(singleship)):
        for i in range(1,len(singleship['longitude'].values)):
            if len(singleship) > 1:
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

    # Print NetCDF file
    d = xr.Dataset({'xgridded':(['No_of_points'],iix),
                    'ygridded':(['No_of_points'],iiy),
                    'velocgridded':(['No_of_points'],iiveloc)},
                    coords={'lon':(['grid_length'],x),
                            'lat':(['grid_length'],y)})
    
#    d.to_netcdf(path=datadir + 'L3_gridded_netCDF\\' + filename + '- Grid' + str(BinNo) + ' - upFilter' + '-' + str(upLim) + '.nc')
    sm.checkDir(str(info.dirs.gridded_data))
    
    import os
    
    file_out = os.path.join(str(info.dirs.gridded_data), info.run_name + '_' + str(info.grid.bin_number) + '.nc')
#    
#    file_out = str(mydirs['gridded_data']) + mydirs['run_name'] + '_' + str(BinNo) + '.nc'
    
    print('Writting...')
    print('...' + file_out)
    
    d.to_netcdf(path=file_out)
    
    return

