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
        return self.total - getattr(self, stage)
    
    def percentComplete(self, stage):
        remaining = self.countRemaining(stage)
        return 100 - ((remaining * 100) / self.total)
    
class CollectionUnit(ndb.Model):
    key = ndb.StringProperty()
    name = ndb.StringProperty()
    type = ndb.IntegerProperty()
    stats = ndb.StructuredProperty(CollectionStats)

class CollectionArmy(ndb.Model):
    key = ndb.StringProperty()
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    system = ndb.IntegerProperty()
    stats = ndb.StructuredProperty(CollectionStats)
    units = ndb.StructuredProperty(CollectionUnit, repeated=True)
    