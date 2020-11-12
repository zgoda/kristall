from kristall.response import Response


def test_create_default_response():
    rv = Response('test')
    assert rv.mimetype == 'application/json'
