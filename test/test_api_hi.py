import unittest as u

from fakes import PeeweeSimpleDB, PeeweeDBRel, PeeweeDBFK
from fakes import setup_peewee_db, teardown_peewee_db
from fakes import SQLASimpleDB, SQLADBRel, SQLADBFK
from fakes import setup_sqla_db, teardown_sqla_db
from fakes import bottleapp, bottle_auth_decorator

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
    webapp = None
    webauth = None
    db_setup = None
    db_teardown = None

    def setUp(self):
        """ Given a Model
        and a web app
        and a path
        and a GET method
        """
        self.db_setup.im_func()
        self.app = self.webapp()
        self.check = self.webapp()
        #trick: we want the function to stay unbound and not get self...
        self.auth = self.webauth.im_func
        self.datas = [
            {'id': 1, 'content': u'entry1'},
            {'id': 2, 'content': u'entry2'},
            {'id': 3, 'content': u'entry3'},
        ]
        self.path = '/api/test'
        self.api = api_hi(
            self.path, self.dbrel, self.app, ['GET'], self.auth)

    def tearDown(self):
        self.db_teardown.im_func()

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


TestBottleAPIPeewee = type('MapBasicAPIToPeeweeModel',
                           (MapBasicAPIToModel,), dict(
                               simpledb=PeeweeSimpleDB,
                               dbrel=PeeweeDBRel,
                               dbfk=PeeweeDBFK,
                               db_setup=setup_peewee_db,
                               db_teardown=teardown_peewee_db,
                               webapp=bottleapp,
                               webauth=bottle_auth_decorator(True),))

TestBottleAPISQLA = type('MapBasicAPIToSQLAModel',
                         (MapBasicAPIToModel,), dict(
                             simpledb=SQLASimpleDB,
                             dbrel=SQLADBRel,
                             dbfk=SQLADBFK,
                             db_setup=setup_sqla_db,
                             db_teardown=teardown_sqla_db,
                             webapp=bottleapp,
                             webauth=bottle_auth_decorator(True),))

del MapBasicAPIToModel
