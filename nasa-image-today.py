#!/usr/bin/python
#coding=utf-8

__version__='0.1'
__description__='''Download pictrue of NASA today need feedparser'''

import urllib2
import feedparser
import urllib
import time
import os
import sys
import HTMLParser

class Beijing(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.image_url=''
        
    def handle_starttag(self,tag,attrs):
        #print tag
        if tag=='a':
            for name,value in attrs:
                if name=='href':
                    #print value
                    if value.endswith('jpg'):
                        self.image_url=value

def getDownloadDir():
    if sys.platform=='win32':
        download_dir='c:/temp';
    else:
        download_dir=os.environ['HOME']+'/NationPhoto'
    
    download_dir=download_dir+'/sky'

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    return download_dir


def getToday():
    return time.strftime('%Y-%m-%d')

'''Download NASA pic'''
def getNASAToday():
    today=getToday()
    url = 'http://www.nasa.gov/rss/image_of_the_day.rss'
    
    download_dir=getDownloadDir()        
    rss=feedparser.parse(url)

    #image_url=rss.feed.image['url']
    image_url=rss['entries'][0]['guid']
    #print image_url
    
    data=urllib2.urlopen(image_url).read()
    bp=Beijing()
    bp.feed(data)
    nasa_url='http://www.nasa.gov'
    download_image_url=nasa_url+bp.image_url
    urllib.urlretrieve(download_image_url,download_dir+'/NASA-'+today+'.jpg')

def getBeijingTianWenToday():
    bp=Beijing()
    data=urllib.urlopen('http://www.bjp.org.cn/apod/today.htm').read()
    
    lines=data.split("\n")
    rs=[]
    for line in lines:
        line=line.strip()
        if not line.startswith('<!['):
            rs.append(line)
            
    data="\n".join(rs)
    #print data
    
    bp.feed(data)
    
    #print bp.image_url
    urllib.urlretrieve(bp.image_url,getDownloadDir()+'/Beijing-TianWen-'+getToday()+'.jpg')
    
if __name__=='__main__':
    getNASAToday()
    getBeijingTianWenToday()
