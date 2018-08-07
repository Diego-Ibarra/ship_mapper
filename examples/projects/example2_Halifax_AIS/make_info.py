import ship_mapper as sm

# Make info object
info = sm.info(calling_file=__file__, run_name='example2_Halifax_AIS')

# Get metadata from "grid" and copy it into info
info = sm.grid_to_info(info, 'Halifax_Area', 'basemap_sidebar', grid_type='one-off')

# Get metadata from "data_info.yaml" and copy it into info
info = sm.data_to_info(info, 'AIS_CCG')

info = sm.calculate_gridcell_areas(info)

info.save()
