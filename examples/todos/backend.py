from datetime import datetime, timezone

from peewee import (
    BooleanField, CharField, DateTimeField, Model, SqliteDatabase, TextField,
)
from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple

from kristall.application import Application
from kristall.response import Response

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
        ret = {
            'title': self.title,
            'description': self.description,
            'dateAdded': self.added.replace(tzinfo=timezone.utc).timestamp(),
            'isComplete': self.is_complete,
            'dateCompleted': None
        }
        if self.is_complete:
            ts = self.completed.replace(tzinfo=timezone.utc).timestamp()
            ret['dateCompleted'] = ts
        return ret


class TodoResource:

    def get(self, request, todo_id):
        try:
            todo = Todo.get_by_id(todo_id)
        except Todo.DoesNotExist:
            raise NotFound()
        return todo.as_dict()

    def put(self, request, todo_id):
        try:
            Todo.get_by_id(todo_id)
        except Todo.DoesNotExist:
            raise NotFound()
        data = request.get_json()
        data['is_complete'] = data.pop('isComplete', False)
        if data['is_complete']:
            data['completed'] = datetime.utcnow()
        Todo.update(**data).where(Todo.id == todo_id).execute()
        return Response(status=200, headers={'Location': f'/todo/{todo_id}'})


class TodoCollectionResource:

    def post(self, request):
        data = request.get_json()
        is_complete = data.pop('isComplete', False)
        if is_complete:
            data['completed'] = datetime.utcnow()
        todo = Todo.create(is_complete=is_complete, **data)
        return Response(status=201, headers={'Location': f'/todo/{todo.id}'})

    def get(self, request):
        todos = [t.as_dict() for t in Todo.select().order_by(Todo.added)]
        return {'todos': todos}


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
