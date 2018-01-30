from google.appengine.ext import ndb

class CollectionStats(ndb.Model):
    total = ndb.IntegerProperty()
    made = ndb.IntegerProperty()
    based = ndb.IntegerProperty()
    sanded = ndb.IntegerProperty()
    sprayed = ndb.IntegerProperty()
    magnetised = ndb.IntegerProperty()
    painted = ndb.IntegerProperty()
    
    def countRemaining(self, stage):
        return total - getattr(self, stage)
    
    def percentComplete(self, stage):
        remaining = countRemaining(self, stage)
        return (remaining / total) * 100
    
class CollectionUnit(ndb.Model):
    key = ndb.StringProperty()
    name = ndb.StringProperty()
    type = ndb.IntegerProperty()
    stats = ndb.StructuredProperty(CollectionStats)

class CollectionArmy(ndb.Model):
    key = ndb.StringProperty()
    name = ndb.StringProperty()
    system = ndb.IntegerProperty()
    stats = ndb.StructuredProperty(CollectionStats)
    units = ndb.StructuredProperty(CollectionUnit, repeated=True)
    