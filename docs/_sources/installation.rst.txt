Installation
-------------

It is recommended to run `ship_mapper` in an `Anaconda <https://www.anaconda.com/download/>`_ 
environment.

You will need to install a couple
of dependencies that do not install by default when installing Anaconda:


Install ``basemap`` and ``basemap-data-hires`` mapping libraries.

In console...

::

    conda install -c conda-forge basemap basemap-data-hires

Install ``netcdf4`` to be able to work with `.nc` files

In console...

::

    conda install -c anaconda netcdf4
    

Install ``git``...

::

    conda install git



Then, install ``ship_mapper``...


Method 1
++++++++

Use pip to install directly from github


::

    pip install git+https://github.com/Diego-Ibarra/ship_mapper
    

Method 2
++++++++

Download repository, then execute the following in terminal (or anaconda promt):

::

    python setup.py install


or if you want to be able to manipulate the modules code without having to re-install between changes...

::

    python setup.py develop
    


.. warning::
    
    If you are using SPYDER IDE, you should dissable inline plotting: Go to Tools > Preferences > IPython console > Graphics ...and change the Backend to "automatic"



Updating ship_mapper
++++++++++++++++++++

If you want to update to the newest version, first...

::

    pip uninstall ship_mapper
    

then...

::

    pip install git+https://github.com/Diego-Ibarra/ship_mapper
    