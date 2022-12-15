import mongoengine as db

class FlowMap(db.Document):
    _id = db.StringField(primary_key=True)
    className = db.StringField(required=False)
    flowID = db.StringField(required=True)
    modelID = db.StringField(required=True)
    catalogID = db.StringField(required=True)
    swimID = db.StringField(required=True)
    type = db.StringField(required=True)
    paramValue = db.DynamicField(required=False)
    meta = {
        'collection': 'flowmappings',
        'db_alias': 'workflow-db-alias'
    }