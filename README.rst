.. image:: https://readthedocs.org/projects/ship-mapper/badge/?version=latest
    :target: http://ship-mapper.readthedocs.io/en/latest/?badge=latest
.. image:: https://travis-ci.org/Diego-Ibarra/ship_mapper.svg?branch=master
    :target: https://travis-ci.org/Diego-Ibarra/ship_mapper

ship-mapper
-----------
Tool to create "ship density" heat maps from AIS, VMS and other ship-position services.

WARNING: This project is in VERY early development stages. Don't use just yet.


WARNING!!! BUG related to Basemap
-------------
The plotting module currently used by ship_mapper (i.e. Basemap) fails to setup PROJ_LIB properly, yielding the following error:

>>> KeyError: 'PROJ_LIB'

The temporary fix this problem is to do the following at the begining of each working session (remeber to add the CORRECT path to EPSG in your own computer):

>>>import os
os.environ['PROJ_LIB'] = r'C:\Users\Diego\Anaconda3\Library\share'

Read more about this bug here: https://github.com/matplotlib/basemap/issues/419


Documentation
-------------
https://diego-ibarra.github.io/ship_mapper/index.html
