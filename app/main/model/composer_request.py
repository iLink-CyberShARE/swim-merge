import mongoengine as db

class ComposerRequest(db.Document):
    flowid = db.StringField(required=True)
    inputs = db.ListField(db.StringField())
    outputs =db.ListField(db.StringField())

    meta = {
        'collection': 'composerinputs',
        'db_alias': 'workflow-db-alias'
    }