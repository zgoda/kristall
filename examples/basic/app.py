import json

from kristall.application import Application
from werkzeug.serving import run_simple


class Resource1:

    def get(self, request):
        return {'message': 'Hi there'}


class Resource2:

    def get(self, request):
        return json.dumps({'message': 'Hi there'})


class Resource3:

    def post(self, request):
        data = request.get_json()
        return data


def make_app():
    app = Application()
    app.add_resource('/hello1', Resource1())
    app.add_resource('/hello2', Resource2())
    app.add_resource('/hello3', Resource3())
    return app


app = make_app()

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True)
