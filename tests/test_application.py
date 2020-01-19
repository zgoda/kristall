import json

import pytest

from kristall.application import Application
from kristall.request import Request
from kristall.response import Response


def test_create():
    app = Application()
    assert app._error_handlers == {}
    assert app._resource_cache == {}
    assert len(app.url_map._rules) == 0
    assert app.json_encoder == json.JSONEncoder
    assert app.json_decoder == json.JSONDecoder
    assert app.request_class == Request
    assert app.response_class == Response


class TestApplication:

    @pytest.fixture
    def app(self):
        return Application()

    def test_add_simple_resource_object(self, app):

        class Resource:

            def get(self, request):
                return {'message': 'test'}

        res = Resource()
        app.add_resource('/endpoint', res)
        assert len(app.url_map._rules) == 1

    def test_add_object_with_endpoint(self, app):

        class Resource:

            endpoint = 'test-endpoint'

            def get(self, request):
                return {'message': 'test'}

        res = Resource()
        app.add_resource('/endpoint', res)
        assert len(app.url_map._rules) == 1
        assert res.endpoint in app._resource_cache
        rule = app.url_map._rules[0]
        assert rule.methods == {'GET', 'HEAD'}

    def test_add_error_handler(self, app):
        def handler(code, *args, **kwargs):
            return Response(json.dumps({'message': 'fail'}), status=code)
        app.add_error_handler(500, handler)
        assert len(app._error_handlers) == 1

    def test_default_error_handler_with_message(self, app):
        rv = app.default_error_handler(500, description='fail')
        assert rv.status_code == 500
        assert json.loads(rv.get_data().decode('utf-8')) == {'message': 'fail'}

    def test_default_error_handler_no_message(self, app):
        rv = app.default_error_handler(500)
        assert rv.status_code == 500
        assert len(rv.get_data()) == 0
