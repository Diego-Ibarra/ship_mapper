import numpy as np
import matplotlib.pyplot as plt
import _pickle as pickle
from pathlib import Path
import netCDF4
import ship_mapper as sm


project_path = 'C:\\Users\\IbarraD\\Documents\\GitHub\\ship_mapper\\examples\\projects\\test_1'
path_to_map = Path(project_path) / 'ancillary'

m = sm.make_basemap(project_path,[43,45.55,-61.1,-55.7])


bathymetry_file = str(path_to_map / 'usgsCeSrtm30v6.nc')

# open NetCDF data in 
nc = netCDF4.Dataset(bathymetry_file)
ncv = nc.variables
lon = ncv['longitude'][:]
lat = ncv['latitude'][:]
lons, lats = np.meshgrid(lon,lat)
topo = ncv['topo'][:,:]

# For topo
x,y = m(lons,lats)
depth_levels = [-1000,-900,-800,-700,-600,-500,-400,-300,-200,-150,-100,-75,-50,-20]
cs = plt.contour(x,y,topo,depth_levels,cmap=plt.get_cmap('Blues_r'),linewidths=1,linestyles='solid',zorder=7)



# Polygon +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from matplotlib.patches import Polygon
    
poly_lats = [44.0203, 41.225982, 41.6064488, 44.910864,]
poly_lons = [-59.9863, -57.10252, -56.3708845,-56.86052,]
poly_x, poly_y = m(poly_lons, poly_lats)
#    poly_xy = zip(poly_x,poly_y)
poly_xy = np.transpose(np.array((poly_x,poly_y)))
print(poly_xy)
poly = Polygon(poly_xy, closed=True, edgecolor='red', alpha=0.8, fill=False, zorder=15)
plt.gca().add_patch(poly)

    
# Save basemap
picklename = str(path_to_map / 'basemap.p')
pickle.dump(m,open(picklename,'wb'),-1)
print('!!! Pickle just made: ' + picklename)