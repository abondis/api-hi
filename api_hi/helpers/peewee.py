class PeeweeHelper:
    """map Apify methods to peewee queries
    and other helpers"""
    def __init__(self, model):
        self.model = model

    def columns(self, select=None):
        """Get a list of filtered columns of the model"""
        cols = []
        for col_name, col_obj in self.model._meta.fields.iteritems():
            if select is None or col_name in select:
                cols.append(col_obj)
        if self.model._meta.rel_exists:
            for r in self.model._meta.reverse_rel:
                if select is None or r in select:
                    cols.append(getattr(self.model, r))
        return set(cols)

    def get_relations(self, entry, select=None):
        """Get filtered list of relations in an entry, usefull to
        append the relaters to the fields"""
        rels = {}
        if self.model._meta.rel_exists:
            for r in self.model._meta.reverse_rel:
                if select is None or r in select:
                    rels[r] = [rel.id for rel in getattr(entry, r)]
        return rels

    def select(self, select=None):
        """Prepare a query"""
        print(select)
        if select is not None:
            if 'id' not in select:
                select.append('id')
            query = self.model.select(*self.columns(select))
        else:
            query = self.model.select()
        return query

    def where(self, query, id, select=None):
        """Return the datas for a specific ID given select options"""
        result = query.where(self.model.id == id).first()
        rels = []
        if result is not None:
            rels = self.get_relations(result, select)
            result = result._data
            result.update(rels)
        return {'result': result}

    def all(self, query, select=None):
        """Select all the results"""
        result = []
        for e in query:
            r = e._data
            rels = self.get_relations(e, select)
            r.update(rels)
            result.append(r)
        return {'result': result}

    def add(self, *args, **kwargs):
        """Create an entry"""
        new = self.model(**kwargs)
        new.save()
        return(new._data)

    def update(self, id, **kwargs):
        """Update an entry"""
        entry = self.model.get(self.model.id == id)
        entry.update(**kwargs).execute()
        entry = self.model.get(self.model.id == id)
        return(entry._data)

    def delete(self, id):
        """Delete an entry"""
        self.model.delete().where(self.model.id == id).execute()
