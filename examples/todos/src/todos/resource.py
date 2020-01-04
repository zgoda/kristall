from pony.orm import db_session
from werkzeug.exceptions import NotFound

from kristall.request import Request
from kristall.response import Response

from .models import Todo, User, db
from .schema import user_schema, todo_schema


class UserCollectionResource:

    @db_session
    def get(self, request: Request) -> str:
        users = User.select().order_by(User.name)
        return user_schema.dumps(users, many=True)

    @db_session
    def post(self, request: Request) -> Response:
        data = user_schema.loads(request.get_data())
        user = User(**data)
        db.commit()
        data = user_schema.dumps(user)
        return Response(data, headers={'Location': f'/user/{user.id}'})


class UserItemResource:

    @db_session
    def get(self, request: Request, user_id: int) -> str:
        user = User.get(id=user_id)
        if not user:
            raise NotFound(description='')
        return user_schema.dumps(user)


class UserTodoCollectionResource:

    @db_session
    def get(self, request: Request, user_id: int) -> str:
        todos = Todo.select(lambda t: t.user.id == user_id).order_by(Todo.title)
        if not todos:
            raise NotFound(description='')
        return todo_schema.dumps(todos, many=True)

    @db_session
    def post(self, request: Request, user_id: int) -> Response:
        user = User.get(id=user_id)
        if not user:
            raise NotFound(description='')
        data = todo_schema.loads(request.get_data())
        todo = Todo(user=user, **data)
        db.commit()
        return Response(status=201, headers={'Location': f'/todo/{todo.id}'})


class TodoItem:

    @db_session
    def get(self, request: Request, todo_id: int) -> str:
        todo = Todo.get(id=todo_id)
        if not todo:
            raise NotFound(description='')
        return todo_schema.dumps(todo)


user_collection = UserCollectionResource()
user_item = UserItemResource()
user_todo_collection = UserTodoCollectionResource()
todo_item = TodoItem()
