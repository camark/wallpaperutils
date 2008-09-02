#!/usr/bin/python
#coding=utf-8

import time
import urllib2
import urllib
import os


today=time.strftime('%y/%m/%d')
today_another=time.strftime('%Y-%m-%d')
#print today

deskcity_url='http://www.deskcity.com/daily/index'
deskcity_home='http://www.deskcity.com'
url_today=deskcity_url

urldata=urllib2.urlopen(url_today).read()

lines=urldata.split("\n")
temp_str="<li><a href='/daily/show/"

urls=[]
for line in lines:
    line=line.strip()
    if line.startswith(temp_str):
       urls.append(line)

def isDownload(str):
	download_sizes=['1280x1024']
	for i in download_sizes:
		if str.find(i)<>-1:
			return True

	return False    

download_dir=os.environ['HOME']+'/NationPhoto/'+today_another

if not os.path.exists(download_dir):
	os.makedirs(download_dir)

for url in urls:
    target_url=url[url.index("'")+1:url.index('target')-2]
    #print target_url
    
    if isDownload(url):
        print url
        url_data=urllib2.urlopen(deskcity_home+target_url).read()
        
        lines=url_data.split("\n")

        temp_str='<div class="it" id="simg">'

        for line in lines:
            line=line.strip()
            if line.startswith(temp_str):
                #line=line.strip()
                find_line=line[len(temp_str)+1:]
                
        print find_line

        pos=find_line.index('src=')
        image_url=find_line[pos+len('src="'):-len(' /></div>')-1]
        print deskcity_home+image_url
        urllib.urlretrieve(deskcity_home+image_url,download_dir+'/'+today_another+'.jpg')
    
    
