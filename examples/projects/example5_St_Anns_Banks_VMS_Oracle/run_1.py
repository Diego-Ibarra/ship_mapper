import ship_mapper as sm
from ship_mapper.oracle import download_vms, filter_by_gear
import datetime
import xarray as xr


info = sm.make_info_from_GridData(calling_file=__file__,
                                  run_name='1_run',
                                  region='St_Anns_Bank',
                                  basemap='basemap_sidebar',
                                  grid_type='generic',
                                  data_name = 'VMS_DFO_Oracle')

# Change or define some items within info
info.sidebar.included_vessel_types = 'All'
info.grid.interp_threshold = 40 #knots
info.maps.mask_below = 1
info.maps.textbox = True
info.maps.cbarmin = 'auto'
info.maps.cbarmax = 'auto'


# dates
now = datetime.datetime.now()
#now = datetime.datetime(2018, 5, 10, 0, 0, 0 )
enddate = datetime.datetime(now.year, now.month, now.day, 6, 0, 0 )
#startdate = enddate - datetime.timedelta(days=7)
startdate = enddate - datetime.timedelta(days=1)



#download_vms(info, startdate, enddate)

# ----------------------------------------------------------------------
#Convert original data to nc
#sm.bulk_convert_to_nc(info.converter,
#                      path_to_data_in=info.dirs.data_original,
#                      overwrite=False)

data = xr.open_dataset(info.dirs.data_nc + r'\vms_autoDownloaded.nc')

# Only keeo "fixed gear" data
data_filtered = filter_by_gear(info, data, startdate, enddate,
                                   gearcode_sheet=str(info.dirs.project_path) + r'\fixed_gear.xlsx')
     
# Project "dots" into a grid
#sm.gridder(info, data, 'vms_autoDownloaded', overwrite=True)
    
    
## Merge grids   
#sm.grid_merger(info)

# Make map
#m = sm.map_density(info, 
#                   file_in=str(info.dirs.gridded_data)+r'\vms_autoDownloaded',
#                   cmap='inferno_r',
#                   sidebar=True)
#
#sm.grid_to_esriascii(info, file_in=None)

# Make shapefiles
#sm.mergedgrid_to_shp(info)
