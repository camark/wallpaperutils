#!/usr/bin/python

import flickrapi
import os
import time
import Image

day=int(time.strftime('%d'))
if day %2 == 1:
    api_key ='api-key1'
    secret_key='sk1'
else:
    api_key ='api-key2'
    secret_key='sk2'

flickr = flickrapi.FlickrAPI(api_key,secret_key)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
    raw_input('Press enter after authorized this program')

flickr.get_token_part_two((token,frob))



def callback(progress,done):
    if done:
        print 'upload to flickr'

class UploadHistory:
	def __init__(self,filename='uh.dat'):
		self.filename=os.environ['HOME']+'/python/uh.dat'
		self.uploads=[]
	def readcfg(self):
		if os.path.exists(self.filename):
			f=open(self.filename,'r')
			for line in f.readlines():
				self.uploads.append(line[0:-len(os.linesep)])

			f.close()

	def writecfg(self):
		f=open(self.filename,'w')
		for up in self.uploads:
			f.write(up+os.linesep)

		f.close()

	def isUploaded(self,filename):
		if self.uploads.count(filename)>0:
			return True
		else:
			self.uploads.append(filename)
			return False

	def addUpload(self):
		pass

def isGG(filename):
    im=Image.open(filename)
    if im.size[0]==100 or im.size[1]==100:
        return True
    else:
        return False

homedir=os.environ['HOME']
today=time.strftime('%Y-%m-%d')
savedir=homedir+'/temp/'+today

files=os.listdir(savedir)
uh=UploadHistory()

for f in files:
    if f[-4:]=='.jpg':
        rf = savedir + '/' + f
	if not uh.isUploaded(rf) and not isGG(rf):
	        flickr.upload(filename=rf,tags='iheartchaos',is_public=0)

uh.writecfg()
