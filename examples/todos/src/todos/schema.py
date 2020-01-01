import operator

from marshmallow import Schema, fields, post_dump


class UserSchema(Schema):
    pk = fields.Int(attribute='id')
    name = fields.Str(required=True)
    todos = fields.Nested(
        'TodoSchema', dump_only=True, many=True, only=['pk', 'title', 'done']
    )

    @post_dump
    def sort_todos(self, obj, *args, **kwargs):
        obj['todos'].sort(key=operator.itemgetter('title'))
        return obj


class TodoSchema(Schema):
    pk = fields.Int(attribute='id')
    title = fields.Str(required=True)
    description = fields.Str()
    user = fields.Nested('UserSchema', dump_only=True, only=['pk', 'name'])
    done = fields.Bool()
    created = fields.DateTime(dump_only=True)
    resolved = fields.DateTime()
    comment = fields.Str()


user_schema = UserSchema()
todo_schema = TodoSchema()
