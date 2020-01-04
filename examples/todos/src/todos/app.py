from kristall.application import Application

from . import resource


def create_app():
    app = Application()
    configure_resources(app)
    return app


def configure_resources(app: Application):
    app.add_resource('/user', resource.user_collection)
    app.add_resource('/user/<int:user_id>', resource.user_item)
    app.add_resource('/user/<int:user_id>/todo', resource.user_todo_collection)
    app.add_resource('/todo/<int:todo_id>', resource.todo_item)
