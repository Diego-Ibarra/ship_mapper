import ship_mapper as sm


run_name = 'run1'

mydirs = sm.load_mydirs(__file__, run_name)

converter = 'VMS_2012_18_selectedVessels'
path_to_converter = 'C:\\Users\\IbarraD\\Documents\\Example\\converters\\'

sm.convert_to_nc(mydirs['data_original'], mydirs['data_nc'], converter, path=mydirs['my_converters'])