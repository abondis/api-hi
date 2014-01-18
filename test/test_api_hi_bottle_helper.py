import unittest as u
from api_hi.helpers import BottleHelper
from bottle import Bottle

app = Bottle()


class TestBottleHelper(u.TestCase):
    """Test bottlepy helper"""
    def setUp(self):
        self.helper = BottleHelper(app)

    def test_route(self):
        """Scenario: we add a route"""
        self.assertEquals(app.routes, self.helper.app.routes)
        self.helper.route('/test', lambda: True, ['GET', 'POST'])
        self.assertEquals(app.routes, self.helper.app.routes)

    def test_get_request_datas(self):
        """Scenario: we need to get some data from the request
        """
        self.assertIsNone(
            self.helper.request('test'))
        self.assertIsNone(
            self.helper.request(['test']))
