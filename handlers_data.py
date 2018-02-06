from handlers_base import BaseHandler
import dao_collection

class UpdateDataHandler(BaseHandler):

    def get(self):

        dao_collection.DeleteAllNdbData()
        armies_raw = dao_collection.LoadCollectionDataFromSource()
        armies_ndb = dao_collection.GetAllNdbData()
        
        self.renderResponse(
            'data/home.html',
            armies_ndb=armies_ndb,
            armies_raw=armies_raw,
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
