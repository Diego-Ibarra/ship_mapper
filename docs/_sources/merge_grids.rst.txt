Merge grids
============

Use function :func:`~gridder.grid_merger` to merge all ``grid-files.nc`` from a 
project into one single ``merged.nc`` file

Example: 



.. code-block:: python

    import ship_mapper as sm
    
    info = sm.load_info('1_run') 
    
    sm.grid_merger(info)