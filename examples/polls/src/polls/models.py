import os
from datetime import datetime

from pony.orm import Database, Optional, Required, Set

db = Database()


class Poll(db.Entity):
    title = Required(str)
    description = Optional(str)
    created = Required(datetime, default=datetime.utcnow)
    options = Set(lambda: Option)


class Option(db.Entity):
    name = Required(str)
    poll = Required(Poll)
    votes = Set(lambda: Vote)


class Vote(db.Entity):
    option = Required(Option)
    date = Required(datetime, default=datetime.utcnow)


db.bind(provider='sqlite', filename=os.environ['POLLS_DB'], create_db=True)
db.generate_mapping(create_tables=True)
