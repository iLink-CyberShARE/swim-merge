import mongoengine as db

class ModelOutput(db.EmbeddedDocument):
    modelID = db.StringField(required=True)
    varName = db.StringField(required=True)
    varBenchMarks = db.ListField(required=False)
    varinfo = db.ListField(required=False)
    varValue = db.DynamicField(required=False)