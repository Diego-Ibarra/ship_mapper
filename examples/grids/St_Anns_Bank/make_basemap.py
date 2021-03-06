import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import netCDF4
import ship_mapper as sm

# Make info object
info = sm.info(__file__)

# Define more items in info
info.grid.region = 'St_Anns_Banks'
info.grid.basemap = 'basemap_sidebar'
info.grid.type = 'generic' # opsions: 'one-off' OR 'generic'
info.grid.bin_number = None ## Number of gridcells in the x and y dimenssions
info.grid.bin_size = 0.0025 # Degrees
info.grid.minlat = 45.5
info.grid.maxlat = 47.5
info.grid.minlon = -61
info.grid.maxlon = -58
info.grid.epsg_code = '4326'
info.maps.resolution = 'f'
info.maps.parallels = 0.5 # Deegres between lines
info.maps.meridians = 0.5# Deegres between lines
info.maps.scalebar_km = 30


project_path = info.dirs.project_path
path_to_map = info.dirs.ancillary 

m = sm.make_basemap(info, [info.grid.minlat,
                           info.grid.maxlat,
                           info.grid.minlon,
                           info.grid.maxlon], sidebar=True)


# Get topography (i.e. bathymetry) from NOAA
bathymetry_file = str(path_to_map / 'usgsCeSrtm30v6.nc')
nc = netCDF4.Dataset(bathymetry_file)
ncv = nc.variables
lon = ncv['longitude'][:]
lat = ncv['latitude'][:]
lons, lats = np.meshgrid(lon, lat)
topo = ncv['topo'][:, :]

# For topo
x, y = m(lons, lats)

# Make topograhy countour lines
depth_levels_1 = np.linspace(topo.min(), -700, num=5)
depth_levels = np.append(depth_levels_1,np.linspace(-650, -50, num=15))
depth_levels = depth_levels.tolist()

cs = plt.contour(
    x,
    y,
    topo,
    depth_levels,
    cmap=plt.get_cmap('Blues_r'),
    linewidths=0.3,
    linestyles='solid',
    zorder=7)

# Save basemap
sm.save_basemap(m,info)

