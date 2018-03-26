'''
Below are functions that will be loaded when calling: import ship_mapper as sm
'''
from .converters import convert_to_nc

from .core import distance, estimate_velocity, elapsed_days, align_with_grid, interp2d, spatial_filter, import_general_settings, load_mydirs

from .core.gridder import gridder

from .core.mapper import map_density

