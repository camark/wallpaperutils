#!/usr/bin/env python

import wordpresslib
import MSBlogAPI
import xmlrpclib
import HTMLParser
from urllib import urlopen
import re
import os
import sys
import time
import Image


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
        regpat='http://www.iheartchaos.com/(\d{4})/(\d{2})/(\d{2})/((\w+-?)+)/'
        regx=re.compile(regpat)

        re_result=regx.match(str)
	
	
	
        if re_result:
            return True
        else:
            return False

class PicParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        #self.download=PicDownload()
        self.imageurls=[]
	self.images=VisitRecord(filename=os.environ['HOME']+'/temp/image_published.dat')

    def handle_starttag(self,tag,attrs):
        if tag=='img':
            for name,value in attrs:
                if name=='src':
                    #print value
                    if self.isDownload(value) and not self.images.isVisited(value):
                        self.imageurls.append(value)
                        #print value

    def isDownload(self,imgurl):
        regpat='http://www.iheartchaos.com/wp-content/uploads/(\d{4})/(\d{2})/((\w+-?)+).jpg'
        regx=re.compile(regpat)

        re_result=regx.match(imgurl)
        
        if re_result:
            return True
        else:
            return False

    def generateBlog(self):
        html=''
        image_width=400
        image_height=300
	if len(self.imageurls):
		#html=html+'<ul>'
	        for url in self.imageurls:
        	    html=html+'<img src=%s align=center/><br/>' % (url)
		#html=html+'</ul>'
		self.images.writecfg()
        return html

    def publishtoblog(self):
        today=time.strftime('%Y-%m-%d')
        desp=self.generateBlog()
        #print desp
        if len(desp):
            title='Girls of IheartChaos of %s'  % (today)
            mb=MSBlogAPI.MsMetaBlogAPI('MyBlog','user','password')
            ms_Post=MSBlogAPI.NewPost()
            ms_Post.title=title
            ms_Post.description=desp
            ms_Post.categories=['girl of iheartchaos']
            bt=xmlrpclib.Boolean(True)
            rv=mb.newPost(ms_Post,bt)
        #print 'Success send to LiveSpace,PostID:',rv
	


class VisitRecord:
    def __init__(self,filename='/home/xx/temp/blog-published.dat'):
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
for url in ichaos.urls:
    if not vr.isVisited(url):
        pp=PicParser()
	a=urlopen(url).read()
#print a
        pp.feed(a)
        pp.publishtoblog()

vr.writecfg()






