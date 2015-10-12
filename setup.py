#!/usr/bin/env python
"""
Tolk
====

Tolk is JSON-RPC proxy for doing Modbus communication over RTU and TCP.
"""
from setuptools import setup

setup(name='Tolk',
      version='0.1.3',
      author='Auke Willem Oosterhoff',
      author_email='oosterhoff@baopt.nl',
      description='JSON-RPC proxy for talking Modbus over RTU and TCP.',
      url='https://github.com/AdvancedClimateSystems/Tolk/',
      long_description=__doc__,
      license='MPL',
      packages=[
          'tolk',
          'scripts',
      ],
      install_requires=[
          'docopt>=0.6.2',
          'logbook>=0.11.2',
          'modbus-tk>=0.4.3',
          'python-jsonrpc>=0.7.12',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Embedded Systems',
      ],
      entry_points={
          'console_scripts': [
            'json_rpc_client = scripts.json_rpc_client:main',
            'modbus_tcp_slave = scripts.modbus_tcp_slave:main',
            'tolk_server = scripts.tolk_server:main',
        ]
      })
