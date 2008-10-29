#!/usr/bin/env python
#coding=cp936

import urllib2
import HTMLParser
import baidublog
import urllib

class cnbeta_spider(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.in_title = False
        self.in_content = False
        self.is_ubuntu_news = False
        self.news_title = ''
        self.news_content = []
        
    def handle_starttag(self,tag,tag_data):
        if tag == 'title':
            self.in_title = True   
            
        if tag == 'div':
            for name,value in tag_data:
                if name == 'id' and value == 'news_content':
                    self.in_content = True                
                if name == 'class' and value == 'digbox':
                    self.in_content = False       
        #print tag,tag_data
        
    def handle_data(self,data):
        if self.in_title:
            #print data
            
            news = 'cnBeta.COM_Ubuntu_'
            if data.startswith( news ):
                self.is_ubuntu_news = True
                self.news_title = '[Ubuntu News]' + data[len(news):]
                
            self.in_title = False
            
        if self.in_content:
            #print data
            self.news_content.append( '<p>' + data + '</p>' )
            #self.in_content = False

article_id = 68318
url = 'http://www.cnbeta.com/articles/%d.htm' % (article_id)

url_data = urllib2.urlopen(url).read()
#print url_data
url_data=url_data.replace('<strong>','')
url_data=url_data.replace('</strong>','')
#url_data =  urllib.quote_plus(url_data)
url_data = url_data.replace('&rdquo;','')
url_data = url_data.replace('&ldquo;','')
url_data = url_data.replace('&rsquo;','')

cs = cnbeta_spider()
cs.feed(url_data)

print cs.news_title
blog_content = '<img src="http://hiphotos.baidu.com/camark/pic/item/034a49dadb15aac0b7fd48ec.jpg" align=right>'

i=0
count = len( cs.news_content) -1 
contents = []

#if cs.news_content[5] == '<p>的投递</p>':
#    cs.news_content = cs.news_content[5:]
        
for con in cs.news_content:
    print con
    blog_content = blog_content + con
    
bb = baidublog.BaiduBlog()
username = 'xxxx'
password = 'xxxx'
blogname = 'xxxx'
bb.login(username,password)
bb.publishBlog(blogname,cs.news_title,blog_content,'ubuntu/debian')
