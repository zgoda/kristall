import json
from typing import Callable, Iterator

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response as WerkzeugResponse

from .request import Request
from .response import Response
from .utils import endpoint as gen_endpoint


class Application:
    """Wrapper over WSGI application. This class provides simple route
    registration mechanism that allows to match code execution to request
    paths. It's the central point of an app but does not provide much more
    than that.

    Possible customizations include custom JSON encoder and decoder classes
    and possibility to specify custom request and response classes.

    :cvar json_encoder: JSON encoder class, defaults to
                        :class:`~json.JSONEncoder`
    :cvar json_decoder: JSON decoder class, defaults to
                        :class:`~json.JSONDecoder`
    :cvar request_class: request encapsulation class, defaults to
                         :class:`~kristall.request.Request`
    :cvar response_class: response encapsulation class, defaults to
                          :class:`~kristall.response.Response`
    """

    METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

    json_encoder = json.JSONEncoder
    json_decoder = json.JSONDecoder
    request_class = Request
    response_class = Response

    def __init__(self):
        self.url_map = Map()
        self._resource_cache = {}

    def add_resource(self, path: str, resource: object):
        """Register resource under specified path. The resource is an
        instance that is expected to provide methods that correspond to HTTP
        words. If the instance provides :attr:`endpoint` attribute the it will
        be used as endpoint name, otherwise it will be registered under the
        name that is it's class dotted path.

        :param path: HTTP path which resource serves
        :type path: str
        :param resource: resource instance
        :type resource: object
        """
        resource_methods = []
        for method in self.METHODS:
            handler_name = method.lower()
            handler = getattr(resource, handler_name, None)
            if handler:
                resource_methods.append(method)
        endpoint = getattr(resource, 'endpoint', None)
        if not endpoint:
            endpoint = gen_endpoint(resource)
        self.url_map.add(Rule(path, endpoint=endpoint, methods=resource_methods))
        self._resource_cache[endpoint] = resource

    def dispatch(self, request: Request) -> Response:
        """Dispatch and service HTTP request.

        :param request: request wrapper
        :type request: Request
        :raises MethodNotAllowed: if resource that is registered for specified
                                  path does not support HTTP method
        :return: response that is either result of request handler or an error
        :rtype: Response
        """
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            resource = self._resource_cache[endpoint]
            handler = getattr(resource, request.method.lower())
            result = handler(request, **values)
        except HTTPException as e:
            return e
        if isinstance(result, WerkzeugResponse):
            return result
        if isinstance(result, str):
            return self.response_class(result)
        return self.response_class(json.dumps(result, cls=self.json_encoder))

    def wsgi_app(self, environ: dict, start_response: Callable) -> Response:
        """Wrapper over WSGI application that exposes WSGI application for
        further wrapping with WSGI middleware.

        :param environ: WSGI environ
        :type environ: dict
        :param start_response: callable that is used to begin writing response
        :type start_response: Callable
        :return: response object
        :rtype: Response
        """
        request = self.request_class(environ, self.json_decoder)
        response = self.dispatch(request)
        return response(environ, start_response)

    def __call__(self, environ: dict, start_response: Callable) -> Iterator:
        return self.wsgi_app(environ, start_response)
