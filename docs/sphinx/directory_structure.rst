Directory structure
===================


We suggest to split ``data``, ``grids`` and ``projects`` into 3 different directories. 
Note that the actual code of `ship_mapper` gets automatically installed elsewhere with
the other python modules.

Directory tree example

.. code-block:: python

    |--data
    |  |--AIS_CCG
    |  |--VMS_DFO
    |
    |--grids
    |  |--Maritimes
    |  |--St.Anns_Bank
    |
    |--projects
    |  |--Maritimes_AIS
    |  |--Halifax_AIS
    |  |--St_Anns_Bank_AIS
    |  |--Maritimes_VMS
    |  |--settings.py
    |
    |
    |
    |
    |
    |
    |
    |
    |--anaconda3
    |  |--envs
    |     |--myenv
    |        |--Lib
    |           |--site-packages
    |              |--ship_mapper

