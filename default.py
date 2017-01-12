import sys
import json
import urllib2
import xbmc
import xbmcgui
import xbmcplugin


def get_key_path():
    root_path = xbmc.translatePath('special://home')
    if xbmc.getCondVisibility('system.platform.windows'):
        return root_path + 'addons\\plugin.video.kodi_watchlist\\key.txt'
    if xbmc.getCondVisibility('system.platform.linux'):
        return root_path + 'addons/plugin.video.kodi_watchlist/key.txt'  # TODO linux support is untested


addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

apiKey = open(get_key_path()).read()


def get_api_root():
    return 'https://api.themoviedb.org/3/'


def add_api_key():
    return '?api_key=' + apiKey


def build_api_url(resource):
    return get_api_root() + resource + add_api_key()


def get_authentification_token():
    token_URL = build_api_url('authentication/token/new')
    http_response = urllib2.urlopen(token_URL)
    json_response = http_response.read().decode('utf-8')
    response = json.loads(json_response)
    return response['request_token']


user = xbmcplugin.getSetting(addon_handle, 'username')
password = xbmcplugin.getSetting(addon_handle, 'password')


# following from example:
url = 'http://localhost/some_video.mkv'
li = xbmcgui.ListItem(get_authentification_token(), iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
