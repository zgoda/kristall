import inspect
import json
from typing import Any, Callable, Optional

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response as WerkzeugResponse

from .request import Request
from .response import Response


class Application:

    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    json_encoder = json.JSONEncoder
    json_decoder = json.JSONDecoder

    def __init__(self):
        self.url_map = Map()
        self._resource_cache = {}
        self._error_handlers = {}

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

    def add_error_handler(self, code: int, handler: Callable, *args, **kwargs):
        self._error_handlers[code] = (handler, args, kwargs)

    def default_error_handler(
                self, code: int, description: Optional[str] = None, *args, **kwargs
            ) -> Response:
        if description:
            msg = json.dumps({'message': description})
        else:
            msg = ''
        return Response(msg, status=code)

    def dispatch(self, request: Request) -> Response:
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = self._resource_cache[endpoint]
            result = handler(request, **values)
            if isinstance(result, WerkzeugResponse):
                return result
            if isinstance(result, str):
                return Response(result)
            return Response(json.dumps(result, cls=self.json_encoder))
        except HTTPException as e:
            code = e.code
            if code is not None:
                description = e.description
                handler_info = self._error_handlers.get(code)
                if handler_info is None:
                    return self.default_error_handler(code, description)
                handler, args, kwargs = handler_info
                return handler(code, description, *args, **kwargs)
            return e

    def wsgi_app(self, environ: dict, start_response: Callable):
        request = Request(environ)
        response = self.dispatch(request)
        return response(environ, start_response)

    def __call__(self, environ: dict, start_response: Callable):
        return self.wsgi_app(environ, start_response)
