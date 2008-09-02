#!/usr/bin/python

import time
from urllib import urlretrieve
import os

#image_url='http://images.ucomics.com/comics/ga/2008/ga080801.gif'
image_url='http://images.ucomics.com/comics/ga'
thisyear=time.strftime('%Y')
today=time.strftime('%y%m%d')

today_imageUrl=image_url+'/'+thisyear+'/ga'+today+'.gif'

#a=urlopen(today_imageUrl).read()

dirname=os.environ['HOME']+'/NationPhoto'
if not os.path.exists(dirname):
    os.mkdir(dirname)
savefilename=dirname+'/ga'+today+'.gif'

##f=open(savefilename,'wb')
##f.write(a)
##f.close()
urlretrieve(today_imageUrl,savefilename)

