from handlers_base import BaseHandler
import dao_collection

class UpdateDataHandler(BaseHandler):

    def get(self):

        ndb_armies = dao_collection.GetArmySummary()
        
        self.renderResponse(
            'data/home.html',
            ndb_armies=ndb_armies,
        )

class DeleteDataHandler(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'data/home.html',
        )

class UpdateCacheHandler(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'data/home.html',
        )

class DeleteCacheHandler(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'data/home.html',
        )
