"""
Good place to read about packaging:
https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages

#setup(name='ship_mapper',
#      version='0.1',
#      packages=find_packages(),
#      description = 'Tool to create "ship density" heat maps from AIS, VMS and other ship-position services',
#      author = 'Diego Ibarra',
#      author_email = 'Diego.Ibarra@dal.ca',
#      url = 'https://github.com/Diego-Ibarra/ship_mapper',
#      download_url = 'https://github.com/Diego-Ibarra/ship_mapper/archive/0.1.tar.gz',
#      keywords = ['ship', 'vessels', 'mapping'],
#      install_requires=['xarray',
#                        'pandas'
#                        'numpy',
#                        'pytest',
#                        'basemap',
#                        'xlrd',
#                        'cmocean',
#                        'basemap-data-hires',
#                        'matplotlib']
#      )

setup(name='ship_mapper',
      version='0.1',
      packages=find_packages(),
      install_requires=['xarray>=0.10.0',
                        'matplotlib>=2.1.2']
      )

