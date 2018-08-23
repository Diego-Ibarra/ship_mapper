import math
import numpy as np
import os


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
    
    
    :param float seconds: Elapsed time (in seconds).
        
    :param float distance: Elapsed distance (in meters).
    
    :return: Estimated velocity (in knots)
    :rtype: float
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
    '''
    Interpolated between 2 points
    '''
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



def spatial_filter(file_in, info):
    '''
    Returns only the "pings" within a defined box
    '''
    import xarray as xr
    
    print('spatial_filter ---------------------------------------------------')
    
    minlat = info.grid.minlat
    maxlat = info.grid.maxlat
    minlon = info.grid.minlon
    maxlon = info.grid.maxlon
    
    all_data = xr.open_dataset(file_in)
    
    indx = ((all_data['longitude']>  minlon) &
            (all_data['longitude']<= maxlon) &
            (all_data['latitude']>  minlat) &
            (all_data['latitude']<= maxlat))
        
    filtered_data = all_data.sel(Dindex=indx)

    return filtered_data



def checkDir(directory):
    '''
    Check if ``directory`` exists. In not, make it!

    :param str directory: Absolute path of directory to check and/or make.
    '''

    if not os.path.exists(directory):
        os.makedirs(directory)
        print("Directory didn't exist... now it does: " + directory)
    return



def make_mydirs(top_dir, data_nc_dir, filedash):
    '''
    Makes directories needed for project
    '''
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



def get_all_files(dir_in):
    '''
    Returns all files within a directory
    '''
    all_files =[]
    # Do all files in all directories within dir_in
    for root, dirs, files in os.walk(dir_in):
        for file in files:
            all_files.append(os.path.join(root, file))  
    return all_files



def get_filename_from_fullpath(fullpath):
    '''
    Returns the filename given a fullpath to a file
    '''
    return os.path.splitext(os.path.split(fullpath)[1])[0]



def get_path_from_fullpath(fullpath):
    '''
    Returns the path to a file given a fullpath to the file
    '''
    return os.path.splitext(os.path.split(fullpath)[0])[0]



def degrees_to_meters(degrees, reference_latitude):
    '''
    Converts degrees to meters
        
    dy   = latitude difference in meters;
    dlat = latitude difference in degrees;
    dx   = longitude difference in meters;
    dlon = longitude difference in degrees;
    alat = average latitude between the two fixes;
    
    Reference: American Practical Navigator, Vol II, 1975 Edition, p 5
    
    Source: http://pordlabs.ucsd.edu/matlab/coord.htm
    '''
    import math
    
    rlat = reference_latitude * math.pi/180;
    m = 111132.09 * 1 - 566.05 * math.cos(2 * rlat) + 1.2 * math.cos(4 * rlat);
    dy = degrees * m
    
    p = 111415.13 * math.cos(rlat) - 94.55 * math.cos(3 * rlat);
    dx = degrees * p
    return (dx+dy)/2



def write_info2data(D,info):
    '''
    Writes metadata from ``info`` object to the `attibutes` section in the data
    '''
    import types

    for row in info.__dict__.keys():
        if type(info.__dict__[row]) != types.SimpleNamespace:
            exec("D.attrs['" + row + "'] = info." + row)
        if type(info.__dict__[row]) == types.SimpleNamespace:
            for subrow in info.__dict__[row].__dict__.keys():
                exec("D.attrs['" + row + "." + subrow + "'] = info." + row + "." + subrow)
    return D



def stop(message):
    '''
    Stop
    '''
    import sys
    sys.exit(message)
    return
