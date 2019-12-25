from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import ClassVar, Optional
from uuid import UUID, uuid4

from tinydb import TinyDB, where

from .schema import PollSchema, poll_schema

db = TinyDB(os.environ['POLLS_DB'])


@dataclass
class Poll:
    poll_id: UUID
    title: str
    open_dt: datetime
    close_dt: datetime

    schema: ClassVar[PollSchema] = poll_schema

    @classmethod
    def create(
                cls, title: str,
                start_date: Optional[datetime] = None,
                end_date: Optional[datetime] = None
            ) -> Poll:
        if start_date is None:
            start_date = datetime.utcnow()
        if end_date is None:
            end_date = start_date + timedelta(days=14)
        poll_id = uuid4()
        return cls(poll_id=poll_id, title=title, open_dt=start_date, close_dt=end_date)

    def save(self):
        doc = self.schema.dump(self)
        db.upsert(doc, where('poll_id') == self.poll_id)
