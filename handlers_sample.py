from handlers_base import BaseHandler

class HomePage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/product_home.html',
        )

class ListingPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/product_listing.html',
        )

class DetailPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/product_detail.html',
        )

class SearchPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/home.html',
        )

class SearchResultsPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/search_results.html',
        )
        
class ArticlePage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/home.html',
        )
        
class InfiniteScrollPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/home.html',
        )

class MWebPage(BaseHandler):

    def get(self):
        
        self.renderResponse(
            'sample/home.html',
        )

