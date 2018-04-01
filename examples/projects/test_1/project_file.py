import ship_mapper as sm


#top_dir = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\'
top_dir = 'C:\\Users\\cerc-user\\Documents\\Github\\ship_mapper\\examples\\'


data_nc_dir = top_dir + 'data\\VMS_2012-18_selectedVessels\\data_original\\'

# Pack dirs into mydirs (other default dirs are also populated in mydirs)
info = sm.info(top_dir, data_nc_dir, __file__)

# Define more items in info
info.grid.bin_number = 1000 ## Number of gridcells in the x and y dimenssions
info.grid.minlat = 43
info.grid.maxlat = 45.55
info.grid.minlon = -61.1
info.grid.maxlon = -55.7

## Upper and lower limits (apparent Spped) to filter ship density data
info.filt.speed_low = 1 # Knots
info.filt.speed_high = 4.5 # Knots

# -----------------------------------------------------------------------------
#
#converter = 'VMS_2012_18_selectedVessels'
##path_to_converter = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\data\\VMS_2012-18_selectedVessels'
#path_to_converter = 'C:\\Users\\cerc-user\\Documents\\GitHub\\ship_mapper\\examples\\data\\VMS_2012-18_selectedVessels'
#
## Convert original data to nc
#sm.bulk_convert_to_nc(converter,
#                      path_to_data_in=info.dirs.data_original,
#                      path_to_converter=path_to_converter,
#                      overwrite=True)


# Filter and grid all input files
for file_in in sm.get_all_files(info.dirs.data_nc):
    
    # Get file name
    file_name = sm.get_filename_from_fullpath(file_in)
    
    # Filter data
    filtered_data = sm.spatial_filter(file_in, info) 
    
    # Further filter data by speed
    indx = ((filtered_data['ApparentSpeed'] > info.filt.speed_low) &
            (filtered_data['ApparentSpeed'] < info.filt.speed_high))
    
    filtered_data = filtered_data.sel(Dindex=indx)
    
    
    
    # Project "dots" into a grid
    sm.gridder(info, filtered_data, file_name)
#
#file_in = str(info.dirs.gridded_data) + '\\project_file_1000.nc'
#sm.map_density(info, file_in, save=True)
     
    
    
    
    
    
    
    
## Filter data
#filtered_data = sm.spatial_filter(str(info.dirs.data_nc) + '\\2012-2018 - Select Vessels - Clipped.nc', info) 
#
#
## Further filter data by speed
#indx = ((filtered_data['ApparentSpeed'] > info.filt.speed_low) &
#        (filtered_data['ApparentSpeed'] < info.filt.speed_high))
#
#filtered_data = filtered_data.sel(Dindex=indx)
#
#
## Project "dots" into a grid
#sm.gridder(info, filtered_data)
#
#file_in = str(info.dirs.gridded_data) + '\\project_file_1000.nc'
#sm.map_density(info, file_in, save=True)




#
#
#
#
#
#
##
###
###file_nc= 'C:\Users\IbarraD\Documents\GitHub\ship_mapper\examples\data\VMS_2012-18_selectedVessels\data_nc'
###file_grid= 'C:\\Users\\IbarraD\\Documents\\Example\\grid - 2012-2018 - Select Vessels - Clipped.nc'
##
###Good##
#filtered_data = sm.spatial_filter(mydirs['data_nc'] + '2012-2018 - Select Vessels - Clipped.nc', spatial) 
###
####sm.gridder(BinNo, upLim, filtered_data, file_grid)
#sm.gridder(BinNo, upLim, filtered_data, mydirs)
###
###sm.gridder(BinNo, file_in, file_out, spatial=spatial)
###
###sm.map_density(BinNo,downLim,upLim,file_grid,spatial=None)
#
#file_in = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\projects\\test_1\\gridded_data\\project_file_1000.nc'
#
#sm.map_density(BinNo,downLim,upLim,file_in,mydirs,spatial=spatial)