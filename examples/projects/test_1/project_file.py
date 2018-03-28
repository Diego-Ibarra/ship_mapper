import ship_mapper as sm


top_dir = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\'
data_nc_dir = top_dir + 'data\\VMS_2012-18_selectedVessels\\data_nc\\'

# Pack dirs into mydirs (other default dirs are also populated in mydirs)
mydirs = sm.make_mydirs(top_dir, data_nc_dir, __file__)



##
##
##
##converter = 'VMS_2012_18_selectedVessels'
###path_to_converter = 'C:\\Users\\IbarraD\\Documents\\Example\\converters\\'
##path_to_converter = 'C:\\Users\\cerc-user\\Documents\\Github\\ship_mapper\\examples\\data\\VMS_2012-18_selectedVessels\\'
##
##sm.convert_to_nc(mydirs['data_original'], mydirs['data_nc'], converter, path=mydirs['my_converters'])
#
# Number of gridcells in the x and y dimenssions
BinNo = 1000
# Upper and lower limits (apparent Spped) to filter ship density data 
downLim = 1 # Knots
upLim = 4.5 # Knots
spatial=[43,45.55,-61.1,-55.7]
#
##
##file_nc= 'C:\Users\IbarraD\Documents\GitHub\ship_mapper\examples\data\VMS_2012-18_selectedVessels\data_nc'
##file_grid= 'C:\\Users\\IbarraD\\Documents\\Example\\grid - 2012-2018 - Select Vessels - Clipped.nc'
#
##Good##
filtered_data = sm.spatial_filter(mydirs['data_nc'] + '2012-2018 - Select Vessels - Clipped.nc', spatial) 
##
###sm.gridder(BinNo, upLim, filtered_data, file_grid)
sm.gridder(BinNo, upLim, filtered_data, mydirs)
##
##sm.gridder(BinNo, file_in, file_out, spatial=spatial)
##
##sm.map_density(BinNo,downLim,upLim,file_grid,spatial=None)

file_in = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\projects\\test_1\\gridded_data\\project_file_1000.nc'

sm.map_density(BinNo,downLim,upLim,file_in,mydirs,spatial=spatial)