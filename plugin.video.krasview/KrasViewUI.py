import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib

language = sys.modules["__main__"].language


def alert(title, text, secs=5000):
    xbmc.executebuiltin('Notification(' + title + ',' + text + ',' + str(secs) + ')')


def addDir(name, url, mode, iconimage, page=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + mode
    if page != None:
        u += '&page=' + str(page)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    # liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def addVideoItem(name, url, thumbnail):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=watch"
    li = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=False)

def addCatItem(name, url, thumbnail):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=list_other_video"
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=li, isFolder=True)


#main menu
def buildMainMenu():
    addDir(language(30030), 'video', 'video', '')
    addDir(language(30031), 'channel', 'channel', '')
    addDir(language(30032), 'series', 'series', '')
    addDir(language(30033), 'movie', 'movie', '')
    addDir(language(30034), 'anime', 'anime', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#main video menu
def buildMainVideoMenu():
    addDir(language(30001), 'new_video', 'list_video', '')
    addDir(language(30002), 'view_video', 'list_video', '')
    addDir(language(30003), 'rate_video', 'list_video', '')
    addDir(language(30004), 'comm_video', 'list_video', '')
    addDir(language(30005), 'viewed_video', 'list_video', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#main video menu
def buildMainOtherMenu(type):
    addDir(language(30020), 'new_' + type, 'list_cat', '')
    addDir(language(30021), 'popular_' + type, 'list_cat', '')
    addDir(language(30022), 'best_' + type, 'list_cat', '')
    addDir(language(30023), 'tag_' + type, 'list_cat', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#cat list
def buildCatGallery(arr, url, page):
    addon_handle = int(sys.argv[1])
    xbmcplugin.setContent(addon_handle, 'albums')
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')  # "Thumbnail" view

    for video in arr:
        link = video['link']
        caption = video['name']
        thumbnail = video['thumbnail']
        addCatItem(caption, link, thumbnail)

    addDir(language(30006), url, 'list_cat', '', page + 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#cat list
def buildTagGallery(arr, url, page):
    addon_handle = int(sys.argv[1])
    xbmcplugin.setContent(addon_handle, 'albums')
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')  # "Thumbnail" view

    for video in arr:
        link = video['link']
        caption = video['name']
        thumbnail = video['thumbnail']
        addCatItem(caption, link, thumbnail)

    addDir(language(30006), url, 'list_tag', '', page + 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#tag list menu
def buildTagListMenu(arr, type):
    for tag in arr:
        addDir(tag["name"], type + "_" + tag["name"] , 'list_tag', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def buildVideoList(arr, url, page, mode):
    addon_handle = int(sys.argv[1])
    xbmcplugin.setContent(addon_handle, 'movies')
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.confluence':
        xbmc.executebuiltin('Container.SetViewMode(500)')  # "Thumbnail" view
    for video in arr:
        link = video['link']
        caption = video['name']
        thumbnail = video['thumbnail']
        addVideoItem(caption, link, thumbnail)
    addDir(language(30006), url, mode, '', page + 1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def playVideo(video):
    if video['link'] != "":
        li = xbmcgui.ListItem(video['name'], iconImage=video['icon'], thumbnailImage=video['thumbnail'])
        li.setInfo('video', {'Title': video['name']})
        xbmc.Player().play(video['link'], li, False)
    else:
        alert('error', 'video link not specified')