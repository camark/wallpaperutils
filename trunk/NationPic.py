#!/usr/bin/python
from urllib import urlopen
import HTMLParser
import re
import os
import time

nations ='http://photography.nationalgeographic.com'
today ='/photography/photo-of-the-day/archive'
turl = 'http://photography.nationalgeographic.com/photography/photo-of-the-day'
todayurl = nations + today
wallpaper_path = '/photography/wallpaper'
wallpaper_static_path = '/staticfiles/NGS/Shared/StaticFiles/Photography/Images/POD'

class NationParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.pages=[]
        #print 'hi'

    def handle_starttag(self,tag,attrs):
        try:
            if tag=='a':
                for name,value in attrs:                
                    if name=='href':
                        imagename=self.isImagePath2(value)
                        if imagename and not (self.pages.count(imagename)):
                            #print value
                            self.pages.append(imagename)
                            
        except HTMLParser.HTMLParser:
            pass
    
    def isImagePath(self,url):
        ip='/photography/enlarge/enlarge/((\w+-?)+).html'
        regx=re.compile(ip)

        re_result=regx.match(url)
        if re_result:
            print 'Match'
            print url
            
        return re_result

    def isImagePath2(self,url):
        
        a=url.split('/')
##        print str(len(a))
##        for i in a:
##            print i
        if a[1]=='photography' and a[2]=='wallpaper':
            #print 'find %s' % (a[3][0:-len('.html')])
            return a[3][0:-len('.html')]
        else:
            return None
    

def isImageRealPath(url):
    ip=wallpaper_static_path+'/(\w+)/((\w+-?)+).jpg'

    regx=re.compile(ip)
    re_result=regx.findall(url)

    if re_result:
        return re_result
    else:
        return None
    
def isImagePath(url):
    ip='/photography/wallpaper/((\w+-?)+).html'
    ip1='<a class="wallpaper" href="/photography/wallpaper/boat-race-boyer_pod_image.html">Wallpaper</a>'
    regx=re.compile(ip)
    re_result=regx.findall(url)

    if re_result:
#        print 'content:'
        np = NationParser()
        np.feed(url)

        for i in np.pages:
##            print i
            url=nations+wallpaper_path+'/'+i+'.html'
#            print url
            a1=urlopen(url).read()
            lines=a1.split(os.linesep)
            downloads=[]
            for l in lines:
#                print 'line %s' % (l)
                a=isImageRealPath(l)
                if a:
                    for (key,filename,other) in a:
                        if other in ['sw','lw','xl'] and not (filename in downloads):
                            filename_url=nations+wallpaper_static_path+'/'+key+'/'+filename+'.jpg'
                            downloads.append(filename_url)
                            image_data=urlopen(filename_url).read()
#                            print filename
                            dirname=os.environ['HOME']+'/NationPhoto'
                            if not os.path.exists(dirname):
                                os.mkdir(dirname)
                            dirname=dirname+'/'+time.strftime('%Y-%m-%d')
                            if not os.path.exists(dirname):
                                os.mkdir(dirname)
                            savefilename=dirname+'/'+filename+'.jpg'
                            if not os.path.exists(savefilename):
                                f=open(savefilename,'wb')
                                f.write(image_data)
                                f.close()
        #print url

    return re_result

html=urlopen(turl).read()
#np = NationParser()
lines=[]
lines=html.split(os.linesep)
for l in lines:
    #print l
    isImagePath(l[0:-len(os.linesep)])
    #pass

#print 'Walk complete'
#np.feed(html)

