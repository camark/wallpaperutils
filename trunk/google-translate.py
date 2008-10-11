#!/usr/bin/python
import urllib2
import urllib
import HTMLParser
import sgmllib

class TranstParser(sgmllib.SGMLParser):
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        self.results=[]
        self.indata=False

    def start_div(self,attrs):
        divs=[v for k,v in attrs if k=='id']

        if 'result_box' in divs:
            self.indata=True
            

    def handle_data(self,data):
        if self.indata:
            self.results.append(data)
            self.indata=False
lin = 'en'
lout = 'zh_CN'
#lout = 'en'
text = 'dog'
req_data={"hl":"zh-cn","ie":"UTF-8",'text':text,"langpair":"%s|%s" % (lin,lout)}
req_url='http://translate.google.cn/translate_t'

data=urllib.urlencode(req_data)
req=urllib2.Request(req_url,data)

req.add_header('User-Agent','Mozilla/4.0')
data=urllib2.urlopen(req).read()
#print data

tp=TranstParser()
tp.feed(data)

for a in tp.results:
    print a
