import sys
import re
import simplejson as json

BASE_URI = 'http://krasview.ru'
NEW_VIDEO_PATH = '/video/new'
POPULAR_VIDEO_PATH = '/video/view'
BEST_VIDEO_PATH = '/video/rate'
COMMENTED_VIDEO_PATH = '/video/comm'
WATCHED_VIDEO_PATH = '/video/viewed'

NEW_PATH = '/fresh'
POPULAR_PATH = ''
BEST_PATH = '/top'
TAGS_PATH = '/tag'

class KrasViewScrapper:
    def __init__(self):
        self.common = sys.modules["__main__"].common
        self.core = sys.modules["__main__"].core

    #video
    def getVideoNew(self, page):
        return self._getVideoGallery(NEW_VIDEO_PATH, page)
    def getVideoView(self, page):
        return self._getVideoGallery(POPULAR_VIDEO_PATH, page)
    def getVideoRate(self, page):
        return self._getVideoGallery(BEST_VIDEO_PATH, page)
    def getVideoComm(self, page):
        return self._getVideoGallery(COMMENTED_VIDEO_PATH, page)
    def getVideoViewed(self, page):
        return self._getVideoGallery(WATCHED_VIDEO_PATH, page)

    def getVideo(self, url, page):
        return self._getVideo(url, page)

    def getPath(self, type, mode):
        prefix = ''
        if type == 'new':
            prefix = NEW_PATH
        elif type == 'popular':
            prefix = POPULAR_PATH
        elif type == 'best':
            prefix = BEST_PATH
        elif type == 'tag':
            prefix = TAGS_PATH
        return '/' + mode + prefix

    def getCatTag(self, page, type, mode):
        return self._getCatTag(page, type, mode)

    def getCatGallery(self, page, type, mode):
        return self._getCatGallery(page, type, mode)

    def getTagsList(self, type):
        return self._getTagsList(type)

    #tags list
    def _getTagsList(self, type):
        params = {}
        params['link'] = BASE_URI + '/' + type
        params['method'] = 'GET'
        ret = self.core._fetchPage(params)
        gallery = self.common.parseDOM(ret["content"], "div", attrs={"class": "tags"})
        ret = []
        if (len(gallery) > 0):
            for k in gallery:
                ret.extend(self._parseTag(k))
        return ret

    #cat list
    def _getCatTag(self, page=None, type=None, tag=None):
        params = {}
        params['link'] = BASE_URI + '/' + type + TAGS_PATH + '/' + tag
        if page != None:
            params['link'] += '?page=' + str(page)
        params['method'] = 'GET'
        ret = self.core._fetchPage(params)

        gallery = self.common.parseDOM(ret["content"], "ul", attrs={"class": "channel-gallery"})
        ret = []
        if (len(gallery) > 0):
            for k in gallery:
                ret.extend(self._parseCat(k))
        return ret

    #cat list
    def _getCatGallery(self, page=None, type=None, mode=None):
        params = {}
        params['link'] = BASE_URI + self.getPath(type, mode)
        if page != None:
            params['link'] += '?page=' + str(page)
        params['method'] = 'GET'
        ret = self.core._fetchPage(params)

        gallery = self.common.parseDOM(ret["content"], "ul", attrs={"class": "channel-gallery"})
        ret = []
        if (len(gallery) > 0):
            for k in gallery:
                ret.extend(self._parseCat(k))
        return ret


    def _getVideoGallery(self, path, page=None):
        params = {}
        params['link'] = BASE_URI + path
        if page != None:
            params['link'] += '?page=' + str(page)
        params['method'] = 'GET'
        ret = self.core._fetchPage(params)

        gallery = self.common.parseDOM(ret["content"], "ul", attrs={"class": "video-gallery"})
        ret = []
        if (len(gallery) > 0):
            for k in gallery:
                ret.extend(self._parseGallery(k))
        return ret

    def _getVideo(self, path, page=None):
        params = {}
        params['link'] = BASE_URI + path + '?category=-1'
        if page != None:
            params['link'] += '&page=' + str(page)
        params['method'] = 'GET'
        ret = self.core._fetchPage(params)

        gallery = self.common.parseDOM(ret["content"], "ul", attrs={"class": "video-gallery"})
        ret = []
        if (len(gallery) > 0):
            for k in gallery:
                ret.extend(self._parseGallery(k))
        return ret

    def _parseTag(self, html):
        ret_arr = []
        items = self.common.parseDOM(html, "a")
        if len(items) > 0:
            for item in items:
                tag = {}
                tag['name'] = self.common.stripTags(item.encode('utf-8'))
                ret_arr.append(tag)
        return ret_arr

    def _parseCat(self, html):
        ret_arr = []
        items = self.common.parseDOM(html, "li")
        if (len(items) > 0):
            for item in items:
                videoDict = {}
                # get name of the video
                elem = self.common.parseDOM(item, "img", ret='alt')
                if len(elem) > 0:
                    videoDict['name'] = elem[0].encode('utf-8')
                else:
                    continue
                # get link for the video
                elem = self.common.parseDOM(item, "a", ret='href')
                videoDict['link'] = elem[0].encode('utf-8')
                #get image for the video
                elem = self.common.parseDOM(item, "img", ret='src')
                if len(elem) > 0:
                    videoDict['thumbnail'] = elem[0].encode('utf-8')
                else:
                    videoDict['thumbnail'] = ""  #TODO: set default png here!!!

                ret_arr.append(videoDict)
        return ret_arr

    def _parseGallery(self, html):
        ret_arr = []
        items = self.common.parseDOM(html, "li")
        p1 = re.compile(r'<div.*?</div>')
        p2 = re.compile(r'<.*?>')
        if (len(items) > 0):
            for item in items:
                videoDict = {}
                # get name of the video
                #elem = self.common.parseDOM(item, "a", attrs={'itemprop': 'name'}, ret='title')
                elem = self.common.parseDOM(item, "a")
                if len(elem) > 0:
                    videoDict['name'] = p2.sub('', p1.sub('', elem[0].encode('utf-8').replace('&quot;', '"')))
                else:
                    continue
                #get link for the video
                elem = self.common.parseDOM(item, "a", attrs={'itemprop': 'name'}, ret='href')
                videoDict['link'] = elem[0].encode('utf-8')
                #get image for the video
                elem = self.common.parseDOM(item, "img", ret='src')
                if len(elem) > 0:
                    videoDict['thumbnail'] = elem[0].encode('utf-8')
                else:
                    videoDict['thumbnail'] = ""  #TODO: set default png here!!!
                ret_arr.append(videoDict)
        return ret_arr

    def getVideoItem(self, url):
        params = {'link': BASE_URI + url, 'method': 'GET'}
        ret = self.core._fetchPage(params)
        if ret['status'] == 200:
            videoLink = self._getVideoLink(ret['content'])
            name = self.common.parseDOM(ret['content'], 'span', attrs={"itemprop": 'name'})
            if len(name) > 0:
                name = self.common.stripTags(name[0])
            else:
                name = 'unknown name'
            return {'name': name, 'link': videoLink, 'icon': '', 'thumbnail': ''}
        else:
            return None

    def _getVideoLink(self, html):
        videoContainer = self.common.parseDOM(html, "div", attrs={"id": "video-container"})
        if len(videoContainer) > 0:
            script = self.common.parseDOM(videoContainer[0], 'script')
            if len(script) > 0:
                m = re.search(r"flashvars:\s*({[^}]*})", script[0])
                flashVars = json.loads(m.group(1))
                retLink = flashVars['url']
        return retLink