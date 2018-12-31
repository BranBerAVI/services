from marshmallow import Schema, fields, post_load

from .models import Commit, Change, Changes, Developer


class ChangeSchema(Schema):
    path = fields.String()
    insertions = fields.Integer(missing=None)
    deletions = fields.Integer(missing=None)

    @post_load
    def make_change(self, data):
        return Change(**data)


class DeveloperSchema(Schema):
    name = fields.String()
    email = fields.String(missing=None)

    @post_load
    def make_developer(self, data):
        return Developer(**data)


class CommitSchema(Schema):
    sha = fields.String()
    timestamp = fields.Integer()
    author = fields.Nested(DeveloperSchema)

    @post_load
    def make_commit(self, data):
        return Commit(**data)


class ChangesSchema(Schema):
    commit = fields.Nested(CommitSchema)
    changes = fields.Nested(ChangeSchema, many=True)

    @post_load
    def make_changes(self, data):
        return Changes(**data)


class CollaborationSchema(Schema):
    path = fields.String()
    collaboration = fields.Float()