import json
import xbmc


class Library:

    def _json_query(self, method):
        json_query = {"jsonrpc": "2.0", "id": 1, "method": method, "params": {}}
        json_string = json.dumps(json_query)
        result = xbmc.executeJSONRPC(json_string)
        return unicode(result, 'utf-8', errors='ignore')

    def get_movies(self):
        return self._json_query('VideoLibrary.GetMovies')
