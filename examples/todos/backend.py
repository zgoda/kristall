from datetime import datetime

from peewee import (
    BooleanField, CharField, DateTimeField, Model, SqliteDatabase, TextField,
)
from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple

from kristall.application import Application

sqlite_pragmas = {
    'journal_mode': 'wal',
    'cache_size': -64 * 1000,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
}

db = SqliteDatabase('todos.sqlite', pragmas=sqlite_pragmas)


def db_connect(*args, **kw):
    db.connect(reuse_if_open=True)


def db_close(*args, **kw):
    if not db.is_closed():
        db.close()


class Todo(Model):
    title = CharField(max_length=200)
    description = TextField(null=True)
    added = DateTimeField(default=datetime.utcnow, index=True)
    is_complete = BooleanField(default=False)
    completed = DateTimeField(null=True)

    class Meta:
        database = db

    def as_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'dateAdded': self.added.isoformat(),
            'isComplete': self.is_complete,
            'dateCompleted': self.completed.isoformat(),
        }


class TodoResource:

    def get(self, request, todo_id):
        try:
            todo = Todo.get_by_id(todo_id)
        except Todo.DoesNotExist:
            raise NotFound()
        return todo.as_dict()


class TodoCollectionResource:

    def get(self, request):
        pass


def make_app() -> Application:
    app = Application()
    app.add_before_request(db_connect)
    app.add_after_request(db_close)
    app.add_resource('/todos', TodoCollectionResource())
    app.add_resource('/todo/<int:todo_id>', TodoResource())
    return app


def main():
    db.create_tables([Todo])
    app = make_app()
    run_simple('127.0.0.1', 5000, app, use_reloader=True)


if __name__ == '__main__':
    main()
