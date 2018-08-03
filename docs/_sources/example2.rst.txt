2. Halifax_AIS
=================

.. _1_run.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/projects/example2_Halifax_AIS/1_run.py
.. _make_basemap.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/projects/example2_Halifax_AIS/make_basemap.py
.. _make_info.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/projects/example2_Halifax_AIS/make_info.py


Executing 1_run.py_ (shown below) will produce the following map.

.. image:: ./_images/example2_Halifax_AIS.png
   :target: _images/example2_Halifax_AIS.png
   :align: center

Note that before you execute 1_run.py_, you need to ensure that the 
``.basemap`` and ``.grid`` files were made before and are available (they 
should be in the ``projects/example2_Halifax_AIS`` directory). If not,
you have to make them using make_basemap.py_. Note that the ``Halifax_Area`` grid
is a "one-off" grid and this it is not in the ``/grids`` directory (instead it is in the project directory).

Also you need to ensure that the ``info`` file (i.e. `info_1_run.p`) was priorly made
and is available. If not, you have to make it with make_info.py_

Below are the contents of 1_run.py_

.. literalinclude:: ../../examples/projects/example2_Halifax_AIS/1_run.py