import sys
import json
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


SETTING_REQ_TOK = 'req_tok'

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')


def get_key_path():
    root_path = xbmc.translatePath('special://home')
    if xbmc.getCondVisibility('system.platform.windows'):
        return root_path + 'addons\\plugin.video.kodi_watchlist\\key.txt'
    if xbmc.getCondVisibility('system.platform.linux'):
        return root_path + 'addons/plugin.video.kodi_watchlist/key.txt'  # TODO linux support is untested

apiKey = open(get_key_path()).read().rstrip()


def get_api_root():
    return 'https://api.themoviedb.org/3/'


def add_api_key():
    return '?api_key=' + apiKey


def get_value_from_response(api_url, key):
    http_response = urllib2.urlopen(api_url)
    json_response = http_response.read().decode('utf-8')
    response = json.loads(json_response)
    return response[key]


def build_api_url(resource):
    return get_api_root() + resource + add_api_key()


def get_request_token():
    token_url = build_api_url('authentication/token/new')
    return get_value_from_response(token_url, 'request_token')


def get_session_id(req_tok):
    session_url = build_api_url('authentication/session/new') + '&request_token=' + req_tok
    return get_value_from_response(session_url, 'session_id')


if xbmcplugin.getSetting(addon_handle, SETTING_REQ_TOK) == '':
    req_tok = get_request_token()
    xbmcplugin.setSetting(addon_handle, id=SETTING_REQ_TOK, value=req_tok)  # TODO why does it not save the setting?
    xbmcgui.Dialog().ok(__addonname__, 'Call https://www.themoviedb.org/authenticate/ ' + req_tok
                        + ' from your browser and validate the token and add it in the settings')

req_token = xbmcplugin.getSetting(addon_handle, SETTING_REQ_TOK)
session_id = get_session_id(req_token)

# following from example:
url = 'http://localhost/some_video.mkv'
li = xbmcgui.ListItem(session_id, iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
