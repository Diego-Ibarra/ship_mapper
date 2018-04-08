import ship_mapper as sm


#top_dir = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\'
top_dir = 'C:\\Users\\cerc-user\\Documents\\Github\\ship_mapper\\examples\\'


data_nc_dir = top_dir + 'data\\CCG_AIS\\data_original\\'

# Pack dirs into mydirs (other default dirs are also populated in mydirs)
info = sm.info(top_dir, data_nc_dir, __file__)

# Define more items in info
info.grid.bin_number = 1000 ## Number of gridcells in the x and y dimenssions
#info.grid.minlat = 43
#info.grid.maxlat = 45.55
#info.grid.minlon = -61.1
#info.grid.maxlon = -55.7
info.grid.minlat = 43
info.grid.maxlat = 46
info.grid.minlon = -62.0
info.grid.maxlon = -55.7

## Upper and lower limits (apparent Spped) to filter ship density data
#info.filt.speed_low = 1 # Knots
#info.filt.speed_high = 4.5 # Knots
info.filt.speed_low = 0 # Knots
info.filt.speed_high = 20 # Knots

info.ship_id = 'MMSI'

# -----------------------------------------------------------------------------

# Convert original data to nc
converter = 'CCG_AIS'
#sm.bulk_convert_to_nc(converter, path_to_data_in=info.dirs.data_original, overwrite=True)


# Filter and grid all input files
for file_in in sm.get_all_files(info.dirs.data_nc):
    
    # Get file name
    file_name = sm.get_filename_from_fullpath(file_in)
    
    # Filter data
    filtered_data = sm.spatial_filter(file_in, info) 
    
    # Further filter data by speed
    indx = ((filtered_data['Speed_Over_Ground_SOG_knots'] > info.filt.speed_low) &
            (filtered_data['Speed_Over_Ground_SOG_knots'] < info.filt.speed_high))
    
    filtered_data = filtered_data.sel(Dindex=indx)
##
filtered_data.close()   

sm.gridder(info, filtered_data, file_name, overwrite=True)




##
##
###data_in = filtered_data
##
####file_in = sm.get_all_files(info.dirs.data_nc)[0]    
####
####file_name = sm.get_filename_from_fullpath(file_in)
####import xarray as xr
####data = xr.open_dataset(file_in)
####
##### Project "dots" into a grid
####sm.gridder(info, data, file_name, overwrite=True)
###    
# Merge grids    
sm.grid_merger(info)

# Make plots
sm.map_density(info)
#
# Make plots
import os
file_in = os.path.join(info.dirs.data_nc, 'CCG_AIS_Dynamic_Data_2017-06-01.nc')
sm.map_dots(info, file_in)
     
    
    