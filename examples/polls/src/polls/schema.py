from marshmallow import Schema, fields


class VoteSchema(Schema):
    pk = fields.Int(dump_only=True, attribute='id')
    date = fields.DateTime()


class OptionSchema(Schema):
    pk = fields.Int(dump_only=True, attribute='id')
    name = fields.String()
    votes = fields.Nested('VoteSchema', only=['date'], many=True, dump_only=True)


class PollSchema(Schema):
    pk = fields.Int(dump_only=True, attribute='id')
    title = fields.Str()
    created = fields.DateTime(dump_only=True)
    options = fields.Nested(
        'OptionSchema', only=['pk', 'name'], many=True, dump_only=True
    )


poll_schema = PollSchema()
