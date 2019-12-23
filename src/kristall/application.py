import inspect
import json
from typing import Any, Callable

from werkzeug.routing import Map, Rule

from .request import Request
from .response import Response


class Application:

    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    def __init__(self):
        self.url_map = Map()
        self._resource_cache = {}

    def add_resource(self, path: str, resource: Any):
        res_obj = dict(inspect.getmembers(resource))
        for method in self.METHODS:
            handler_name = method.lower()
            if handler_name in res_obj:
                klass = res_obj[handler_name].__self__.__class__
                mod_name = klass.__module__
                class_name = klass.__name__
                endpoint = f'{mod_name}.{class_name}:{handler_name}'
                self.url_map.add(Rule(path, endpoint=endpoint, methods=[method]))
                self._resource_cache[endpoint] = res_obj[handler_name]

    def dispatch(self, request: Request) -> Response:
        adapter = self.url_map.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        handler = self._resource_cache[endpoint]
        result = handler(request, **values)
        if isinstance(result, Response):
            return result
        if isinstance(result, str):
            return Response(result, mimetype='application/json')
        return Response(json.dumps(result), mimetype='application/json')

    def wsgi_app(self, environ: dict, start_response: Callable):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)

    def __call__(self, environ: dict, start_response: Callable):
        return self.wsgi_app(environ, start_response)
