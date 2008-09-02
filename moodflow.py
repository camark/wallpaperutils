#!/usr/bin/env python
#coding=utf-8

''' Python program for download great wallpapers'''
import urllib2
import urllib
import HTMLParser
import os
import time
import sys

class Beijing(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.image_url=[]
        
    def handle_starttag(self,tag,attrs):
        #print tag
        if tag=='a':
            for name,value in attrs:
                if name=='href':
                    #print value
                    if value.endswith('jpg'):
                        self.image_url.append(value)

def getDownloadDir():
    if sys.platform=='win32':
        download_dir='c:/temp';
    else:
        download_dir=os.environ['HOME']+'/NationPhoto'
    
    download_dir=download_dir+'/'+time.strftime('%Y-%m-%d')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    return download_dir

def DownPic(homeurl,images_url):
    html=urllib2.urlopen(images_url).read()
    bj=Beijing()
    bj.feed(html)
    
    for img in bj.image_url:
        print 'Download %s' % (img)
        image_name=img.split('/')[-1]
        urllib.urlretrieve(homeurl+img,getDownloadDir()+'/'+image_name)
    
    
moodflow_url='http://www.moodflow.com/'
moodflow_images_url='http://www.moodflow.com/Wallpapers.html'

socksoff_images_url='http://www.socksoff.co.uk/walls01.html'
socksoff_url='http://www.socksoff.co.uk/'

def main():
    DownPic(socksoff_url,socksoff_images_url)
    DownPic(moodflow_url,moodflow_images_url)
    
    
if __name__=='__main__':
    main()

