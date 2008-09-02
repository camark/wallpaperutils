#!/usr/bin/python

import time
import urllib2
import xml.dom.minidom

today = time.strftime("%Y-%m-%d")
baidu_url = 'http://hi.baidu.com/ui/text/olympic/nsatom_gold.xml?t=' + today

xmlfile = urllib2.urlopen(baidu_url).read()
xmlfile = xmlfile.decode('gbk').encode('UTF-8')
xmlfile = xmlfile.replace('encoding="gbk"','encoding="utf-8"')

dom = xml.dom.minidom.parseString(xmlfile)

root = dom.documentElement


def getTagText(nodes):
    rc = ''
    for node in nodes.childNodes:
        if node.nodeType in ( [node.TEXT_NODE , node.CDATA_SECTION_NODE ] ):
            rc = rc + node.data

    return rc

def outbyformat(modals):
    title='Country          Gold  Sliver Bronze  Total'
    item ='#country              #gold    #silver      #bronze      #total'
    print title
    for modal in modals:
        item_text=item
        for str_text in ['country','gold','silver','bronze','total']:
            item_text=item_text.replace('#'+str_text,modal[str_text])

        print item_text

def output(modals):
    for modal in modals:
        print '%s %s %s %s %s' % (modal['country'],
                                  modal['gold'],
                                  modal['silver'],
                                  modal['bronze'],
                                  modal['total']
                                  )
modals=[]
for node in root.getElementsByTagName('entry'):
    nsmeta = node.getElementsByTagName('nsmeta')[0]
    MedalTable = nsmeta.getElementsByTagName('MedalsTable')[0]
   
    medalhash={}
    for str_text in ['country','gold','silver','bronze','total']:
        m_node = MedalTable.getElementsByTagName(str_text)[0]
        medalhash[str_text]=getTagText(m_node)

    modals.append(medalhash)

#outbyformat(modals)
output(modals)


    
