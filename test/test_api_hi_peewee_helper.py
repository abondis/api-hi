import unittest as u
from api_hi.helpers import PeeweeHelper

from fakes import PeeweeSimpleDB, PeeweeDBRel, PeeweeDBFK
from fakes import setup_peewee_db, teardown_peewee_db


class TestPeeweeHelper(u.TestCase):
    """Feature: we got helpers to do simple sqla queries"""
    def setUp(self):
        setup_peewee_db()
        self.simple = PeeweeHelper(PeeweeSimpleDB)
        self.fk = PeeweeHelper(PeeweeDBFK)
        self.rel = PeeweeHelper(PeeweeDBRel)

    def tearDown(self):
        teardown_peewee_db()

    def test_get_columns(self):
        """Scenario: get the columns of the model"""
        rel_cols = set(
            [PeeweeDBRel.relaters, PeeweeDBRel.content, PeeweeDBRel.id])
        self.assertEquals(rel_cols, self.rel.columns())

    def test_get_filtered_columns(self):
        """Scenario: get the filtered columns of the model"""
        rel_cols = set([PeeweeDBRel.relaters, PeeweeDBRel.id])
        self.assertEquals(rel_cols, self.rel.columns(['relaters', 'id']))

    def test_get_relations(self):
        """Get relations from an entry"""
        entry = PeeweeDBRel.select().first()
        rels = {'relaters': [x.id for x in entry.relaters]}
        result = self.rel.get_relations(entry)
        self.assertEquals(rels, result)

    def test_get_filtered_relations(self):
        """Get relations from an entry"""
        entry = PeeweeDBRel.select(PeeweeDBRel.id).first()
        rels = {}
        result = self.rel.get_relations(entry, ['id'])
        self.assertEquals(rels, result)

    def test_select(self):
        """Scenario: we get a list of simple entries
        ie: table with one primary key, and no references"""
        entries = PeeweeDBRel.select()
        result = self.rel.select()
        self.assertEquals(entries, result)

    def test_where(self):
        """We want specific ID details"""
        entries = PeeweeDBRel.select()
        entry = entries.first()._data
        entry['relaters'] = [1, 2, 3]
        result = self.rel.where(entries, 1)
        self.assertEquals(entry, result['result'])

    def test_all(self):
        """We want all the entries"""
        entries = PeeweeDBRel.select()
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
