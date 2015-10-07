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
      description='JSON-RPC proxy for talking Modbus over RTU and TCP.',
      long_description=__doc__,
      license='MPL',
      packages=[
          'tolk',
          'scripts',
      ],
      install_requires=[
          'docopt>=0.6.24',
          'modbus-tk>=0.4.3',
          'python-jsonrpc>=0.7.12',
      ],
      entry_points={
          'console_scripts': [
              'json_rpc_client = scripts.json_rpc_client:main',
              'modbus_tcp_slave = scripts.modbus_tcp_slave:main',
              'tolk_server = scripts.tolk_server:main',
          ]
      })
