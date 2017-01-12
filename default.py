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

key = open(get_key_path()).read()

# following from example:
url = 'http://localhost/some_video.mkv'
li = xbmcgui.ListItem(key, iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)
