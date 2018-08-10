import ship_mapper as sm

info = sm.make_info_from_GridData(calling_file=__file__,
                                  run_name='1_run',
                                  region='Maritimes',
                                  basemap='basemap_sidebar',
                                  grid_type='generic',
                                  data_name = 'VMS_DFO')

# Change or define some items within info
info.sidebar.included_vessel_types = 'All'
info.grid.interp_threshold = 40 #knots
info.maps.mask_below = 1
info.maps.textbox = True
info.maps.cbarmin = 'auto'
info.maps.cbarmax = 'auto'


# ----------------------------------------------------------------------
#Convert original data to nc
sm.bulk_convert_to_nc(info.converter,
                      path_to_data_in=info.dirs.data_original,
                      overwrite=True)


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
