#!/usr/bin/python

import urllib2
import urllib
import re
import xml.dom.minidom
import os

class SongUrl:
    def __init__(self,artist='',title='',url=''):
        self.artist=artist
        self.title=title
        self.url=url

    def decode(self,artist_song):
        strs=artist_song.split('+')
        self.title=strs[0]
        if len(strs)==2:
            self.artist=strs[1]
        else:
            self.artist='+'.join(strs[1:])

baidu_mp3 = 'http://list.mp3.baidu.com/list/newhits.html?top1'
mp3url = '<td><a href="http://mp3.baidu.com/m?tn=baidump3&ct=134217728&lm=-1&li=2&word='
mp3url_real = '<td class=d><a href="http://220.181.38.82/m?ct=134217728&tn=baidusg,'

a=urllib2.urlopen(baidu_mp3).read()

song_urls=[]
for line in a.split("\n"):
    if line.strip().startswith(mp3url):
        line=line.strip()
        other=line[len(mp3url):]
        other_dot=other.index('"')
        artist_song=line[len(mp3url):len(mp3url)+other_dot]
        song_url=line[line.index('"')+1:len(mp3url)+other_dot]
        su=SongUrl()
        su.url=song_url
        su.decode(urllib.unquote(artist_song))
        song_urls.append(su)

#down_dir='c:/temp/mp3-top100'
down_dir=os.environ['HOME']+'/NationPhoto'
#s1=song_urls[1]
def getTagText(nodes):
    rc = ''
    for node in nodes.childNodes:
        if node.nodeType in ( [node.TEXT_NODE , node.CDATA_SECTION_NODE ] ):
            rc = rc + node.data
    return rc

def cencode(strs):
    return strs.decode('gbk').encode('utf-8')

def isFileDownloaded(songurl):
    artist=songurl.artist
    title=songurl.title

    for ext in ['mp3','wma','rm']:
        filename='%s/%s-%s.%s' % (down_dir,cencode(artist),cencode(title),ext)

        if os.path.exists(filename):
            return True

    return False


box_url='http://box.zhangmen.baidu.com/x?'
download_urls=[]
for s1 in song_urls:
    if isFileDownloaded(s1):
        continue
    mp3_url=urllib.urlencode({'op':12,'count':1,'title':'%s$$%s$$$$' % (s1.title,s1.artist)})
    mp3_url=box_url+mp3_url
    #print mp3_url
    b=urllib2.urlopen(mp3_url).read()
    xmlfile = b.decode('gbk').encode('UTF-8')
    xmlfile = xmlfile.replace('encoding="gb2312"','encoding="utf-8"')

    dom = xml.dom.minidom.parseString(xmlfile)

    root = dom.documentElement

    data_node=root.getElementsByTagName('data')[0]
    encode_str=getTagText(data_node.getElementsByTagName('encode')[0])
    decode_str=getTagText(data_node.getElementsByTagName('decode')[0])
    type_str=getTagText(data_node.getElementsByTagName('type')[0])

    file_ext='mp3'
    if type_str=='2':
        file_ext='wma'
    if type_str=='1':
        file_ext='rm'

    font_site=encode_str[0:encode_str.rfind("/")]
    mp3_down_url=font_site+'/'+decode_str
    mp3_file_name=down_dir+'/'+s1.artist+'-'+s1.title+'.'+file_ext

    if mp3_down_url.startswith('http'):
        download_urls.append(mp3_down_url.encode('gbk'))
	os.system('axel  "%s" -o "%s" -a' % (mp3_down_url.encode('gbk'),mp3_file_name.decode('gbk').encode('utf-8')))
