class YamlHelper:
    """map Apify methods to yaml 'persistent storage'
    and other helpers
    check https://github.com/clivecrous/yaml-model and
      https://github.com/nicotaing/yaml_record
    Concept:
    model: is a folder
    schema: is free, but mayber later implement a 'schema.yml' file describing
      - no external keys
    entries: are <id>.yml since we (the API) filter only by ID
      - or one single file:
        - advantage: could implement search more easily
        - disadvantages:
             - could end up beeing a big file
               (maybe not for what we are looking for)
             - the file would be loaded in memory
             - more read/write
    Ideas:
      - implement an index to be able to filter by other attributes
      - implement foreign keys (fk: <model>.<key>) ?
    """
    def __init__(self, model):
        self.model = model

    def columns(self, select=None):
        """Get a list of filtered columns of the model
        no schema, what do we want from that ?
        """
        pass

    def get_relations(self, entry, select=None):
        """Get filtered list of relations in an entry, usefull to
        append the relaters to the fields
        no relation, what do we want from that ?
        """
        pass

    def select(self, select=None):
        """Prepare a query
        prepare a query filtering by column selected
        """
        pass

    def where(self, query, id, select=None):
        """Return the datas for a specific ID given select options
        where: id == id
        """
        pass

    def all(self, query, select=None):
        """Select all the results from the 'query'"""
        pass

    def add(self, *args, **kwargs):
        """Create an entry"""
        pass

    def update(self, id, **kwargs):
        """Update an entry"""
        pass

    def delete(self, id):
        """Delete an entry"""
        pass
