import ship_mapper as sm

info = sm.info(__file__)

# Define more items in info
info.grid.region = 'Halifax_Area'
info.grid.basemap = 'basemap_sidebar'
info.grid.type = 'one-off' # opsions: 'one-off' OR 'generic'
info.grid.bin_number = None ## Number of gridcells in the x and y dimenssions
info.grid.bin_size = 0.001 # Degrees
info.grid.minlat = 44.1
info.grid.maxlat = 44.8
info.grid.minlon = -64.3
info.grid.maxlon = -62.8
info.grid.epsg_code = '4326'

info.maps.resolution = 'f'
info.maps.parallels = 0.1 # Deegres between lines
info.maps.meridians = 0.1# Deegres between lines
info.maps.scalebar_km = 10

## Upper and lower limits (apparent Spped) to filter ship density data
info.filt.speed_low = 0 # Knots
info.filt.speed_high = 100 # Knots

#project_path = info.dirs.project_path
#path_to_map = info.dirs.ancillary 

m = sm.make_basemap(info,
                    [info.grid.minlat,
                     info.grid.maxlat,
                     info.grid.minlon,
                     info.grid.maxlon],
                     sidebar=True)

