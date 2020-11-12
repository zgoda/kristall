import pytest
from werkzeug.test import Client

from kristall.application import Application
from kristall.response import Response


@pytest.fixture()
def app(mocker):
    app = Application()
    app.add_resource(
        '/', mocker.MagicMock(get=mocker.Mock(return_value={'message': 'test'}))
    )
    return app


def test_add_before_request(app: Application, mocker):
    func = mocker.Mock()
    app.add_before_request(func)
    assert app._before_request[0] is func


def test_add_after_request(app: Application, mocker):
    func = mocker.Mock()
    app.add_after_request(func)
    assert app._after_request[0] is func


@pytest.mark.parametrize('when', ['before', 'after'])
def test_call_ok(when, app: Application, mocker):
    func = mocker.Mock(return_value=None)
    meth_name = f'add_{when}_request'
    fn = getattr(app, meth_name)
    fn(func)
    c = Client(app, Response)
    resp = c.get('/')
    assert resp.status_code == 200
    func.assert_called_once()


@pytest.mark.parametrize('when', ['before', 'after'])
def test_hooks_rv(when, app: Application, mocker):
    code = 410
    func = mocker.Mock(return_value=Response('test', status=code))
    meth_name = f'add_{when}_request'
    fn = getattr(app, meth_name)
    fn(func)
    c = Client(app, Response)
    resp = c.get('/')
    assert resp.status_code == code
    func.assert_called_once()
