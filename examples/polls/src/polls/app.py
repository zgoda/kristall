from kristall.application import Application

from . import resource


def create_app():
    app = Application()
    configure_resources(app)
    return app


def configure_resources(app: Application):
    app.add_resource('/poll/<poll_id>', resource.poll_item)
    app.add_resource('/polls', resource.poll_collection)
