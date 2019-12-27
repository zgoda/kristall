from marshmallow import Schema, fields


class OptionSchema(Schema):
    name = fields.String()


class PollSchema(Schema):
    poll_id = fields.UUID()
    title = fields.String()
    open_dt = fields.DateTime()
    close_dt = fields.DateTime()
    options = fields.Nested('OptionSchema', many=True)


poll_schema = PollSchema()
