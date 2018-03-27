
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



def import_general_settings(path=None):
    '''
    imports general_settings
    '''
    import imp


    if path is None:
#        path = os.path.realpath('..') 
        print()
        file, pathname, description = imp.find_module('general_settings',[os.path.realpath('../..')+'\\'])
        general_settings = imp.load_module('general_settings', file, pathname, description)
    else:
        file, pathname, description = imp.find_module('general_settings',[path])
        general_settings = imp.load_module('general_settings', file, pathname, description)
    
    return general_settings




def load_mydirs(filedash, run_name, path2settings=None):
#    general_settings = import_general_settings(path=path2settings)
    general_settings = import_general_settings(path=path2settings)
    
    project_name = os.path.split(os.path.split(filedash)[0])[1]
    
    mydirs = {}
#    mydirs['top'] = general_settings.top_dir
#    mydirs['data_original'] = general_settings.data_original
#    mydirs['data_nc'] = general_settings.data_nc
#    mydirs['my_converters'] = general_settings.my_converters
#    mydirs['projects'] = general_settings.projects
#    mydirs['myproject'] = general_settings.projects + '\\' + project_name + '\\'
#    mydirs['gridded_data'] = mydirs['myproject'] + 'gridded_data\\'
    
    mydirs['top'] = general_settings.top_dir
    mydirs['data_original'] = general_settings.data_original
    mydirs['data_nc'] = general_settings.data_nc
    mydirs['my_converters'] = general_settings.my_converters
    mydirs['projects'] = general_settings.projects
    mydirs['myproject'] = general_settings.projects + '\\' + project_name + '\\'
    mydirs['gridded_data'] = mydirs['myproject'] + 'gridded_data\\'
    
    return mydirs
    
    