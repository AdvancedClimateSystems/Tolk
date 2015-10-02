#!/usr/bin/env python
"""
Tolk
====

Tolk is JSON-RPC proxy for doing serial communication in the form of Modbus
over RTU.

.. code:: bash

    $ ./tolk

"""
from setuptools import setup

setup(name='Tolk',
      version='0.1.0',
      author='Auke Willem Oosterhoff',
      author_email='oosterhoff@baopt.nl',
      description='JSON-RPC proxy for talking Modbus over RTU.',
      long_description=__doc__,
      license='MPL',
      packages=[
          'tolk',
      ],
      install_requires=[
          'modbus-tk>=0.4.3',
          'python-jsonrpc>=0.7.12',
      ],
      entry_points={
          'console_scripts': [
              'tolk = tolk.cli:main',
          ],
      })
