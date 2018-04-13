import ship_mapper as sm


top_dir = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\'
#top_dir = 'C:\\Users\\cerc-user\\Documents\\Github\\ship_mapper\\examples\\'


data_nc_dir = top_dir + 'data\\VMS_2012-18_selectedVessels\\data_original\\'

# Pack dirs into mydirs (other default dirs are also populated in mydirs)
info = sm.info(top_dir, data_nc_dir, __file__)

# Define more items in info
info.grid.bin_number = 1000 ## Number of gridcells in the x and y dimenssions
info.grid.minlat = 43
info.grid.maxlat = 45.55
info.grid.minlon = -61.1
info.grid.maxlon = -55.7
info.grid.epsg_code = '4326'

## Upper and lower limits (apparent Spped) to filter ship density data
info.filt.speed_low = 1 # Knots
info.filt.speed_high = 4.5 # Knots

info.ship_id = 'ship_id_vrn'

# -----------------------------------------------------------------------------
#
#converter = 'VMS_2012_18_selectedVessels'
#path_to_converter = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\data\\VMS_2012-18_selectedVessels'
##path_to_converter = 'C:\\Users\\cerc-user\\Documents\\GitHub\\ship_mapper\\examples\\data\\VMS_2012-18_selectedVessels'
#
### Convert original data to nc
##sm.bulk_convert_to_nc(converter,
##                      path_to_data_in=info.dirs.data_original,
##                      path_to_converter=path_to_converter,
##                      overwrite=True)
#
#
## Filter and grid all input files
#for file_in in sm.get_all_files(info.dirs.data_nc):
#    
#    # Get file name
#    file_name = sm.get_filename_from_fullpath(file_in)
#    
#    # Filter data (spatial trimmer)
#    filtered_data = sm.spatial_filter(file_in, info) 
#    
#    # Further filter data by speed
#    indx = ((filtered_data['ApparentSpeed'] > info.filt.speed_low) &
#            (filtered_data['ApparentSpeed'] < info.filt.speed_high))
#    
#    filtered_data = filtered_data.sel(Dindex=indx)
#     
#    # Project "dots" into a grid
#    sm.gridder(info, filtered_data, file_name, overwrite=True)
#    
## Merge grids   
#sm.grid_merger(info)
#
## Make map
#m = sm.map_density(info)

#sm.mergedgrid_to_shp(info)
