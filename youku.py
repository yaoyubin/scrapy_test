#!/usr/bin/python

#coding="utf-8"
import re
import urllib2
import threading
import Queue
class youku(threading.Thread):

    def __init__(self,baseUrl,youkuQueue):
        threading.Thread.__init__(self)
        self.baseUrl=baseUrl if self.hasHttp().match(baseUrl) else 'http://'+baseUrl
        self.youkuQueue=youkuQueue
        self.vshow=self.youku_v_show()
        self.showpage=self.youku_show_page()
        self.start()
    
    def hasHttp(self):
        return re.compile("^http://")
    
    def youku_v_show(self):
        return re.compile(r'http://v\.youku\.com/v_show/id_.+\.html')
    
    def youku_show_page(self):
        return re.compile(r'http://www\.youku\.com/show_page/id_.+\.html')
    
    def parseUrl(self):
        req=urllib2.urlopen(self.baseUrl)
        contet=req.read()
        
        
        if self.vshow.match(self.baseUrl):
            return set(self.vshow.findall(contet))
        else:
            return set(self.showpage.findall(contet))
            
    def run(self):
        print ("start parse Youku ")
        matches=self.parseUrl()
        print (matches)
        for matche in matches:
            print ('matches:%s'%matche)
            self.youkuQueue.put(matche)
"""
if __name__=='__main__':
    Base_Url="http://www.youku.com/show_page/id_z70902150919c11e0a046.html"
    #Base_Url="http://tv.youku.com/search/"
    #Base_Url="http://v.youku.com/v_show/id_XNDkyODUyMTQ0.html"
    #Base_Url="http://www.baidu.com"
    youkuQueue=Queue.Queue()
    youku=youku(Base_Url,youkuQueue)
"""


