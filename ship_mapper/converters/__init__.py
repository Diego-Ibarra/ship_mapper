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



def bulk_convert_to_nc(converter, path_to_data_in=None, path_to_converter=None, overwrite=False):
    import imp
    import os
    from pathlib import Path
    import ship_mapper as sm
    
    print('bulk_convert_to_nc -----------------------------------------------')
    
    # Determine converter and paths
    if os.path.isfile(converter) and path_to_converter is None and path_to_data_in is None:
        dir_to_converter, converter_filename = os.path.split(converter)
        dir_in  = Path(dir_to_converter) / 'data_original'
#        dir_out  = Path(dir_to_converter) / 'data_nc'
    elif not os.path.isfile(converter) and path_to_converter is not None and path_to_data_in is None:
        dir_to_converter = path_to_converter
        converter_filename = converter + '.py'
        dir_in  = Path(dir_to_converter) / 'data_original'
#        dir_out  = Path(dir_to_converter) / 'data_nc'
    else:
        dir_to_converter = path_to_converter
        converter_filename = converter + '.py'
        dir_in = path_to_data_in
        
  
    # Load converter as module
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
                convert.convert(file_in,file_out)
                
            elif not os.path.isfile(file_out):
                sm.checkDir(root_out)
#                if not os.path.exists(root_out):
#                    os.makedirs(root_out)
#                    print("Directory didn't exist... now it does: " + root_out)
                
                # Convert!
                print('Processing: ' + file_in)
                convert.convert(file_in,file_out)
    return