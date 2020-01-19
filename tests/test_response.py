from kristall.response import Response


class TestResponse:

    def test_create_default(self):
        rv = Response('test')
        assert rv.mimetype == 'application/json'
