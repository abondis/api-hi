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
