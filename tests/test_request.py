import json

import pytest
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.test import EnvironBuilder

from kristall.request import Request


@pytest.fixture()
def custom_decoder():

    class CustomDecoder(json.JSONDecoder):
        pass

    return CustomDecoder


def test_create_default():
    builder = EnvironBuilder(path='/endpoint', method='GET')
    env = builder.get_environ()
    req = Request(env)
    assert req.decoder == json.JSONDecoder


def test_create_custom_decoder(custom_decoder):
    decoder = custom_decoder
    builder = EnvironBuilder(path='/endpoint', method='GET')
    env = builder.get_environ()
    req = Request(env, json_decoder=decoder)
    assert req.decoder == decoder


def test_get_data_entity_too_large():
    builder = EnvironBuilder(
        path='/endpoint', method='POST', data={'field': 'a' * 5 * 1024 * 1024}
    )
    env = builder.get_environ()
    req = Request(env)
    with pytest.raises(RequestEntityTooLarge):
        req.get_data()


def test_get_data_ok_form():
    fld_name = 'field'
    fld_value = 'value'
    builder = EnvironBuilder(
        path='/endpoint', method='POST', data={fld_name: fld_value}
    )
    env = builder.get_environ()
    req = Request(env)
    rv = req.get_data()
    assert isinstance(rv, str)
    assert rv == f'{fld_name}={fld_value}'


def test_get_data_ok_json():
    data = {
        'field': 'value'
    }
    builder = EnvironBuilder(
        path='/endpoint', method='POST', data=json.dumps(data),
        content_type='application/json',
    )
    env = builder.get_environ()
    req = Request(env)
    rv = req.get_data()
    assert isinstance(rv, str)
    assert json.loads(rv) == data


def test_get_json_ok():
    data = {
        'field': 'value'
    }
    builder = EnvironBuilder(
        path='/endpoint', method='POST', data=json.dumps(data),
        content_type='application/json',
    )
    env = builder.get_environ()
    req = Request(env)
    rv = req.get_json()
    assert isinstance(rv, dict)
    assert rv == data


def test_get_json_custom_decoder(custom_decoder):
    data = {
        'field': 'value'
    }
    builder = EnvironBuilder(
        path='/endpoint', method='POST', data=json.dumps(data),
        content_type='application/json',
    )
    env = builder.get_environ()
    req = Request(env)
    rv = req.get_json(decoder=custom_decoder)
    assert isinstance(rv, dict)
    assert rv == data
