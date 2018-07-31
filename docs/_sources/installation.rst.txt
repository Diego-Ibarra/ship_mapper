Installation
-------------

It is recommended that you make an `environment <https://conda.io/docs/user-guide/tasks/manage-environments>`_ dedicated to run `ship_mapper`.


Then, `activate` your dedicated environment, and install a couple of dependencies that do not install by defaul:

In console...

::

    conda install -c conda-forge basemap basemap-data-hires


In console...

::

    conda install -c anaconda netcdf4
    

Then, install `ship_mapper`...


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
    