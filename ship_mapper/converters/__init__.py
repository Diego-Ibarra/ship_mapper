def convert_to_nc(data_in, data_out, converter, path=None):
    '''
     Import appropiate converter, which is a file in folder "converters" within
     this module, or a customade file in the "path" folder 
     '''
    import imp
    try:
        if path is None:
            exec('from . import ' + converter)
        else:
            file, pathname, description = imp.find_module(converter,[path])
            exec(converter + " = imp.load_module('"+ converter +"', file, pathname, description)")
    except ImportError:
        errorMessage = ("converter '" + converter + "' does not exist in this 'path'. "
                        'Check spelling. Otherwise, you may need to make a new '
                        'converter file (e.g. MyPath/MyConverterFile.py)')
        raise ImportError(errorMessage)
    
    # call converter function from approatie converter file
    eval(converter + '.convert(data_in, data_out)')
    return