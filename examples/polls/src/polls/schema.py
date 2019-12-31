from marshmallow import Schema, fields


class VoteSchema(Schema):
    id = fields.Int(dump_only=True)  # noqa: A003
    date = fields.DateTime()


class OptionSchema(Schema):
    id = fields.Int(dump_only=True)  # noqa: A003
    name = fields.String()
    votes = fields.Nested('VoteSchema', only=['date'], many=True, dump_only=True)


class PollSchema(Schema):
    id = fields.Int(dump_only=True)  # noqa: A003
    title = fields.Str()
    created = fields.DateTime(dump_only=True)
    options = fields.Nested(
        'OptionSchema', only=['id', 'name'], many=True, dump_only=True
    )


poll_schema = PollSchema()
