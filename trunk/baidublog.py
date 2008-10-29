#!/usr/bin/python
# -*- coding: cp936 -*-

import urllib2
import httplib
import cookielib
import urllib

class BaiduBlog:
    def __init__(self):
        cookie = cookielib.CookieJar()
        self.httpcookie = urllib2.HTTPCookieProcessor(cookie)


    def login(self,username,password):
        url='http://passport.baidu.com/?login'
        postdata= urllib.urlencode(
            {
                'username':username,
                'password':password
                }
            )
        request = urllib2.Request(url,postdata)
        opener = urllib2.build_opener(request,self.httpcookie)
        opener.open(request)

    def publishBlog(self,blogName,blog_title,blog_text,blog_catname='默认分类',isAllowCommit=1,isPublished=0):
        if len(blog_title)>100 or len(blog_text)>40000:
            print 'Blog Tilte must less than 100,and Blog Text must less 40000'
            return
        
        url = 'http://hi.baidu.com/%s/commit' % (blogName)
        postdata = urllib.urlencode(
            {
                'ct':1,
                'cm':1,
                'spBlogText':blog_text,
                'spBlogTitle':blog_title,
                'spBlogCatName':blog_catname,
                'spIsCmtAllow':isAllowCommit,
                'spBlogPower':isPublished,
                'tj':' 发表文章 '
                }
            )
        request=urllib2.Request(url,postdata)
        opener = urllib2.build_opener(request,self.httpcookie)
        opener.open(request)

        
    
if __name__=='__main__':
    bb = BaiduBlog()
    username = 'xxx'
    password = 'xxx'
    blogname = 'xxx'
    bb.login(username,password)
    bb.publishBlog(blogname,'hello','test','python')
    
