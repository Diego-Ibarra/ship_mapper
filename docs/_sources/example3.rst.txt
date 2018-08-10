3. St_Anns_Banks_AIS
====================

.. _1_run.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/projects/example3_St_Anns_Banks_AIS/1_run.py
.. _make_basemap.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/grids/St_Anns_Bank/make_basemap.py
.. _make_info.py: https://github.com/Diego-Ibarra/ship_mapper/blob/master/examples/projects/example3_St_Anns_Banks_AIS/make_info.py


Executing 1_run.py_ (shown below) will produce the following map.

.. image:: ./_images/example3_St_Anns_Banks_AIS.png
   :target: _images/example3_St_Anns_banks_AIS.png
   :align: center

Note that before you execute 1_run.py_, you need to ensure that the 
``.basemap`` and ``.grid`` files were made before and are available (they 
should be in the ``/grids/St_Anns_banks`` directory). If not,
you have to make them using make_basemap.py_

Below are the contents of 1_run.py_

.. literalinclude:: ../../examples/projects/example3_St_Anns_Banks_AIS/1_run.py