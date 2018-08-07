Standard NC files
===================


`ship_mapper` works with data inside netCDF files (.nc) with a spedific structure.

Therefore, a first step is to convert the original "ship data" from 
the orginal source files into .nc files with the standard format. This is done with 
:func:`bulk_convert_to_nc <ship_mapper.bulk_convert_to_nc>` as shown in the example below.


Example:

.. code-block:: python

    import ship_mapper as sm
    
    sm.bulk_convert_to_nc(info.converter,
                          path_to_data_in=info.dirs.data_original,
                          overwrite=False)
                          
Note that the conversion from source to `Standard NC` is done by a `converter file`.

The following converter files are included:

.. toctree::
   :maxdepth: 3
   
   ./AIS_CCG
   ./VMS_DFO
   ./VMS_DFO_Oracle