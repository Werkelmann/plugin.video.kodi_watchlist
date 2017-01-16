import sys
import json
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from api_wrapper import Wrapper
from library_wrapper import Library
from difflib import SequenceMatcher as SeqMatcher

SETTING_SESSION_ID = 'session_id'

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')


# Read TheMovieDB-API-Key from plugin source
def get_key_path():
    root_path = xbmc.translatePath('special://home')
    if xbmc.getCondVisibility('system.platform.windows'):
        return root_path + 'addons\\plugin.video.kodi_watchlist\\key.txt'
    if xbmc.getCondVisibility('system.platform.linux'):
        return root_path + 'addons/plugin.video.kodi_watchlist/key.txt'  # TODO linux support is untested

api_key = open(get_key_path()).read().rstrip()
moviedb = Wrapper(api_key)
library = Library()


# init a session id for the user
def authenticate():
    setting_session_id = xbmcplugin.getSetting(addon_handle, SETTING_SESSION_ID)
    if setting_session_id == '':
        req_tok = moviedb.get_request_token()
        xbmcgui.Dialog().ok(__addonname__, 'Call https://www.themoviedb.org/authenticate/ ' + req_tok
                            + ' from your browser and validate the token')
        try:
            session_id = moviedb.get_session_id(req_tok)
            xbmcgui.Dialog().ok(__addonname__, 'Save the following to your settings: ' + session_id
                                + ". Then restart the plugin")
            xbmcplugin.endOfDirectory(addon_handle)
        except urllib2.HTTPError:
            xbmcgui.Dialog().ok(__addonname__, 'Token was not successfully allowed')
            xbmcplugin.endOfDirectory(addon_handle)


# Navigation
def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)


def add_movie_to_list(movie, movies_in_library):
    icon_image = 'DefaultVideo.png'
    path_to_file = ''
    for movie_in_lib in movies_in_library['result']['movies']:
        if SeqMatcher(None, movie['title'], movie_in_lib['title']).ratio() > 0.9:
            icon_image = movie_in_lib['thumbnail']
            path_to_file = movie_in_lib['file']
    li = xbmcgui.ListItem(movie['title'], thumbnailImage=icon_image, path=path_to_file)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=path_to_file, listitem=li)


def add_show_to_list(show, shows_in_library):
    icon_image = 'DefaultVideo.png'
    path_to_file = ''
    for show_in_lib in shows_in_library['result']['tvshows']:
        if SeqMatcher(None, show['name'], show_in_lib['title']).ratio() > 0.9:
            icon_image = show_in_lib['thumbnail']
            path_to_file = show_in_lib['file']
    li = xbmcgui.ListItem(show['name'], thumbnailImage=icon_image, path=path_to_file)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=path_to_file, listitem=li, isFolder=True)

args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)
# Menu to choose movies or shows
if mode is None:
    authenticate()
    movies_url = build_url({'mode': 'folder', 'foldername': 'movies'})
    movies_li = xbmcgui.ListItem('Movies', iconImage='DefaultMovies.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=movies_url, listitem=movies_li, isFolder=True)
    shows_url = build_url({'mode': 'folder', 'foldername': 'shows'})
    shows_li = xbmcgui.ListItem('TV shows', iconImage='DefaultTVShows.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=shows_url, listitem=shows_li, isFolder=True)

# movie and show lists
elif mode[0] == 'folder':
    session_id = xbmcaddon.Addon().getSetting(SETTING_SESSION_ID)  # does not work with xbmcplugin...
    folder_name = args['foldername'][0]
    if folder_name == 'movies':
        movie_watchlist = moviedb.get_sorted_movie_watchlist(session_id)
        movies_in_library = library.get_movies()
        for movie in movie_watchlist:
            add_movie_to_list(movie, movies_in_library)
    elif folder_name == 'shows':
        tv_watchlist = moviedb.get_sorted_tv_watchlist(session_id)
        shows_in_library = library.get_shows()
        for show in tv_watchlist:
            add_show_to_list(show, shows_in_library)

# for movie in library.get_movies()['result']['movies']:
# xbmcgui.Dialog().ok(__addonname__, json.dumps(library.get_shows()))
xbmcplugin.endOfDirectory(addon_handle)
