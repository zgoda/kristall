import os
from datetime import datetime

from pony.orm import Database, Optional, Required, Set

db = Database()


class User(db.Entity):
    name = Required(str)
    todos = Set('Todo')


class Todo(db.Entity):
    title = Required(str)
    description = Optional(str)
    user = Required(User)
    done = Required(bool, default=False)
    created = Required(datetime, default=datetime.utcnow)
    resolved = Optional(datetime)
    comment = Optional(str)


db.bind(provider='sqlite', filename=os.environ['TODOS_DB'], create_db=True)
db.generate_mapping(create_tables=True)
