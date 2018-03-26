"""
Good place to read about packaging:
https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages

setup(name='ship_mapper',
      version='0.1',
      packages=find_packages(),
      install_requires=['xarray',
                        'numpy']
      )
