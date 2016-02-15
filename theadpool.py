#!/usr/bin/python

#coding="utf-8"
import re
import urllib2
from youku import youku
from flcvd import flcvd
from Queue import Queue


class theadpool:

    def __init__(self,form,downloadList,youkuQueue,worknum):
        self.form=form
        self.downloadList=downloadList
        self.youkuQueue=youkuQueue
        self.works=[]
        self.worknum=worknum
        self.initflcvd()
    
    def initflcvd(self):
        for i in range(self.worknum):
            self.works.append(flcvd(i ,self.form,self.downloadList,self.youkuQueue))
            
    def finish(self):
        for work in self.works:
            if work.isAlive():
                work.join()            
        

def thunder(downloadList):
    thunderListFile=open('downloadlist.lst','w+')
    downloadList=set(downloadList)
    for download in downloadList:
        thunderListFile.write('%s\n'%download);
    thunderListFile.close()


if __name__=='__main__':
    downloadList=[]
    youkuQueue=Queue()
    worknum=4
    Base_Url="http://v.youku.com/v_show/id_XNDkyODUyMTQ0.html"
    #Base_Url="http://www.youku.com/show_page/id_z70902150919c11e0a046.html"
    
    
    youku(Base_Url,youkuQueue)
    
    theadpools=theadpool('super',downloadList,youkuQueue,worknum)
    theadpools.finish()
    
    thunder(downloadList)

