Kristall
========

Lightweight web framework for building APIs and backends.

Why
---

Because Falcon sucks. And since Flask sucks less, I decided to build a WSGI
framework that's based on Werkzeug and is simpler than Flask. Sure, there are
Flask extensions like Flask-RESTFul and Flask-RESTPlus but they are built on
top of Flask and do many extra things that are better done by others, or not
done at all.

But since not everything sucks in Falcon I'd grab some ideas, like resourceful
routing without need to subclass specific ``Resource`` base class, or only
static route registration.

What
----

* resourceful routing
* static route registration
* only JSON content type supported

That's it for now.
