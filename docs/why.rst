Some questions and some answers
===============================

Why WSGI?
---------

While it may seem outdated in 2020, WSGI is still valid option for Python web programming. For many people it's even the only viable option, considering how easily ASGI eats megabytes of RAM, and how unstable ASGI servers are, despite almost 5 years of development. In comparison WSGI:

* is rock solid
* has a bunch of mature servers to run your application
* is easily scalable with standard tools
* has many stable deployment options

And all that is being blogged on to death for years now so all options are covered, whether you prefer gunicorn over uwsgi, or lighttpd over nginx (idk why would anyone do that but hey), or you are just adventurous and want to run bare Python application with CherryPy. WSGI still covers all your bases, despite being 17 years old.

For most people processing hundreds of thousands of connections per second is not the most important problem - but how to efficiently use that 2 cores of VPS is. Even *moderately fast* framework is *fast enough* if there are 2-3 simultaneous connections served by application. And for most people trying to start with most efficient framework to be able to handle high traffic that would eventually come in next 3, 4 or 5 years makes them spend too much time on things that would never happen.

So use WSGI framework and be happy today. Tomorrow may never come.

Why another framework?
----------------------

Since we settled on WSGI let's look what framework options do we have for REST API development? There is `Django REST Framework <https://www.django-rest-framework.org/>`_, some Flask add-ons and `Falcon <https://falconframework.org/>`_. Of these only Falcon is purpose built to be fast as API server - it does not provide anything besides basic HTTP features and is really fast. In most of benchmarks it easily outperforms all other contenders, including some async based. On the other hand, Flask add-ons provide familiar interface at the cost of larger footprint. The performance is acceptable and to be fair, when facing performance issues your 1st companion should be profiler, not new framework. But anyway Flask add-ons give you familiar interface at the cost of many megabytes wasted for things that you don't use in Web API application. And most probably it will be abandoned in a year, forked in next year and the usual dance of not-so-compatible forks will follow.

Of course there are still plenty of others but let's be honest, the boom time for Python WSGI frameworks was ~10 years ago and since then most of these frameworks became abandonware. Their user base was too small to catch up when original creator lost interest in development and in most cases the code lays untouched for years on Github. There's something excessively tragic about abandoned code and I am sure someone will write a great theatrical drama about this. Or even make a block-busting movie but for now let's focus on 2020 state of WSGI frameworks for writing REST APIs.

All Flask add-ons (`Flask-RESTFul <https://github.com/flask-restful/flask-restful>`_, `Flask-RESTPlus <https://github.com/noirbizarre/flask-restplus>`_, `Flask-RESTX <https://github.com/python-restx/flask-restx>`_, check news who's last in this chain) have all this Flask cruft that helps so much when building Web applications but is not very usable when building APIs, then add their own cruft like bare bones request values parsing and validation which falls behind other libraries in terms of both features and performance. Seriously, people, use `Colander <https://pypi.org/project/colander/>`_ or `Marshmallow <https://pypi.org/project/marshmallow/>`_. But they both have one thing that's invaluable - it's familiarity of framework API. It's still Flask, and you write code like in any Flask based application.

So why not Falcon? The developers decided on some features that are far from being common, friendly or even convenient. Not a big deal, but for many developers the idea of modifying passed response object in request handler may seem to be awkward. I guess this is the price you pay for that performance. Falcon is very good piece of software but it does not mean that it would fit everybody.

That's why Kristall is being developed. I want as much Flask in Falcon as I could get so there is a Werkzeug based framework with much smaller feature set than Flask but on par with Falcon.

Why so minimalistic?
--------------------

Others will give you more out of the box but Kristall does not pose any limits for extending. In fact, I wrote it with extendability in mind. All provided classes are supposed to be used as bases for customizations - both :class:`~kristall.request.Request` and :class:`~kristall.response.Response` are just thin wrappers over Werkzeug's structures, and :class:`~kristall.application.Application` is simple glue over WSGI application idea.

In this sense this is not a framework, where you'd expect to have many ready to use classes. It's still more of a toolbox that provides developer with building blocks to make his new application.
