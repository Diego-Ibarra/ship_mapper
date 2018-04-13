'''
Below are functions that will be loaded when calling: import ship_mapper as sm
'''
from .converters import convert_to_nc, bulk_convert_to_nc

from .utils import (distance, estimate_velocity, elapsed_days,
                    align_with_grid, interp2d, spatial_filter,
                    checkDir, make_mydirs, get_all_files,
                    get_filename_from_fullpath)

from .gridder import gridder, grid_merger, mergedgrid_to_shp

from .mapper import map_density, map_dots, make_basemap, map_dots_one_ship

from .info_object import info

