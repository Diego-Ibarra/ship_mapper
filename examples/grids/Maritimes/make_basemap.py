import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import netCDF4
import ship_mapper as sm

# Pack dirs into mydirs (other default dirs are also populated in mydirs)
info = sm.info(__file__)

# Define more items in info
info.grid.region = 'Maritimes'
info.grid.basemap = 'basemap_sidebar'
info.grid.type = 'generic' # opsions: 'one-off' OR 'generic'
info.grid.bin_number = None ## Number of gridcells in the x and y dimenssions
info.grid.bin_size = 0.01 # Degrees
info.grid.minlat = 39.9
info.grid.maxlat = 48.3
info.grid.minlon = -69
info.grid.maxlon = -54.7
info.grid.epsg_code = '4326'

info.maps.resolution = 'i'
info.maps.parallels = 1 # Deegres between lines
info.maps.meridians = 1# Deegres between lines
info.maps.scalebar_km = 150


project_path = info.dirs.project_path
path_to_map = info.dirs.ancillary 

m = sm.make_basemap(info, [info.grid.minlat,
                           info.grid.maxlat,
                           info.grid.minlon,
                           info.grid.maxlon], sidebar=True)


bathymetry_file = str(path_to_map / 'usgsCeSrtm30v6.nc')

# open NetCDF data in
nc = netCDF4.Dataset(bathymetry_file)
ncv = nc.variables
lon = ncv['longitude'][:]
lat = ncv['latitude'][:]
lons, lats = np.meshgrid(lon, lat)
topo = ncv['topo'][:, :]

# For topo
x, y = m(lons, lats)

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

