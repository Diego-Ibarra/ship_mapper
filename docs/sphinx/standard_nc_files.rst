Standard NC files
===================


`ship_mapper` works with data inside netCDF files (.nc) with a spedific structure.

Therefore, a first step is to convert the original "ship data" from 
the orginal source files into .nc files with the standard format. This is done with 
:func:`~converters.bulk_convert_to_nc` as shown in the example below.


Example:

.. code-block:: python

    import ship_mapper as sm
    
    sm.bulk_convert_to_nc(info.converter,
                          path_to_data_in=info.dirs.data_original,
                          overwrite=False)