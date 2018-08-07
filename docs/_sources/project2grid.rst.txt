Project data onto grid
======================

The functions in this section are the core of `ship_mapper`. They trasform data
organized in two column (one of latitudes and another of logitudes), into data
organized in a 2-dimessional grid. The functions herein basically count the number
of "pings" of a vessel occurring inside each grid-cell.

The main two fucntions are:

#. :func:`gridder <ship_mapper.gridder>`: Counts “pings” inside a grid-cell and computes “Ship minutes per km2”
#. :func:`gridder.gridder_pingsPerCell <ship_mapper.gridder.gridder_pingsPerCell>`: Counts “pings” inside a gridcell and computes “No. of vessels within grid-cell”

Example: 



.. code-block:: python

    import ship_mapper as sm
    
    info = sm.load_info('1_run') 
    
    # Filter and grid all input files
    for file_in in sm.get_all_files(info.dirs.data_nc):
        
        # Get file name
        file_name = sm.get_filename_from_fullpath(file_in)
        
        # Filter data (spatial trimmer)
        filtered_data = sm.spatial_filter(file_in, info) 

        # Project "dots" into a grid
        sm.gridder(info, filtered_data, file_name, overwrite=True)
