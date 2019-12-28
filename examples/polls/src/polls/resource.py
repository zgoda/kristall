from datetime import datetime, timedelta
from typing import List
from uuid import uuid4

from tinydb import where
from werkzeug.exceptions import NotFound

from kristall.request import Request
from kristall.response import Response
from kristall.utils import url_for

from .models import db
from .schema import poll_schema


class PollItemResource:

    def get(self, request: Request, poll_id: str) -> dict:
        data = db.search(where('poll_id') == poll_id)
        if data:
            return data[0]
        raise NotFound()

    def patch(self, request: Request, poll_id: str) -> dict:
        poll = db.search(where('poll_id') == poll_id)
        if poll:
            poll = poll[0]
        else:
            raise NotFound()
        data = poll_schema.loads(request.get_data(), partial=True)
        poll.update(data)
        db.update(poll, where('poll_id') == poll_id)
        data = poll_schema.load(poll)
        return poll_schema.dump(data)

    def delete(self, request: Request, poll_id: str) -> Response:
        poll = db.search(where('poll_id') == poll_id)
        if poll:
            poll = poll[0]
        else:
            raise NotFound()
        db.remove(where('poll_id') == poll_id)
        return Response(status=204)


poll_item = PollItemResource()


class PollCollectionResource:

    def get(self, request: Request) -> List[dict]:
        data = db.search(where('poll_id').exists())
        return data

    def post(self, request: Request) -> Response:
        poll = poll_schema.loads(request.get_data(), partial=True)
        poll_id = uuid4()
        poll['poll_id'] = poll_id
        now = datetime.utcnow()
        if not poll.get('open_dt'):
            poll['open_dt'] = now
        if not poll.get('close_dt'):
            poll['close_dt'] = now + timedelta(days=14)
        db.insert(poll_schema.dump(poll))
        return Response(
            status=201,
            headers={
                'Location': url_for(
                    'polls.resource.PollItemResource', poll_id=poll_id
                )
            }
        )


poll_collection = PollCollectionResource()
