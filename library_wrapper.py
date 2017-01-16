import json
import xbmc


# https://github.com/BigNoid/service.library.data.provider/blob/master/library.py
class Library:

    def __init__(self):
        self.movie_properties = [
            # 'file',
            'title',
            'thumbnail']

    def _json_query(self, method):
        json_query = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}
        json_query['params']['properties'] = self.movie_properties
        json_string = json.dumps(json_query)
        return json.loads(xbmc.executeJSONRPC(json_string))
        # return unicode(result, 'utf-8', errors='ignore')

    def get_movies(self):
        return self._json_query('VideoLibrary.GetMovies')
