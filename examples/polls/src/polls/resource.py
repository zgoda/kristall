from .models import db

from tinydb import where


class PollItemResource:
    pass


class PollCollectionResource:

    def get(self, request):
        data = db.search(where('poll_id').exists())
        return data


poll_collection = PollCollectionResource()
