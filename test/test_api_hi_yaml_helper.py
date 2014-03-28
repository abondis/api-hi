import unittest as u
from api_hi.helpers import YamlHelper

from fakes import YamlDB
from fakes import setup_yaml_db, teardown_yaml_db
YamlDB, YamlHelper


class TestYamlHelper(u.TestCase):
    """Feature: we got helpers to do simple sqla queries"""
    def setUp(self):
        setup_yaml_db()

    def tearDown(self):
        teardown_yaml_db()

    def test_get_columns(self):
        """Scenario: get the columns of the model"""
        self.assertTrue(False)

    def test_get_filtered_columns(self):
        """Scenario: get the filtered columns of the model"""
        self.assertTrue(False)

    def test_get_relations(self):
        """Get relations from an entry"""
        self.assertTrue(False)

    def test_get_filtered_relations(self):
        """Get relations from an entry"""
        self.assertTrue(False)

    def test_select(self):
        """Scenario: we get a list of simple entries
        ie: table with one primary key, and no references"""
        self.assertTrue(False)

    def test_where(self):
        """We want specific ID details"""
        self.assertTrue(False)

    def test_all(self):
        """We want all the entries"""
        self.assertTrue(False)

    def test_add(self):
        """We add an entry"""
        self.assertTrue(False)

    def test_update(self):
        """We update an entry"""
        self.assertTrue(False)

    def test_delete(self):
        """We delete an entry"""
        self.assertTrue(False)
