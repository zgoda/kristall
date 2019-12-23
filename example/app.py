from kristall.application import Application
from werkzeug.serving import run_simple


class Resource:

    def get(self, request):
        return {'message': 'Hi there'}


def make_app():
    app = Application()
    app.add_resource('/hello', Resource())
    return app


app = make_app()

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True)
