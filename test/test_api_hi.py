import unittest as u


# Fake test objects
## Peewee specific
from peewee import Model, SqliteDatabase, CharField, ForeignKeyField

database = SqliteDatabase(':memory:')


class BaseModel(Model):
    class Meta:
        database = database


class SimpleDB(BaseModel):
    content = CharField()


class DBRel(BaseModel):
    """A DB related to"""
    content = CharField()


class DBFK(BaseModel):
    """A DB with foreign keys"""
    relate_to = ForeignKeyField(DBRel, related_name='relaters')


SimpleDB.create_table()
DBRel.create_table()
DBFK.create_table()

datas = [
    {'content': u'entry1'},
    {'content': u'entry2'},
    {'content': u'entry3'},
]

for d in datas:
    SimpleDB.create(**d)
    DBRel.create(**d)
    DBFK.create(relate_to=1)

model = SimpleDB
import bottle
app = bottle.Bottle


def auth_decorator(arg):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if arg is False:
                raise Exception
            return function(*args, **kwargs)
        return wrapper
    return real_decorator

### End Fake objects

"""
Feature: Basic REST API over Model
      We want to be able to route REST style
      an interface to a Model
  Scenario:
      Given a model mapped to a GET
      When we get with no argument
      then then we should get a list of entries in the model
"""
from api_hi import api_hi


class MapBasicAPIToModel(u.TestCase):
    """ Feature: Basic REST API over Model
    """
    def setUp(self):
        """ Given a Model
        and a web app
        and a path
        and a GET method
        """
        self.datas = [
            {'id': 1, 'content': u'entry1'},
            {'id': 2, 'content': u'entry2'},
            {'id': 3, 'content': u'entry3'},
        ]
        self.app = app()
        self.check = app()
        self.auth = auth_decorator
        self.path = '/api/test'
        self.api = api_hi(
            self.path, self.dbrel, self.app, ['GET'], self.auth(True))

    def test_0_api_hi(self):
        """ Scenario: Map a get URL to a Model
        when Apified
        """
        # then the Api should have a GET route
        self.assertIn('GET', self.api.methods)
        self.check.route('/api/test', ['GET'], lambda: True)
        self.check.route('/api/test/<id>', ['GET'], lambda: True)
        # and the web app should have a GET route
        self.assertEquals(self.api.app.routes[0].rule,
                          self.check.routes[0].rule)

    #should we test get() and post() from here
    #it is already tested from the helpers side


TestAPIPeewee = type('MapBasicAPIToPeeweeModel',
                     (MapBasicAPIToModel,), dict(
                         simpledb=SimpleDB,
                         dbrel=DBRel,
                         dbfk=DBFK))

del MapBasicAPIToModel
