import ship_mapper as sm

info = sm.make_info_from_GridData(calling_file=__file__,
                                  run_name='example2_Halifax_AIS',
                                  region='Halifax_Area',
                                  basemap='basemap_sidebar',
                                  grid_type='one-off',
                                  data_name = 'AIS_CCG')

# Change or define some items within info
info.filt.speed_low = 0.5 # Knots
info.filt.speed_high = 4.5 # Knots
info.grid.interp_threshold = 30 #knots
info.maps.mask_below = 0
info.grid.time_bin = 0.034722 #days
info.sidebar.included_vessel_types = 'all'
info.maps.cbarmin = 'auto'
info.maps.cbarmax = 'auto'

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

# Make map
m = sm.map_density(info, cmap='inferno_r',sidebar=True)

# Make shapefiles
#sm.mergedgrid_to_shp(info)
