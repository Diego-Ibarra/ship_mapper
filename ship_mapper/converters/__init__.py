
def convert_to_nc(data_in, data_out, converter):
    # Import appropiate converter (which is file in folder "converters")
    try:
        exec('from . import ' + converter)
    except ImportError as e:
        errorMessage = ("converter '" + converter + "' does not exist. "
                        'Check spelling. Otherwise, you may need to make a new '
                        'converter file (e.g. MyFile.py) and save it in '
                        './converters')
        raise ImportError(errorMessage)
        return
    
    # call converter function from approatie converter file
    eval(converter + '.convert(data_in, data_out)')
    return