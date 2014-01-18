import unittest as u
from api_hi.helpers import SQLAHelper

from fakes import SQLASimpleDB, SQLADBRel, SQLADBFK
from fakes import setup_sqla_db, teardown_sqla_db


class TestSQLAHelper(u.TestCase):
    """Feature: we got helpers to do simple sqla queries"""
    def setUp(self):
        setup_sqla_db()
        self.simple = SQLAHelper(SQLASimpleDB)
        self.fk = SQLAHelper(SQLADBFK)
        self.rel = SQLAHelper(SQLADBRel)

    def tearDown(self):
        teardown_sqla_db()

    def test_get_columns(self):
        """Scenario: get the columns of the model"""
        rel_cols = set(
            [SQLADBRel.relaters, SQLADBRel.content, SQLADBRel.id])
        self.assertEquals(rel_cols, self.rel.columns())

    def test_get_filtered_columns(self):
        """Scenario: get the filtered columns of the model"""
        rel_cols = set([SQLADBRel.relaters, SQLADBRel.id])
        self.assertEquals(rel_cols, self.rel.columns(['relaters', 'id']))

    def test_get_relations(self):
        """Get relations from an entry"""
        entry = SQLADBRel.select().first()
        rels = {'relaters': [x.id for x in entry.relaters]}
        result = self.rel.get_relations(entry)
        self.assertEquals(rels, result)

    def test_get_filtered_relations(self):
        """Get relations from an entry"""
        entry = SQLADBRel.select(SQLADBRel.id).first()
        rels = {}
        result = self.rel.get_relations(entry, ['id'])
        self.assertEquals(rels, result)

    def test_select(self):
        """Scenario: we get a list of simple entries
        ie: table with one primary key, and no references"""
        entries = SQLADBRel.select()
        result = self.rel.select()
        self.assertEquals(entries, result)

    def test_where(self):
        """We want specific ID details"""
        entries = SQLADBRel.select()
        entry = entries.first()._data
        entry['relaters'] = [1, 2, 3]
        result = self.rel.where(entries, 1)
        self.assertEquals(entry, result['result'])

    def test_all(self):
        """We want all the entries"""
        entries = SQLADBRel.select()
        entry = list(entries.dicts())
        first = entry[0]
        first['relaters'] = [1, 2, 3]
        second = entry[1]
        second['relaters'] = []
        result = self.rel.all(entries)
        self.assertEquals(first, result['result'][0])
        self.assertEquals(second, result['result'][1])

    def test_add(self):
        """We add an entry"""
        entry = {'content': u'entry4'}
        result = self.rel.add(**entry)
        exp = entry
        exp['id'] = 4
        self.assertEquals(exp, result)

    def test_update(self):
        """We update an entry"""
        entry = {'content': u'entry4'}
        result = self.rel.update(1, **entry)
        exp = entry
        exp['id'] = 1
        self.assertEquals(exp, result)

    def test_delete(self):
        """We delete an entry"""
        self.rel.delete(1)
        entries = self.rel.model.select()
        self.assertEquals(None, self.rel.where(entries, 1)['result'])
