def convert_to_nc(data_in, data_out, converter, path_to_converter=None):
    '''
     Import appropiate converter, which is a file in folder "converters" within
     this module, or a customade file in the "path" folder 
     '''
    import imp
    try:
        if path_to_converter is None:
            exec('from . import ' + converter)
        else:
            file, pathname, description = imp.find_module(converter,[path_to_converter])
            exec(converter + " = imp.load_module('"+ converter +"', file, pathname, description)")
    except ImportError:
        errorMessage = ("converter '" + converter + "' does not exist in this 'path'. "
                        'Check spelling. Otherwise, you may need to make a new '
                        'converter file (e.g. MyPath/MyConverterFile.py)')
        raise ImportError(errorMessage)
    
    # call converter function from approatie converter file
    eval(converter + '.convert(data_in, data_out)')
    return



def bulk_convert_to_nc(converter, path_to_data_in=None, path_to_converter=None, path_to_yaml=None, overwrite=False):
    '''
    Converts ALL files in a directory 
    '''
    import imp
    import os
    from pathlib import Path
    import ship_mapper as sm
    
    print('bulk_convert_to_nc -----------------------------------------------')
    
    # Determine converter and paths
    if os.path.isfile(converter) and path_to_converter is None and path_to_data_in is None and path_to_yaml is None:
        print('Case1')
        dir_to_converter, converter_filename = os.path.split(converter)
        dir_in  = Path(dir_to_converter) / 'data_original'
        yaml_in = os.path.join(Path(dir_to_converter),'data_info.yaml')
    elif not os.path.isfile(converter) and path_to_converter is not None and path_to_data_in is not None and path_to_yaml is None:
        print('Case2')
        dir_to_converter = Path(path_to_converter)
        converter_filename = converter + '.py'
        dir_in  = Path(path_to_data_in) / 'data_original'
        yaml_in = os.path.join(Path(path_to_data_in),'data_info.yaml')
    elif not os.path.isfile(converter) and path_to_converter is not None and path_to_data_in is None and path_to_yaml is None:
        print('Case3')
        dir_to_converter = path_to_converter
        converter_filename = converter + '.py'
        dir_in  = Path(dir_to_converter) / 'data_original'
        yaml_in = os.path.join(Path(path_to_data_in),'data_info.yaml')
    elif not os.path.isfile(converter) and path_to_converter is None and path_to_data_in is not None and path_to_yaml is None:
        print('Case4')
        dir_to_converter = os.path.split(__file__)[0]
        converter_filename = converter + '.py'
        dir_in  = Path(path_to_data_in)
        yaml_in = os.path.join(Path(path_to_data_in),'..','data_info.yaml')
    else:
        # This case is when 'converter' is actually a 'info' object
        print('Case5')
        dir_to_converter = os.path.split(__file__)[0]
        converter_filename = converter + '.py'
        dir_in =  Path(path_to_data_in)
        yaml_in = os.path.join(Path(path_to_yaml),'data_info.yaml')

  
    # Load converter as module
    print(converter_filename)
    print(dir_to_converter)
    file, pathname, description = imp.find_module(converter_filename[:-3],[Path(dir_to_converter)])   
    convert = imp.load_module('convert', file, pathname, description)

 
    # Do all files in all directories within path_to_data_in
    for root, dirs, files in os.walk(dir_in):
        for file in files:
            file_in = os.path.join(root, file)
            filename, file_in_extension = os.path.splitext(file_in)
            
            root_out = root.replace('data_original', 'data_nc')
            
            file_out = file_in.replace('data_original', 'data_nc').replace(file_in_extension,'.nc')
            
            # Check if file_out exists and if overwrite is True
            if os.path.isfile(file_out) and overwrite:
                # Convert!
                print('Processing: ' + file_in)
                convert.convert(file_in,file_out,yaml_in)
                
            elif not os.path.isfile(file_out):
                sm.checkDir(root_out)
                
                # Convert!
                print('Processing: ' + file_in)
                convert.convert(file_in,file_out,yaml_in)
    return



def bulk_update_attributes(attrs, path_to_data_in, path_to_data_out, overwrite=False):
    '''
    Updates attributes in ALL files in a directory
    '''
    import xarray as xr
    import os
    import pandas as pd 

    for root, dirs, files in os.walk(path_to_data_in):
        for file in files:
            
            file_in  = os.path.join(path_to_data_in, file)
            file_out = os.path.join(path_to_data_out, file)
            
            if not os.path.isfile(file_out) or overwrite:
                print(file)
                
                d = xr.open_dataset(file_in)
                
                attrs['startdate'] = pd.to_datetime(str(min(d['DateTime'].values))).strftime('%Y-%m-%d %H:%M:%S')
                attrs['enddate'] = pd.to_datetime(str(max(d['DateTime'].values))).strftime('%Y-%m-%d %H:%M:%S')
                
                d.attrs = attrs
                
                
                
                d.to_netcdf(file_out,format='NETCDF4',engine='netcdf4')
    
    return