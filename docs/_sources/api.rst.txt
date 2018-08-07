API (List of modules and functions)
===================================

Code is divided into the following modules:

.. currentmodule:: ship_mapper



Gridder
-------

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   calculate_gridcell_areas
   grid_merger
   gridder
   mergedgrid_to_shp

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   gridder.getWKT_PRJ
   gridder.gridder_pingsPerCell

   
   
Mapper
-------

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   make_basemap
   map_density
   map_dots
   map_dots_one_ship
   save_basemap
   
.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   mapper.load_my_cmap
   mapper.define_path_to_map
   mapper.make_legend_text
   
   
   
Info_Object
-----------

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   attrs_to_info
   data_to_info
   info
   info_to_attrs
   load_info

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   info_object.auto_update



   
Converters
----------

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   bulk_convert_to_nc
   bulk_update_attributes
   convert_to_nc

Included converter files:
   
* :doc:`AIS_CCG  <AIS_CCG>`
* :doc:`VMS_DFO  <VMS_DFO>`
* :doc:`VMS_DFO_Oracle  <VMS_DFO_Oracle>`


Utils
-------

.. autosummary::
   :toctree: ./generated/
   :nosignatures:

   align_with_grid
   checkDir
   degrees_to_meters
   distance
   elapsed_days
   estimate_velocity
   get_all_files
   get_filename_from_fullpath
   get_path_from_fullpath
   interp2d
   make_mydirs
   spatial_filter
   stop
   write_info2data

