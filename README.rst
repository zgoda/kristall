Kristall
========

.. image:: https://travis-ci.com/zgoda/kristall.svg?branch=master
    :target: https://travis-ci.com/zgoda/kristall
    :alt: Travis CI

.. image:: https://codecov.io/gh/zgoda/kristall/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/zgoda/kristall
    :alt: CodeCov

.. image:: https://www.codefactor.io/repository/github/zgoda/kristall/badge
    :target: https://www.codefactor.io/repository/github/zgoda/kristall
    :alt: CodeFactor

Lightweight *web framework*
(`wink, wink <https://www.youtube.com/watch?v=dlDXVI6uM78>`_)
for building APIs and backends.
Reasonably fast in execution, developer friendly. If you need gazillions of
requests served by single process in a second then there are better options
than Kristall. I'm happy when it's not slower than Flask.

Why
---

Some frameworks suck here, others suck there and none is good at all things
I want. I decided to build a WSGI application tool that's based on
`Werkzeug <https://palletsprojects.com/p/werkzeug/>`_ and is simpler than
Flask. Sure, there are
`Flask <https://palletsprojects.com/p/flask/>`_ extensions that make writing
REST APIs simpler like
`Flask-RESTFul <https://flask-restful.readthedocs.io/en/latest/>`_ and
`Flask-RESTPlus <https://flask-restplus.readthedocs.io/en/stable/>`_ but they
are built on top of Flask and do many extra things that are better done by
others, or not done at all. I wanted something that is somewhere in between
Falcon and Flask. Simplicity of Falcon with convenience of Flask.

But since not everything sucks in Falcon I'd grab some ideas, like
resourceful routing without need to subclass specific ``Resource`` base class,
or only static route registration.

What
----

* resourceful routing
* static route registration
* only JSON content type supported
* very limited automatic coercion to JSON

That's it for now.

Future developments:

* JWT-based resource access control (optional)
* CORS support (optional)

What not
--------

* no decorator-based route registration - there's only one way to register
  routes and it is explicit
* no built-in support for any other content type than ``application/json`` on
  both input and output
* no fancy JSON de/encoding, only builtin ``json`` module is used in default JSON
  handling - use schema parsing/validating library eg.
  `Marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_ or
  `Colander <https://docs.pylonsproject.org/projects/colander/en/stable/>`_ if
  you need anything beyond that; default behaviour may be customised to some
  degree by providing JSON decoder and encoder classes

How
---

Really very thin wrapper over Werkzeug utility functions and classes.
Seriously, I'm not calling this *a framework*. Not yet. It consists of
``Application`` class that's and entry point to runtime and
``Request``/``Response`` objects that in fact are Werkzeug's built in
wrappers reconfigured to support only JSON as transport media with some
convenience methods.

Runtime dependencies
--------------------

* Python 3.7
* Werkzeug 0.16

These are minimal versions of requirements.
