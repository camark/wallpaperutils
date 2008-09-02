#!/usr/bin/python

import HTMLParser
from urllib import urlopen
import re
import os
import sys
import time

class IChaosParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.urls=[]

    def handle_starttag(self,tag,attrs):
        if tag=='a':
            for name,value in attrs:
                if name=='href':
                    if self.isUrl(value):
                        if self.urls.count(value)==0 and value.find('#')==-1:
                            self.urls.append(value)
                            #print value

    def isUrl(self,str):
        regpat='http://www.iheartchaos.com/(\d{4})/(\d{2})/(\d{2})/(\w+)'
        regx=re.compile(regpat)

        re_result=regx.match(str)
        if re_result:
            return True
        else:
            return False

class PicParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.download=PicDownload()

    def handle_starttag(self,tag,attrs):
        if tag=='img':
            for name,value in attrs:
                if name=='src':
                    #print value
                    if self.isDownload(value):
                        self.download.Download(value)
                        #print value

    def isDownload(self,imgurl):
        regpat='http://www.iheartchaos.com/wp-content/uploads/(\d{4})/(\d{2})/(\w+-?)*.jpg'
        regx=re.compile(regpat)

        re_result=regx.match(imgurl)
        if re_result:
            return True
        else:
            return False


class PicDownload:
    def __init__(self):
        pass

    def Download(self,imgurl):
        fileSaveDir=self.getSaveDir()
        fileName=imgurl.split('/')[-1]

        if not os.path.exists(fileSaveDir+'/'+fileName):
            socket=urlopen(imgurl)
            os.chdir(fileSaveDir)

            f=open(fileName,'wb')
            f.write(socket.read())
            f.close()

    def getSaveDir(self):
	#today=time.strftime('%Y-%m-%d')
        if sys.platform=='win32':
            def_save_path='c:/temp'            
        elif sys.platform=='linux2':
            def_save_path='/home/gm/temp'
	
        if not os.path.exists(def_save_path):
                os.mkdir(def_save_path)
	
	#if not os.path.exists(def_save_path+'/'+today):
		#os.mkdir(def_save_path+'/'+today)

        return def_save_path
            
class VisitRecord:
    def __init__(self,filename='/home/gm/temp/visitrecord.dat'):
        self.filename=filename
        self.visitedUrls=[]
        self.readcfg()
        

    def readcfg(self):
        if os.path.exists(self.filename):
            f=open(self.filename,'r')
            for line in f.readlines():
                if len(line):
                    self.visitedUrls.append(line[0:-len(os.linesep)])
            f.close()

    def writecfg(self):
        f=open(self.filename,'w')
        for vr in self.visitedUrls:
            f.write(vr+os.linesep)
        f.close()

    def isVisited(self,url):
        if self.visitedUrls.count(url)>0:
            return True
        else:
            self.visitedUrls.append(url)
            return False

    def printUrls(self):
	for url in self.visitedUrls:
		print url
        
        
    
a=urlopen('http://www.iheartchaos.com/category/girls-of-ihc/').read()
#print 'Waiting to Read'
#print a

ichaos=IChaosParser()
ichaos.feed(a)

vr=VisitRecord()
#vr.printUrls()
pp=PicParser()
for url in ichaos.urls:    
    if not vr.isVisited(url):
	#print url
        vr.writecfg()
        a=urlopen(url).read()
#print a
        pp.feed(a)

#vr.writecfg()



