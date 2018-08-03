Spatial filter
===================


:func:`~utils.spatial_filter`



.. code-block:: python

    import ship_mapper as sm
    
    info = sm.load_info('1_run') 
    
    # Filter and grid all input files
    for file_in in sm.get_all_files(info.dirs.data_nc):
        
        # Get file name
        file_name = sm.get_filename_from_fullpath(file_in)
        
        # Filter data (spatial trimmer)
        filtered_data = sm.spatial_filter(file_in, info) 