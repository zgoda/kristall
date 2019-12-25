from marshmallow import Schema, fields


class PollSchema(Schema):
    poll_id = fields.UUID()
    title = fields.String()
    open_dt = fields.DateTime()
    close_dt = fields.DateTime()


poll_schema = PollSchema()
