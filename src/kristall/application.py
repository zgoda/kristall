import inspect
import json
from typing import Callable, Iterator, Optional

from werkzeug.exceptions import HTTPException, MethodNotAllowed
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response as WerkzeugResponse
from werkzeug.wsgi import ClosingIterator

from .request import Request
from .response import Response
from .utils import local, local_manager


class Application:

    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    json_encoder = json.JSONEncoder
    json_decoder = json.JSONDecoder
    request_class = Request
    response_class = Response

    def __init__(self):
        self.url_map = Map()
        self._resource_cache = {}
        self._error_handlers = {}

    def add_resource(self, path: str, resource: object):
        res_obj = dict(inspect.getmembers(resource))
        resource_methods = []
        resource_class = None
        for method in self.METHODS:
            handler_name = method.lower()
            if handler_name in res_obj:
                resource_methods.append(method)
                resource_class = res_obj[handler_name].__self__.__class__
        mod_name = resource_class.__module__
        class_name = resource_class.__name__
        endpoint = getattr(resource, 'endpoint', None) or f'{mod_name}.{class_name}'
        self.url_map.add(Rule(path, endpoint=endpoint, methods=resource_methods))
        self._resource_cache[endpoint] = res_obj

    def add_error_handler(self, code: int, handler: Callable, *args, **kwargs):
        self._error_handlers[code] = (handler, args, kwargs)

    def default_error_handler(
                self, code: int, description: Optional[str] = None, *args, **kwargs
            ) -> Response:
        if description:
            msg = json.dumps({'message': description})
        else:
            msg = ''
        return self.response_class(msg, status=code)

    def dispatch(self, request: Request) -> Response:
        local.url_adapter = adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            resource = self._resource_cache[endpoint]
            handler = resource.get(request.method.lower())
            if handler is None:
                raise MethodNotAllowed()
            result = handler(request, **values)
            if isinstance(result, WerkzeugResponse):
                return result
            if isinstance(result, str):
                return self.response_class(result)
            return self.response_class(json.dumps(result, cls=self.json_encoder))
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

    def wsgi_app(self, environ: dict, start_response: Callable) -> Callable:
        request = self.request_class(environ, self.json_decoder)
        response = self.dispatch(request)
        return ClosingIterator(
            response(environ, start_response), [local_manager.cleanup]
        )

    def __call__(self, environ: dict, start_response: Callable) -> Iterator:
        return self.wsgi_app(environ, start_response)
