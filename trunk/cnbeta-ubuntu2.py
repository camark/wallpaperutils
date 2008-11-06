#!/usr/bin/env python
#coding=cp936

import urllib2
import os
import baidublog

article_id = 69031
url = 'http://www.cnbeta.com/articles/%d.htm' % (article_id)
url_obj = urllib2.urlopen(url)

if url_obj.code == 200:
    url_data = url_obj.read()
    
    
#print url_data

lines=url_data.split(os.linesep)

i =0 

title = ''
title_h_tag = '<h3 id="news_title">'
title_content_tag = '<div id="news_content">'
title_digbox = '<div class="digbox">'
in_content = False
contents = []
for l in lines:
    real_text = l.strip()
    #print "%d" % (i),l.strip()
    i = i+1
    
    if real_text.startswith( title_h_tag ):
        title = real_text[len(title_h_tag):-len('</h3>')]
        
    if in_content:
        contents.append(real_text)
        
    if real_text.startswith(title_content_tag):
        in_content = True
        
    if real_text.startswith(title_digbox):
        in_content = False
        

print title

news_title = title

openoffice_logo = 'http://hiphotos.baidu.com/camark/pic/item/c756a43e9ff6a7e1838b1309.jpg'
ubuntu_logo = 'http://hiphotos.baidu.com/camark/pic/item/034a49dadb15aac0b7fd48ec.jpg'
fedora_logo = 'http://hiphotos.baidu.com/camark/pic/item/9575e3eddf89975479f055f3.jpg'
fullcirlce_logo = 'http://hiphotos.baidu.com/camark/pic/item/1799673e8130222670cf6c80.jpg'

pic_log = fullcirlce_logo
blog_content = '<img src="%s" align="right">' % (pic_log)
for c in contents[:-1]:
    if not c.find('感谢')<>-1:
        print c
        blog_content = blog_content + c
        

bb = baidublog.BaiduBlog()
username = 'superwar3fan'
password = 'blizzard'
blogname = 'camark'
bb.login(username,password)
bb.publishBlog(blogname,news_title,blog_content,'ubuntu/debian')
