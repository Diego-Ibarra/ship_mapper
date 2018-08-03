Workflow
========

Generally speaking, all the instructions on how to proccess raw data into a value-added product 
are written in a ``run file`` within a project directory (e.g. `/projects/Halifax_AIS`).
However, note that each ``run file`` needs to point to a set of ``basemap/grid`` files, 
which are done previously and stored elsewhere (e.g. `/grids/Maritimes/ancillary`).

Even though not all steps are required in every project, the ``run file`` may 
include the following instructions:

* :doc:`Convert original data into "Standard NC files" <standard_nc_files>`: :func:`~converters.bulk_convert_to_nc`
* Filter data
    * :doc:`Filter data to include only a narrow domain  <standard_nc_files>`: :func:`~utils.spatial_filter`
    * :doc:`Filter data to include  specific dates  <standard_nc_files>` 
* :doc:`Project "pings" onto grid  <standard_nc_files>`: :func:`~gridder.gridder`
* :doc:`Merge multiple grids <standard_nc_files>`: :func:`~gridder.grid_merger`
* :doc:`Make a map <standard_nc_files>`: :func:`~mapper.map_density`
* :doc:`Save grid as shapefile <standard_nc_files>`: :func:`~mapper.mergedgrid_to_shp`


.. image:: ./_images/flow_diagram.png
   :target: _images/flow_diagram.png