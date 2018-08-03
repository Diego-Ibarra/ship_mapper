Make maps
======================


Use function :func:`~mapper.map_density` to produce a map from a ``merged.nc`` file

Example: 


.. code-block:: python

    import ship_mapper as sm
    
    info = sm.load_info('1_run') 
    
    m = sm.map_density(info, cmap='inferno_r',sidebar=True)