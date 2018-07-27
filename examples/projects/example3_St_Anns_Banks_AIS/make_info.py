import ship_mapper as sm

info = sm.info(calling_file=__file__, run_name='1_run')

info = sm.grid_to_info(info, 'St_Anns_Bank', 'basemap_sidebar', grid_type='generic')

info = sm.data_to_info(info, 'AIS_CCG')

info = sm.calculate_gridcell_areas(info)

info.save()
