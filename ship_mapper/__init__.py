'''
Below are functions that will be loaded when calling: import ship_mapper as sm
'''
from .converters import convert_to_nc, bulk_convert_to_nc

from .core import distance, estimate_velocity, elapsed_days, align_with_grid, interp2d, spatial_filter, checkDir, make_mydirs

from .core.gridder import gridder

from .core.mapper import map_density, make_basemap

