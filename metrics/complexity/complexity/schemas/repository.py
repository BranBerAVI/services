from marshmallow import Schema, fields, post_load

from ..models import Change, Changes, Commit, Delta, Deltas, Developer, File, \
                     LastModifier, LineChanges, Message, Module, Move, Moves, \
                     Oids, Patch

class OidsSchema(Schema):
    before = fields.String()
    after = fields.String()

    @post_load
    def make_oids(self, data, **kwargs):
        return Oids(**data)


class ChangeSchema(Schema):
    type = fields.Integer()
    oids = fields.Nested(OidsSchema)

    @post_load
    def make_change(self, data, **kwargs):
        return Change(**data)


class DeltaSchema(Schema):
    insertions = fields.Integer(allow_none=True)
    deletions = fields.Integer(allow_none=True)

    @post_load
    def make_delta(self, data, **kwargs):
        return Delta(**data)


class DeveloperSchema(Schema):
    name = fields.String()
    email = fields.String()

    @post_load
    def make_developer(self, data, **kwargs):
        return Developer(**data)


class CommitSchema(Schema):
    sha = fields.String()
    timestamp = fields.Integer()
    author = fields.Nested(DeveloperSchema)

    @post_load
    def make_commit(self, data, **kwargs):
        return Commit(**data)


class DeltasSchema(Schema):
    commit = fields.Nested(CommitSchema)
    deltas = fields.Dict(fields.String(), fields.Nested(DeltaSchema))

    @post_load
    def make_deltas(self, data, **kwargs):
        return Deltas(**data)


class ChangesSchema(Schema):
    commit = fields.Nested(CommitSchema)
    changes = fields.Dict(fields.String(), fields.Nested(ChangeSchema))

    @post_load
    def make_changes(self, data, **kwargs):
        return Changes(**data)


class LastModifierSchema(Schema):
    line = fields.Integer()
    commit = fields.Nested(CommitSchema)

    @post_load
    def make_lastmodifier(self, data, **kwargs):
        return LastModifier(**data)


class LineChangesSchema(Schema):
    commit = fields.Nested(CommitSchema)
    linechanges = fields.Dict(
        fields.String(),
        fields.Dict(fields.String(), fields.List(fields.Integer()))
    )

    @post_load
    def make_linechanges(self, data, **kwargs):
        return LineChanges(**data)


class MessageSchema(Schema):
    commit = fields.Nested(CommitSchema)
    message = fields.String()

    @post_load
    def make_message(self, data, **kwargs):
        return Message(**data)


class ModuleSchema(Schema):
    path = fields.String()

    @post_load
    def make_module(self, data, **kwargs):
        return Module(**data)


class MoveSchema(Schema):
    source = fields.String()
    destination = fields.String()

    @post_load
    def make_move(self, data, **kwargs):
        return Move(**data)


class MovesSchema(Schema):
    commit = fields.Nested(CommitSchema)
    moves = fields.Nested(MoveSchema, many=True)

    @post_load
    def make_moves(self, data, **kwargs):
        return Moves(**data)


class FileSchema(Schema):
    path = fields.String()
    is_active = fields.Boolean()
    module = fields.Nested(ModuleSchema)

    @post_load
    def make_file(self, data, **kwargs):
        return File(**data)


class PatchSchema(Schema):
    commit = fields.Nested(CommitSchema)
    patch = fields.String()

    @post_load
    def make_patch(self, data, **kwargs):
        return Patch(**data)