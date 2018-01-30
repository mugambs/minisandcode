"""Base handler class containing some common convenience functions."""

import logging

from google.appengine.api import users
import webapp2
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):
  """Base handler class that should be extended by subcomponents."""

  def isAdmin(self):
    return users.is_current_user_admin()

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  @webapp2.cached_property
  def collection_data(self):
    try:
      data = collection_dao.GetData()
      return data
    except RuntimeError as e:
      logging.warning(e)
      return {}

  def getTemplateValues(self):
    user = users.get_current_user()
    if user:
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
    
    template_values = {
        'user': user,
        'url': url,
        'url_linktext': url_linktext, 
    }    
    return template_values

  def renderResponse(self, template, **context):
    context.update(self.getTemplateValues())
    self.response.write(self.jinja2.render_template(template, **context))
