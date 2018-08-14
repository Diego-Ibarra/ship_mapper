settings.py 
=============

You will need to crete file called ``settings.py`` and place it in your
``projects`` directory. The contents of this file should be as bellow, however
reflecting your own computer's paths, user and password


.. code-block:: python
    
    '''
    This file should be modified to reflect your computers paths, user and password
    '''
    
    from pathlib import Path
    
    GRIDS = Path(r'C:\Users\IbarraD\ship_mapper\examples\grids')
    
    DATA = Path(r'C:\Users\IbarraD\ship_mapper\examples\data')
    
    ORACLE_USER = 'test_user' 
    
    ORACLE_PASSWORD = 'test_password'