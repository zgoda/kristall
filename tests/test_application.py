import json

import pytest
from werkzeug.exceptions import SecurityError
from werkzeug.test import Client

from kristall.application import Application
from kristall.request import Request
from kristall.response import Response


def test_create():
    app = Application()
    assert app._resource_cache == {}
    assert len(app.url_map._rules) == 0
    assert app.json_encoder == json.JSONEncoder
    assert app.json_decoder == json.JSONDecoder
    assert app.request_class == Request
    assert app.response_class == Response


class TestApplication:

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.app = Application()

    def test_add_simple_resource_object(self):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        res = Resource()
        self.app.add_resource('/endpoint', res)
        assert len(self.app.url_map._rules) == 1

    def test_add_object_with_endpoint(self):

        class Resource:

            endpoint = 'test-endpoint'

            def get(self, request):
                return {'message': 'test'}

        res = Resource()
        self.app.add_resource('/endpoint', res)
        assert len(self.app.url_map._rules) == 1
        assert res.endpoint in self.app._resource_cache
        rule = self.app.url_map._rules[0]
        assert rule.methods == {'GET', 'HEAD'}

    def test_wsgi_app(self):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app.wsgi_app, Response)
        rv = client.get('/endpoint')
        assert rv.status_code == 200

    def test_call(self):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.get('/endpoint')
        assert rv.status_code == 200


class TestDispatch:

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.app = Application()

    def test_not_found(self):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.get('/somewhere')
        assert rv.status_code == 404

    def test_method_not_allowed(self):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.post('/endpoint', data={})
        assert rv.status_code == 405

    def test_error_without_code(self):

        class Resource:

            def get(self, request):
                raise SecurityError()

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.get('/endpoint')
        assert rv.status_code == 400

    def test_resource_return_response(self):

        class Resource:

            def get(self, request):
                return Response(json.dumps({'message': 'test'}))

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.get('/endpoint')
        assert rv.status_code == 200

    def test_resource_return_str(self):

        class Resource:

            def get(self, request):
                return json.dumps({'message': 'test'})

        self.app.add_resource('/endpoint', Resource())
        client = Client(self.app, Response)
        rv = client.get('/endpoint')
        assert rv.status_code == 200
