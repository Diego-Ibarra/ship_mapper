import ship_mapper as sm

info = sm.load_info('example2_Halifax_AIS')

info.filt.speed_low = 0.5 # Knots
info.filt.speed_high = 4.5 # Knots

info.grid.interp_threshold = 30 #knots
info.maps.mask_below = 0
info.grid.time_bin = 0.034722 #days
info.sidebar.included_vessel_types = 'all'


# Filter and grid all input files
for file_in in sm.get_all_files(info.dirs.data_nc):
    
    # Get file name
    file_name = sm.get_filename_from_fullpath(file_in)
    
    # Filter data (spatial trimmer)
    filtered_data = sm.spatial_filter(file_in, info) 
     
    # Project "dots" into a grid
    sm.gridder(info, filtered_data, file_name, overwrite=True)



#Merge grids   
sm.grid_merger(info)

info.maps.cbarmin = 'auto'
info.maps.cbarmax = 'auto'

# Make map
m = sm.map_density(info, cmap='inferno_r',sidebar=True)

# Make shapefiles
#sm.mergedgrid_to_shp(info)
