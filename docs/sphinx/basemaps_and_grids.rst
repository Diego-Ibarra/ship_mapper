Basemap and grid files
======================

Every projects requires a ``.basemap`` and ``.grid`` files. The ``.basemap`` file contains
the "background" map with boundaries, bathymetry and other features. The ``.grid``
file contains metadata about the grid properties. 

We recommend to place the ``.basemap`` and ``.grid`` files in the `/grids/` directory, 
so that they can be re-used by many projects. However you can also place them within
the project directory for one-off use.

Instructions on how to make the ``.basemap`` and ``.grid`` files are made 
usually located in a ``make_basemap.py`` file, which calls the actual fuction that 
makes the basemap, :func:`make_basemap <ship_mapper.make_basemap>`


The example below shows teh contents of a very simple ``make_basemap.py`` file.

.. code-block:: python

    import ship_mapper as sm

    # Make info object
    info = sm.info(__file__)
    
    # Define items in info
    info.grid.region = 'Maritimes'
    info.grid.basemap = 'basemap_sidebar'
    info.grid.type = 'generic' # opsions: 'one-off' OR 'generic'
    info.grid.bin_size = 0.01 # Degrees
    info.grid.minlat = 39.9
    info.grid.maxlat = 48.3
    info.grid.minlon = -69
    info.grid.maxlon = -54.7
    info.grid.epsg_code = '4326'
    
    info.maps.resolution = 'i'
    info.maps.parallels = 1 # Deegres between lines
    info.maps.meridians = 1# Deegres between lines
    info.maps.scalebar_km = 150
    
    m = sm.make_basemap(info, [info.grid.minlat,
                               info.grid.maxlat,
                               info.grid.minlon,
                               info.grid.maxlon], sidebar=True)