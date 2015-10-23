========================================================================
Python API and command line tool for the Veralite™ Smart Home Controller
========================================================================

.. image:: https://img.shields.io/pypi/v/python-veralite.svg
   :target: https://pypi.python.org/pypi/python-veralite
   :alt: PyPI Version

.. image:: https://travis-ci.org/zgreatone/python-veralite.svg?branch=master
   :target: https://travis-ci.org/zgreatone/python-veralite
   :alt: Build Status

.. image:: https://img.shields.io/pypi/dm/python-veralite.svg
   :target: https://pypi.python.org/pypi/python-veralite
   :alt: PyPI Monthly downloads

.. image:: https://img.shields.io/codecov/c/github/zgreatone/python-veralite/master.svg
   :target: http://codecov.io/github/zgreatone/python-veralite?branch=master
   :alt: Coverage report

Installation
============

.. code-block:: bash

    [sudo] pip install python-veralite


Usage
=====

Module
------

You can import the module as `veralite`.

.. code-block:: python

    import veralite

    ip = '192.168.1.89'
    user = 'admin'
    password = 'password'

    vera_api = veralate.Veralite(ip, user, password)

    vera_api.update_devices()


Command line
------------

.. code-block:: bash

    usage: veralite [-h] [--conf FILE] --ip IP -u USER -p PASSWORD
                       {light,motion,switch} ...

    Command line interface to Veralite™ Smart Home Controller

    positional arguments:
      {light,motion,switch}
                        command help
        light               light commands
        motion              motion sensor commands
        switch              switch commands

    optional arguments:
      -h, --help            show this help message and exit
      --conf FILE           config file (default ~/.config/veralite/config)
      --ip IP               the ip for veralite system
      -u USER, --user USER  username for veralite
      -p PASSWORD, --password PASSWORD
                        password for veralite


    examples:
        veralite --ip 192.168.1.22 -u veraadmin -p adminpassword switch modify --id 22 --on
        veralite --ip 192.168.1.22 -u veraadmin -p adminpassword light list
        veralite --ip 192.168.1.22 -u veraadmin -p adminpassword motion modify --id 10 --arm


A configuration file can also be specified to prevent ip/user/password repitition.


.. code-block:: ini

    [DEFAULT]
    ip = 192.168.1.55
    user = theuser
    password = mypassword
