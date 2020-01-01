from typing import List

from pony.orm import db_session
from werkzeug.exceptions import NotFound

from kristall.request import Request
from kristall.response import Response

from .models import Poll, db
from .schema import poll_schema


class PollItemResource:

    @db_session
    def get(self, request: Request, poll_id: str) -> dict:
        poll = Poll.get(id=poll_id)
        if poll:
            return poll_schema.dumps(poll)
        raise NotFound()

    @db_session
    def patch(self, request: Request, poll_id: str) -> dict:
        poll = Poll.get(id=poll_id)
        if not poll:
            raise NotFound()
        data = poll_schema.loads(request.get_data(), partial=True)
        poll.set(**data)
        return poll_schema.dumps(poll)

    @db_session
    def delete(self, request: Request, poll_id: str) -> Response:
        poll = Poll.get(id=poll_id)
        if not poll:
            raise NotFound()
        poll.delete()
        return Response(status=204)


poll_item = PollItemResource()


class PollCollectionResource:

    @db_session
    def get(self, request: Request) -> List[dict]:
        polls = Poll.select().order_by(Poll.title)
        return poll_schema.dumps(polls, many=True)

    @db_session
    def post(self, request: Request) -> Response:
        data = poll_schema.loads(request.get_data(), partial=True)
        poll = Poll(**data)
        db.commit()
        return Response(
            status=201, headers={'Location': f'/poll/{poll.id}'}
        )


poll_collection = PollCollectionResource()
