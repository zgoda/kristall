import os

from tinydb import TinyDB

db = TinyDB(os.environ['POLLS_DB'])
