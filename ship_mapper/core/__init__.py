
import math
import numpy as np
import os

# distance -------------------------------------------------------
def distance(lat1,lon1,lat2,lon2):
    '''
    Estimates distance between 2 points on Earth.
    Assumes earth is a sphere (up to 0.5% error).
    Output is in meters
    '''

    R=6371000  # radius of Earth in meters
    phi_1=math.radians(lat1)
    phi_2=math.radians(lat2)
    
    delta_phi=math.radians(lat2-lat1)
    delta_lambda=math.radians(lon2-lon1)
    
    a=math.sin(delta_phi/2.0)**2+\
       math.cos(phi_1)*math.cos(phi_2)*\
       math.sin(delta_lambda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    return R*c # output distance in meters



def estimate_velocity(seconds, distance):
    '''
    Estimates velocity (in knots) given seconds elapsed to cover a distance (in meters)
    '''
    velocity_m = distance/seconds #units: meters / second
    velocity_k = velocity_m * 1.943844 #units: knots
    
    return velocity_k


def elapsed_days(timedelta):
    '''
    Estimates elapsed days
    '''
    days = timedelta.days
    decimal_days = timedelta.seconds/86400
    return days + decimal_days


def align_with_grid(lon_grid_vector, lat_grid_vector, lon_point, lat_point):
    '''
    Finds which gridcell contains a given lat/lon point 
    '''
    x = np.argmin(np.sqrt((lon_grid_vector - lon_point)**2))
    y = np.argmin(np.sqrt((lat_grid_vector - lat_point)**2))

    return x, y


def interp2d(x1, y1, x2, y2):
    xdiff = x2 - x1
    ydiff = y2 - y1
    delta = max(abs(xdiff),abs(ydiff))
    
    if delta != 0:
        xstep = xdiff/delta
        ystep = ydiff/delta
        
        xx = []
        yy =[]
        
        xx.append(round(x1))
        yy.append(round(y1))
        for i in range(1,delta):
            xx.append(round(x1+(xstep*i)))
            yy.append(round(y1+(ystep*i)))
    else:
        xx = [x1.item()]
        yy = [y1.item()]
    
    return xx, yy



def spatial_filter(file_in, spatial):
    import xarray as xr
    
    minlat = spatial[0]
    maxlat = spatial[1]
    minlon = spatial[2]
    maxlon = spatial[3]
    
    all_data = xr.open_dataset(file_in)
    
    indx = ((all_data['longitude']>  minlon) &
            (all_data['longitude']<= maxlon) &
            (all_data['latitude']>  minlat) &
            (all_data['latitude']<= maxlat))
        
    filtered_data = all_data.sel(Dindex=indx)
    
    print("Filtered!!!")
    
    return filtered_data



def checkDir(directory):
    '''
    Check if ``directory`` exists. In not, make it!

    parameters:
        directory (str): Absolute path of directory to check and/or make.
    '''

    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory didn't exist... now it does: " + directory)
    return




#def import_general_settings(path=None):
#    '''
#    imports general_settings
#    '''
#    import imp
#
#
#    if path is None:
##        path = os.path.realpath('..') 
#        print()
#        file, pathname, description = imp.find_module('general_settings',[os.path.realpath('../..')+'\\'])
#        general_settings = imp.load_module('general_settings', file, pathname, description)
#    else:
#        file, pathname, description = imp.find_module('general_settings',[path])
#        general_settings = imp.load_module('general_settings', file, pathname, description)
#    
#    return general_settings

def make_mydirs(top_dir, data_nc_dir, filedash):
    from pathlib import Path
    
    project_name = os.path.split(os.path.split(filedash)[0])[1]   
#    project_path = Path(os.path.split(os.path.split(filedash)[0])[0])
#    run_path = Path(os.path.split(filedash)[0])
    project_path = Path(os.path.split(filedash)[0])
    run_name = os.path.split(filedash)[1][:-3]

    mydirs = {}  
    mydirs['top'] = top_dir
    mydirs['data_nc'] = data_nc_dir
    mydirs['project_name'] = project_name
    mydirs['project_path'] = project_path
#    mydirs['project_path'] = project_path
#    mydirs['run_path'] = run_path
    mydirs['run_name'] = run_name
    mydirs['gridded_data'] = Path(project_path / 'gridded_data')
    
    return mydirs



#def load_mydirs(filedash, run_name, path2settings=None):
##    general_settings = import_general_settings(path=path2settings)
#    general_settings = import_general_settings(path=path2settings)
#    
#    project_name = os.path.split(os.path.split(filedash)[0])[1]
#    
#    mydirs = {}
##    mydirs['top'] = general_settings.top_dir
##    mydirs['data_original'] = general_settings.data_original
##    mydirs['data_nc'] = general_settings.data_nc
##    mydirs['my_converters'] = general_settings.my_converters
##    mydirs['projects'] = general_settings.projects
##    mydirs['myproject'] = general_settings.projects + '\\' + project_name + '\\'
##    mydirs['gridded_data'] = mydirs['myproject'] + 'gridded_data\\'
#    
#    mydirs['top'] = general_settings.top_dir
#    mydirs['data_original'] = general_settings.data_original
#    mydirs['data_nc'] = general_settings.data_nc
#    mydirs['my_converters'] = general_settings.my_converters
#    mydirs['projects'] = general_settings.projects
#    mydirs['myproject'] = general_settings.projects + '\\' + project_name + '\\'
#    mydirs['gridded_data'] = mydirs['myproject'] + 'gridded_data\\'
#    
#    return mydirs


#def convert_data(converter_file):
#    import imp
#
#    dir_to_file, converter_filename = os.path.split(converter_file)
#        
#    file, pathname, description = imp.find_module(converter_filename[:-3],[dir_to_file])
#    
#    convert = imp.load_module('convert', file, pathname, description)
##    print(type(convert))
#    
#    dir_here = os.path.dirname(os.path.abspath(converter_file))
#    
#    dir_in  = dir_here + '\\data_original\\'
#    dir_out  = dir_here + '\\data_nc\\'
#    
#    
##    print(dir_in)
##    print(dir_out)
##    
#    for root, dirs, files in os.walk(dir_in):
#        for file in files:
#            file_in = os.path.join(root, file)
#            filename, file_in_extension = os.path.splitext(file_in)
#            
#            root_out = root.replace('data_original', 'data_nc')
#            
#            print('-----')
#            print(file_in)
#
#            
#            file_out = file_in.replace('data_original', 'data_nc').replace(file_in_extension,'.nc')
#            
#            print(file_out)
#            
#            if os.path.isfile(file_out):
#                print('yes')
#            else:
#                if not os.path.exists(root_out):
#                    os.makedirs(root_out)
#                    print("Directory didn't exist... now it does: " + root_out)
#                
#                    convert(file_in,file_out)
#    return
    
    