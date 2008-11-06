#!/usr/bin/env python
#coding=utf-8

from BeautifulSoup import *
import urllib2
import urllib
import sys
import time
import os

def getDownloadDir():
    if sys.platform=='win32':
        download_dir='c:/temp';
    else:
        download_dir=os.environ['HOME']+'/NationPhoto'
    
    download_dir=download_dir+'/'+time.strftime('%Y-%m-%d')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    return download_dir

url='http://www.trmusic.com.cn/blog/user1/198/archives/2006/897.asp'

url_obj = urllib2.urlopen(url)

start_url = 'http://image2.sina.com.cn/dongman/'

def DownImgFromUrl(url):
    img_src = url['src']
    image_name = img_src.split('/')[-1]
    urllib.urlretrieve(img_src,getDownloadDir()+'/'+image_name)
    
if url_obj.code == 200:
    url_data = url_obj.read()
    
    bs=BeautifulSoup(''.join(url_data))
    #print bs.prettify()
#    for img in bs.findAll('img'):
#        print img['src']
#        image_path = img['src']
#        
#        if image_path.startswith(start_url):
#            image_name = image_path.split('/')[-1]
#            urllib.urlretrieve(image_path,getDownloadDir()+'/'+image_name)
    
    map(DownImgFromUrl,[m for m in bs.findAll('img') if m['src'].startswith(start_url)])
                
print 1