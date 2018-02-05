import os
import jinja2
import webapp2
from webapp2_extras import jinja2

# TODO: move handlers into a subpackage (https://docs.python.org/3/tutorial/modules.html#packages)
import handlers_sample
import handlers_data
import handlers_portfolio
import filters


_TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'template_files')

config = {
    'webapp2_extras.jinja2': {
        'template_path': _TEMPLATES_PATH,
        'environment_args': {
            'autoescape': True,
            'extensions': [
                'jinja2.ext.autoescape',
                'jinja2.ext.do', 
            ],
        },
        'filters': {
            'progress': filters.GetProgressBarColour,
        },
    }
}
# [END imports]

# [START app]
app = webapp2.WSGIApplication([
    ('/collection', handlers_portfolio.CollectionPage),
    
    ('/data/update', handlers_data.UpdateDataHandler),
    ('/data/delete', handlers_data.DeleteDataHandler),
    ('/cache/update', handlers_data.UpdateCacheHandler),
    ('/cache/delete', handlers_data.DeleteCacheHandler),
    
    ('/sample/home', handlers_sample.HomePage),
    ('/sample/listing', handlers_sample.ListingPage),
    ('/sample/detail', handlers_sample.DetailPage),
    ('/sample/search', handlers_sample.SearchPage),
    ('/sample/search/results', handlers_sample.SearchResultsPage),
    ('/sample/article', handlers_sample.ArticlePage),
    ('/sample/infinitescroll', handlers_sample.InfiniteScrollPage),
], config=config, debug=True)
# [END app]