import sqlalchemy as sa


class SQLAHelper:
    """map Apify methods to sqlalchemy queries
    and other helpers"""
    def __init__(self, model):
        self.model = model

    def _get_relations_names(self):
        return filter(
            lambda p: isinstance(p, sa.orm.properties.RelationshipProperty),
            sa.orm.class_mapper(self.model).iterate_properties
        )

    def columns(self, select=None):
        """Get a list of filtered columns of the model"""
        cols = []
        for col_name, col_obj in \
                self.model.__table__.columns._data.iteritems():
            if select is None or col_name in select:
                cols.append(getattr(self.model, col_name))
        rels = self._get_relations_names()
        if len(rels) > 0:
            for r in rels:
                if select is None or r.key in select:
                    cols.append(getattr(self.model, r.key))
        return set(cols)

    def get_relations(self, entry, select=None):
        """Get filtered list of (objects) relations in an entry, usefull to
        append the relaters to the fields"""
        rel_dict = {}
        rels = self._get_relations_names()
        if len(rels) > 0:
            for r in rels:
                if select is None or r.key in select:
                    rel_dict[r.key] = [rel.id for rel in getattr(entry, r.key)]
        return rel_dict

    def select(self, select=None):
        """Prepare a query"""
        print(select)
        if select is not None:
            if 'id' not in select:
                select.append('id')
            query = self.model.s.query(*self.columns(select)).all()
        else:
            query = self.model.s.query(self.model).all()
        return query

    def where(self, query, id, select=None):
        """Return the datas for a specific ID given select options"""
        result = query.filter_by(id=id).first()
        rels = []
        if result is not None:
            rels = self.get_relations(result, select)
            result = self.sqla_to_dict(result)
            result.update(rels)
        return {'result': result}

    def all(self, query, select=None):
        """Select all the results"""
        result = []
        for e in query:
            r = self.sqla_to_dict(e)
            rels = self.get_relations(e, select)
            r.update(rels)
            result.append(r)
        return {'result': result}

    def add(self, *args, **kwargs):
        """Create an entry
        to add a relation, add the related first
        then add the relater
        """
        new = self.model(**kwargs)
        self.model.s.add(new)
        self.model.s.flush()
        return(self.sqla_to_dict(new))

    def update(self, id, **kwargs):
        """Update an entry"""
        entry = self.model.query.get(id)
        for k in kwargs:
            setattr(entry, k, kwargs[k])
        self.model.s.add(entry)
        self.model.s.flush()
        return(self.sqla_to_dict(entry))

    def delete(self, id):
        """Delete an entry"""
        entry = self.model.query.get(id)
        self.model.s.delete(entry)
        self.model.s.flush()

    # sqlalchemy to_dict
    def sqla_to_dict(self, entry):
        #http://stackoverflow.com/questions/1958219/\
            #convert-sqlalchemy-row-object-to-python-dict
        if entry is None:
            return {}
        return {
            c.name: getattr(entry, c.name)
            for c in entry.__table__.columns}


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

from bottle import request


class BottleHelper:
    """map Apify methods to Bottle magic
    and other helpers"""
    def __init__(self, app):
        self.app = app

    def route(self, path, function, methods=['GET']):
        self.app.route(path, method=methods, callback=function)

    def request(self, items=None):
        if request.json is not None:
            datas = request.json
        else:
            if hasattr(request, 'params'):
                datas = request.params.dict
            else:
                return None
        if items is None:
            return datas
        elif isinstance(items, list):
            ret = {}
            for i in items:
                data = datas.get(i)
                ret[i] = data
            return ret
        else:
            return datas.get(items)


class FlaskHelper:
    """map Apify methods to Flask magic
    and other helpers"""
    pass
