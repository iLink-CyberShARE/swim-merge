import json

class Provenance(object):

    def __init__(self, id, entity, wasGeneratedBy, generatedAtTime):
        self.id = id
        self.entity = entity
        self.wasGeneratedBy = wasGeneratedBy
        self.generatedAtTime = generatedAtTime


    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
        

