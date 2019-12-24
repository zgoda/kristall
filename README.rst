Kristall
========

Lightweight *web framework* (wink, wink) for building APIs and backends.
Reasonably fast in execution, developer friendly. If you need gazillions of
requests served by single process in a second then there are better options
than Kristall. I'm happy when it's not slower than Flask.

Why
---

Because framework F1 sucks. And since framework F2 sucks less, I decided to
build a WSGI application tool that's based on
`Werkzeug <https://palletsprojects.com/p/werkzeug/>`_ and is simpler than
framework F2. Sure, there are `Flask <https://palletsprojects.com/p/flask/>`_
extensions that make writing REST APIs simpler like
`Flask-RESTFul <https://flask-restful.readthedocs.io/en/latest/>`_ and
`Flask-RESTPlus <https://flask-restplus.readthedocs.io/en/stable/>`_ but they
are built on top of Flask and do many extra things that are better done by
others, or not done at all.

But since not everything sucks in framework F1 I'd grab some ideas, like
resourceful routing without need to subclass specific ``Resource`` base class,
or only static route registration.

What
----

* resourceful routing
* static route registration
* only JSON content type supported
* very limited automatic coercion to JSON

That's it for now.

What not
--------

* no decorator-based route registration - there's only one way to register
  routes
* no support for any other content type than ``application/json`` on both
  input and output
* no fancy JSON de/encoding, only builtin :mod:`json` is used in default JSON
  handling - use schema parsing/validating library eg.
  `Marshmallow <https://marshmallow.readthedocs.io/en/stable/>`_ or
  `Colander <https://docs.pylonsproject.org/projects/colander/en/stable/>`_

How
---

Really very thin wrapper over Werkzeug utility functions and classes.
Seriously, I'm not calling this *a framework*. Not yet. It consists of
``Application`` class that's and entry point to runtime and
``Request``/``Response`` objects that in fact are Werkzeug's built in
wrappers reconfigured to support only JSON as transport media.

Runtime dependencies
--------------------

* Python 3.7
* Werkzeug 0.16
* Click 7.0

These are minimal versions of requirements.
