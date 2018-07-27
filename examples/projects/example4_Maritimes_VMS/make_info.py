import ship_mapper as sm

info = sm.info(calling_file=__file__, run_name='1_run')

info = sm.grid_to_info(info, 'Maritimes', 'basemap_sidebar', grid_type='generic')

info = sm.data_to_info(info, 'VMS_DFO')

info = sm.calculate_gridcell_areas(info)

info.save()