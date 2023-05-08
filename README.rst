e(BE:L) RESTful API Client |build| |coverage|
==================================================

**e(BE:L) RESTful API Client** is a client for the easy usage of API methods provided be an e(BE:L) knowledge server.
e(BE:L) is currently in the alpha-testing phase and will be released soon!


Installation |python_versions| |pypi| |pypi_license|
------------------------------------------------------

.. code-block:: sh

    $ pip install ebel_rest


Quick Start
------------

Connect to the database using the credentials.

.. code-block:: python

    from ebel_rest import connect, query

    # Database settings
    server = "https://graphstore.scai.fraunhofer.de"
    db_name = "covid"
    user = "guest"
    password = "guest"
    print_url = True

    # Connect to database
    connect(user, password, server, db_name, print_url)

Start making queries

.. code-block:: python

    pubs = statistics.publication_by_year()
    pubs.data

Usage
--------
This API interface package is designed to simplify communicating with an e(BE:L) generated knowledge graph. Examples
of how to use this package and its methods can be found in
`Examples notebook <https://github.com/e-bel/ebel_rest/blob/master/notebooks/Examples.ipynb>`_.


Disclaimer
----------

The COVID-19 Knowledge Graph is a resource developed in an academic capacity funded by the
`PHAGO project <https://www.phago.eu/home/>`_ and thus comes with no warranty or guarantee of maintenance or support.


.. |pypi| image:: https://img.shields.io/pypi/v/ebel_rest.svg
        :target: https://pypi.python.org/pypi/ebel_rest

.. |travis| image:: https://img.shields.io/travis/e-bel/ebel_rest.svg
        :target: https://travis-ci.org/cebel/ebel_rest

.. |docs| image:: https://readthedocs.org/projects/ebel-rest/badge/?version=latest
        :target: https://ebel-rest.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. |pypi_license| image:: https://img.shields.io/pypi/l/ebel_rest.svg
    :target: https://pypi.python.org/pypi/ebel_rest
    :alt: MIT License

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/ebel_rest.svg
    :alt: Stable Supported Python Versions

.. |coverage| image:: https://codecov.io/gh/e-bel/ebel_rest/coverage.svg?branch=master
    :target: https://codecov.io/gh/e-bel/ebel_rest?branch=master
    :alt: Coverage Status

.. |build| image:: https://travis-ci.com/e-bel/ebel_rest.svg?branch=master
    :target: https://travis-ci.com/e-bel/ebel_rest
    :alt: Build Status