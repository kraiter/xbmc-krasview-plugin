import xbmc
import xbmcaddon
import xbmcplugin
import urllib
import urllib2

ADDON_ID = 'plugin.video.krasview'

settings = xbmcaddon.Addon(id=ADDON_ID)
language = settings.getLocalizedString
userpath = xbmc.translatePath(settings.getAddonInfo("profile"))
import CommonFunctions as common
import KrasViewCore as core
import KrasViewScrapper
import KrasViewUI as ui

scrapper = KrasViewScrapper.KrasViewScrapper()

params = core.get_params()
mode = None
url = None
page = 1

try:
    mode = params["mode"]
except:
    pass

try:
    page = int(params["page"])
except:
    pass

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass

if mode is None or mode == 'main':
    ui.buildMainMenu()

elif mode == 'video':
    ui.buildMainVideoMenu()
elif mode == 'list_video':
    videoList = None
    if url == 'new_video':
        videoList = scrapper.getVideoNew(page)
    if url == 'view_video':
        videoList = scrapper.getVideoView(page)
    if url == 'rate_video':
        videoList = scrapper.getVideoRate(page)
    if url == 'comm_video':
        videoList = scrapper.getVideoComm(page)
    if url == 'viewed_video':
        videoList = scrapper.getVideoViewed(page)
    if videoList is not None:
        ui.buildVideoList(videoList, url, page, mode)
    else:
        ui.buildMainVideoMenu()

elif mode == 'list_other_video':
    videoList = None
    videoList = scrapper.getVideo(url, page)
    if videoList is not None:
        ui.buildVideoList(videoList, url, page, mode)
    else:
        ui.buildMainMenu()

elif mode == 'channel' or mode == 'series' or mode == 'movie' or mode == 'anime':
    ui.buildMainOtherMenu(mode)

elif mode == 'list_tag':
    type = url.split('_')
    catList =  scrapper.getCatTag(page, type[0], type[1])
    if catList is not None:
        ui.buildTagGallery(catList, url, page)
    else:
        ui.buildTagListMenu(catList, type[0])

elif mode == 'list_cat':
    type = url.split('_')
    catList = None
    if type[0] == 'new' or type[0] == 'popular' or type[0] == 'best':
        catList = scrapper.getCatGallery(page, type[0], type[1])
        if catList is not None:
            ui.buildCatGallery(catList, url, page)
        else:
            ui.buildMainOtherMenu(type[1])
    elif type[0] == 'tag':
        catList = scrapper.getTagsList(type[1]);
        if catList is not None:
            ui.buildTagListMenu(catList, type[1])
        else:
            ui.buildMainOtherMenu(type[1])
    else:
        ui.buildMainOtherMenu(type[1])

elif mode == 'watch':
    try:
        url = urllib.unquote_plus(params["url"])
    except:
        ui.alert('error', 'no link given')
    core.watchVideo(url)