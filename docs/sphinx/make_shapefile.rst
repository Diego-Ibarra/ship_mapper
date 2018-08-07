Make shapefile
======================


Use function :func:`mergedgrid_to_shp <ship_mapper.mergedgrid_to_shp>` to produce **shapefiles** from a ``merged.nc`` file

Example: 


.. code-block:: python

    import ship_mapper as sm
    
    info = sm.load_info('1_run') 
    
    sm.mergedgrid_to_shp(info)