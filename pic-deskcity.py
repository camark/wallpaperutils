#!/usr/bin/env python
#coding=utf-8

import urllib2
import urllib
i=145
j=2335
while i<j:
    url='http://www.deskcity.com/daily/show/'+str(i)
    deskcity='http://www.deskcity.com'

    url_data=urllib2.urlopen(url).read()

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
    print image_url
    urllib.urlretrieve(deskcity+image_url,'c:/temp/'+str(i)+'.jpg')
    i=i+10
