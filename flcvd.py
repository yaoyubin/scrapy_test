#!/usr/bin/python

#coding="utf-8"
import re
import urllib
import urllib2
import threading
import Queue

class flcvd(threading.Thread):
    Bae_Url="http://www.flvcd.com/parse.php?"
    def __init__(self,worknum,form,downloadList,youkuQueue):
        threading.Thread.__init__(self)
        #self.url=youkuUrl
        self.showpage=self.hidentFileUrl()
        self.vshow=self.youku_v_show()
        self.herfshow=self.herfFileUrl()
        self.form=form
        self.downloadList=downloadList
        self.youkuQueue=youkuQueue
        self.worknum=worknum
        self.start()
    
    def hidentFileUrl(self):
        return re.compile('(http://f.youku.com/player/getFlvPath.+\s?)')

    def herfFileUrl(self):
        return re.compile(r'<a href=\"(http://f.youku.com/player/getFlvPath[^\"]+)')    
        
    def youku_v_show(self):
        return re.compile(r'http://v\.youku\.com/v_show/id_.+\.html')        
        
    def headers(self,url):
        heads={
            'Host':'www.flvcd.com',
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 '
        }        
        return heads
    
    def compileUrl(self,youkuUrl):
        params={'kw':youkuUrl}
        encode=urllib.urlencode(params)
        form="&format=%s"%(self.form if self.form  else '')
        realUrl="%s%s%s"%(self.Bae_Url,encode,form)
        return realUrl
    
    def parseUrl(self,youkuUrl):
        targetUrl=self.compileUrl(youkuUrl)
        req=urllib2.Request(
            url =targetUrl,
            headers = self.headers(targetUrl)
        )
        resp=urllib2.urlopen(req)
        content=resp.read()
        if self.vshow.match(youkuUrl):
            return self.herfshow.findall(content)
        else:
            return self.showpage.findall(content)

    
    def run(self):
        while True:
            youkuUrl=self.youkuQueue.get()
            print '[No:%d] flvcd robot youku url>>%s'%(self.worknum,youkuUrl)
            matches=self.parseUrl(youkuUrl)
            #print matches
            for item in matches:
                #print item
                self.downloadList.append(item.rstrip())
                
            if self.youkuQueue.empty():
                print '[No:%d] flcvd no work ,bye bye...'%self.worknum
                break
        
        
"""   """   
if __name__=='__main__':
    youkuQueue=Queue.Queue()
    youkuQueue.put('http://v.youku.com/v_show/id_XNDkzNTk2NDQw.html')
    #youkuQueue.put('http://www.youku.com/show_page/id_z70902150919c11e0a046.html')
    downloadList=[]
    flcvd=flcvd(1,'super',downloadList,youkuQueue)
    
