import sys
import urllib2
import CommonFunctions as common
import xbmc

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

class url2request(urllib2.Request):
    def __init__(self, url, method="GET"):
        self._method = method
        urllib2.Request.__init__(self, url)
        self.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)

def _fetchPage(params={}):
    """
    Fetches given page content

    Arguments:
    params - dictionary:
        link - uri to fetch
        method (optional) - request method
    """

    get = params.get
    link = get('link','http://krasview.ru')
    request = url2request(link, get("method", "GET"))
    ret_obj = {"status": 500, "content": "", "error": 0}

    try:
        con = urllib2.urlopen(request)
        inputdata = con.read()
        ret_obj["content"] = inputdata.decode('cp1251').encode('utf8')
        ret_obj["location"] = link
        
        ret_obj["new_url"] = con.geturl()
        ret_obj["header"] = str(con.info())
        ret_obj['status'] = 200
        con.close()
        return ret_obj

    except urllib2.HTTPError, e:
        cont = False
        err = str(e)
        msg = e.read()

        self.common.log("HTTPError : " + err)
        if e.code == 400 or True:
            self.common.log("Unhandled HTTPError : [%s] %s " % (e.code, msg), 1)

        params["error"] = get("error", 0) + 1
        ret_obj = self._fetchPage(params)

        if cont and ret_obj["content"] == "":
            ret_obj["content"] = cont
            ret_obj["status"] = 303

        return ret_obj

    except urllib2.URLError, e:
        err = str(e)
        self.common.log("URLError : " + err)
        if err.find("SSL") > -1:
            ret_obj["status"] = 303
            ret_obj["content"] = sys.modules["__main__"].language(30629)
            ret_obj["error"] = 3  # Tell _findErrors that we have an error
            return ret_obj

        time.sleep(3)
        params["error"] = get("error", 0) + 1
        ret_obj = self._fetchPage(params)
        return ret_obj

    except socket.timeout:
        self.common.log("Socket timeout")
        return ret_obj

def watchVideo(url):
    scrapper = sys.modules["__main__"].scrapper
    ui = sys.modules["__main__"].ui
    video = scrapper.getVideoItem(url)
    #print repr(video)
    if video!=None:
        ui.playVideo(video)
    else:
        ui.alert('Error','Unable to get a link for the video')