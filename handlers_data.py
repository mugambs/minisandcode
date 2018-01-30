from handlers_base import BaseHandler

class UpdateDataHandler(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'data/home.html',
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
