import urllib2
import json


class Wrapper:

    def __init__(self, api_key):
        self.key = api_key
        self.API_ROOT = 'https://api.themoviedb.org/3/'

    def add_api_key(self):
        return '?api_key=' + self.key

    def get_value_from_response(self, api_url, key):
        http_response = urllib2.urlopen(api_url)
        json_response = http_response.read().decode('utf-8')
        response = json.loads(json_response)
        return response[key]

    def build_api_url(self, resource):
        return self.API_ROOT + resource + self.add_api_key()

    def get_request_token(self):
        token_url = self.build_api_url('authentication/token/new')
        return self.get_value_from_response(token_url, 'request_token')

    def get_query_string_postfix(self, name, value):
        return '&{name}={value}'.format(name=name, value=value)

    def get_session_id(self, req_tok):
        session_url = self.build_api_url('authentication/session/new') + \
                      self.get_query_string_postfix('request_token', req_tok)
        return self.get_value_from_response(session_url, 'session_id')

    def get_movie_watchlist(self, session_id):
        movie_watchlist_url = self.build_api_url('account/{account_id}/watchlist/movies') \
                              + self.get_query_string_postfix('session_id', session_id)
        return self.get_value_from_response(movie_watchlist_url, 'results')

    def get_sorted_movie_watchlist(self, session_id):
        watch_list = self.get_movie_watchlist(session_id)
        return sorted(watch_list, key=lambda x: x['title'])

    def get_tv_watchlist(self, session_id):
        show_watchlist_url = self.build_api_url('account/{account_id}/watchlist/tv') \
                             + self.get_query_string_postfix('session_id', session_id)
        return self.get_value_from_response(show_watchlist_url, 'results')

    def get_sorted_tv_watchlist(self, session_id):
        watch_list = self.get_tv_watchlist(session_id)
        return sorted(watch_list, key=lambda x: x['name'])
