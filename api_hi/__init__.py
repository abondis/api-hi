"""
An API
Over a DB
using a web framework
"""

"""
The API should
build over an instance (app) of the web framework
ie: app = Bottle()
and a DB
ie: db = Sqlalchemy('sqlite:memory')
"""
#FIXME: restrict display to specific fields
#
# 'file': {'model': File, 'display': 'publicfield'}
# if 'display' in model.get('file'):
#   displays = model.get('file').get('display')
#   result = []
#   for d in query:
#       data = {k:getattr(d, k) for k in displays}
#TODO: list attributes of each result directly in /api/model
#allow request to ask only for some attributes ie: fields=a,b


class Apify(object):
    functions = [
        {'method': 'GET', 'function': 'get', 'map': ['', '/<id>']},
        {'method': 'POST', 'function': 'post', 'map': ['']},
        {'method': 'DELETE', 'function': 'delete', 'map': ['/<id>']},
        {'method': 'PUT', 'function': 'put', 'map': ['/<id>']},
    ]

    def __init__(self, path, model, app, methods=['GET'], auth=None):
        """
        path: url to map the model to
        model: model object to map the url to
        app: web app instance
        methods: list, GET POST ... defaults to GET
        auth: authentication decorator
        ex:
        if @require('admin') needs to decorate the route, pass require('admin')
        if @require needs to decorate the route, pass require
        """
        self.model = model  # object
        self.app = app  # instance
        if auth is not None:
            self.get = auth(self.get)
            self.post = auth(self.post)
        if path.endswith('/'):
            path = path[:-1]
        self.path = path
        self.methods = methods  # list
        #self.route = self.app.route
        for f in self.functions:
            if f['method'] in methods:
                func = getattr(self, f['function'])
                for path in f['map']:
                    self.route(self.path + path, func, f['method'])

    def get(self, id=None):
        """ this is the api's get function,
        it takes the arguments passed from the route
        """
        select_columns = self.request('select_columns')
        if select_columns is not None:
            select_columns = select_columns.split(',')
        query = self.select(select_columns)
        if id is not None:
            result = self.where(query, id, select_columns)
        else:
            result = self.all(query, select_columns)
        return(result)

    def post(self):
        datas = self.request()
        return self.add(**datas)

    def delete(self, id):
        """Delete something"""
        return self.delete(id)

    def update(self, id):
        """Update an entry"""
        datas = self.request()
        return self.update(id, **datas)

from api_hi.helpers import PeeweeHelper
from api_hi.helpers import BottleHelper
# module, model, helper
db_helpers = [
    {'module': 'peewee',
     'class': 'Model',
     'helper': PeeweeHelper}]
web_helpers = [
    {'module': 'bottle',
     'class': 'Bottle',
     'helper': BottleHelper}]
import sys


def get_helper(obj, helpers):
    """returns the helper for the class of 'obj' or raise an exception"""
    helper = None
    for h in helpers:
        if h['module'] in sys.modules:
            module = sys.modules[h['module']]
            cls = getattr(module, h['class'])
            if issubclass(obj, cls):
                helper = h['helper']
    if helper is None:
        raise(Exception, "This type of helper is not implemented yet %s"
              % obj.__class__)
    return helper


def api_hi(path, model, app, methods=['GET'], auth=None):
    """Meta? determines which helper to use depending on app type
    and model class"""
    db_helper = get_helper(model, db_helpers)
    web_helper = get_helper(type(app), web_helpers)
    API = type('API', (Apify, db_helper, web_helper), {})
    return API(path, model, app, methods, auth)
