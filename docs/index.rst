Kristall
========

Kristall is minimalist Python WSGI framework for writing APIs and backends. It uses `Werkzeug <https://palletsprojects.com/p/werkzeug/>`_ as WSGI toolbox and itself is only very thin wrapper over what Werkzeug provides.

The idea of Werkzeug-based web framework first came to me when I was preparing a `talk for 2009 edition of Pycon.PL conference <https://github.com/zgoda/pyconpl09>`_. At the very beginning it was general purpose framework similar in feature set to `Django <https://www.djangoproject.com/>`_ but resembling more what later become `Flask <https://palletsprojects.com/p/flask/>`_ after brief period of being April Fool's joke. The talk was intended to show how various parts of web framework like Django relate to WSGI and how they can be built with just a basic WSGI toolbox like Werkzeug or `WebOb <https://pypi.org/project/WebOb/>`_ (Werkzeug is still my personal preference).

Then years passed and I got back to the idea when I discovered how limited is my choice when I had to build really simple API that was expected to be maintained by people that usually work with languages other than Python. This should be as simple as `Express.JS <https://expressjs.com/>`_ but no simpler. This should provide features that Falcon provides but with much friendlier library interface, while still being less confusing than these Flask add-ons.

Documentation
-------------

.. toctree::
    :maxdepth: 2

    quickstart


API documentation
-----------------

.. toctree::
    :maxdepth: 2

    modules


Miscellanea
-----------

.. toctree::
    :maxdepth: 2

    why


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
