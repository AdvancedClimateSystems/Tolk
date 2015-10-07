Installation
============

As package
----------

If you want to use Tolk as a package you can install Tolk from Pypi::

    $ pip install tolk

or using `setup.py`::

    # Assumed you've got Tolk's source.
    $ pip setup.py install

For development, debugging and testing
---------------------------------------

If you want to build the documentation or run the test suite you need the
source which is on GitHub_. Download it and install Tolk's requirement using
pip::

    $ pip install -r dev_requirements.txt

Now you can build the docs::

    $ sphinx-build -b html docs/source docs/build

Or run the tests::

    $ py.test tests

.. External references:
.. _GitHub: https://github.com/AdvancedClimateSystems/Tolk
