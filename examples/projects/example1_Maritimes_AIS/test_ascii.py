import ship_mapper as sm
import xarray as xr

info = sm.make_info_from_GridData(calling_file=__file__,
                                  run_name='1_run',
                                  region='Maritimes',
                                  basemap='basemap_sidebar',
                                  grid_type='generic',
                                  data_name = 'AIS_CCG')

# Change or define some items within info
info.sidebar.included_vessel_types = 'All'
info.grid.interp_threshold = 40 #knots
info.maps.mask_below = 1
info.maps.textbox = True
info.maps.cbarmin = 'auto'
info.maps.cbarmax = 'auto'

d = xr.open_dataset(r'C:\Users\IbarraD\ship_mapper\examples\projects\example1_Maritimes_AIS\merged_grid\merged_grid.nc')


DataShape = d['ship_density'].shape

TheFile=open("testfile.asc","w")
TheFile.write('ncols ' + str(DataShape[0]) + '\n')
TheFile.write('nrows ' + str(DataShape[1]) + '\n')
TheFile.write('xllcenter ' + str(info.grid.minlon) + '\n')
TheFile.write('yllcenter ' + str(info.grid.minlat) + '\n')
TheFile.write('cellsize ' + str(info.grid.bin_size) + '\n')
TheFile.write('nodata_value  0.0\n')


print('Printing esri ascii file')
for i in range(DataShape[1]-1,-1,-1):
    for j in range(0,DataShape[0]):
        TheFile.write(str(d['ship_density'].values[j,i]) + chr(32))
    TheFile.write("\n")
TheFile.close()