import sys
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
user = xbmcplugin.getSetting(addon_handle, 'username')
password = xbmcplugin.getSetting(addon_handle, 'password')

# following from example:
url = 'http://localhost/some_video.mkv'
li = xbmcgui.ListItem(user, iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
