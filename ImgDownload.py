#!/usr/bin/env python
#coding=utf-8

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
                        
        if tag == 'img':
            for name,value in attrs:
                if name == 'src':                    
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

def IsValidFileName(str):
        if str.find('?') <> -1:
            return False
        if str.find('&') <> -1:
            return False
        
        if str.find('.') <> -1:
            return False
        
        return True



def DownloadUrl(url):
    html_data=urllib2.urlopen(url).read()
    bj=Beijing()
    bj.feed(html_data)
    
    image_index = 1
    for img in bj.image_url:
        image_name=img.split('/')[-1]
        print image_name
        
        if IsValidFileName(image_name):
            urllib.urlretrieve(img,getDownloadDir()+'/'+image_name)
        else:
            urllib.urlretrieve(img,getDownloadDir()+'./'+('%d_img.jpg' % (image_index)))
            image_index = image_index+1
        
        
#DownloadUrl('http://www.smashingapps.com/2008/09/19/21-extremely-vibrant-and-creative-advertisements-with-animals.html')
#DownloadUrl('http://www.hongkiat.com/blog/100-absolutely-beautiful-nature-wallpapers-for-your-desktop/')
#DownloadUrl('http://www.hongkiat.com/blog/70-beautiful-dual-monitors-desktop-wallpapers/')
if __name__=='__main__':
    DownloadUrl('http://www.trmusic.com.cn/blog/user1/198/archives/2006/897.asp')