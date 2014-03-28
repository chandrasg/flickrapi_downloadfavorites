#! /usr/bin/env python

import flickr_api, pprint, os, sys,argparse,json,csv
flickr_api.set_keys(api_key = '52182e4e29c243689f8a8f45ee2939ae', api_secret = 'a6238b15052797dc')

def DownloadSource(SourceList, PhotosetTitle):
        
        for url in SourceList:
                os.system("wget --append-output=download.log --no-verbose --no-clobber -P '%s' -i %s" % (PhotosetTitle,'downloadstack'))
		#print url
                pass


def GetSource(PhotoList,SizeToDownload):
        SourceList = []
        f = open('downloadstack', 'wb')

        for PhotoId in PhotoList:
		
                r = flickr_api.method_call.call_api(
                        method = "flickr.photos.getSizes",
                        photo_id = PhotoId
                    )
                for Size in r['sizes']['size']:
                        if Size['label'] == SizeToDownload:
                                SourceList.append(Size['source'])
                                f.write('%s \n' % Size['source'])
		
        f.close()	
        return SourceList

def GetInfo(PhotoList,userid):
	for PhotoId in PhotoList:
		g = open('/home/chandrasg/Desktop/%s/%s_Info.json'%(userid,PhotoId),'wb')
		g=convert(g)
		h = open('/home/chandrasg/Desktop/%s/%s_Exif.json'%(userid,PhotoId),'wb')
		h=convert(h)

		#print g
		q= flickr_api.method_call.call_api(
                        method = "flickr.photos.getInfo",
                        photo_id = PhotoId,
			format='xml'
                    )
		q=convert(q)
		g.write(str(q))
		g.close()       		
		
		r=flickr_api.method_call.call_api(
                        method = "flickr.photos.getExif",
                        photo_id = PhotoId,
			format='xml'
                    )
		r=convert(r)
		h.write(str(r))
		h.close()       		

def GetFavorites(userid):
	PhotoList=[]
	r = flickr_api.method_call.call_api(
                method = "flickr.favorites.getPublicList",
                user_id = userid,
		per_page=200
                )
	
	for r in r['photos']['photo']:
		PhotoList.append(r['id'])
	return PhotoList

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def GetUserid(userid):
	userid= "http://www.flickr.com/photos/"+userid+"/"
	r = flickr_api.method_call.call_api(
                method = "flickr.urls.lookupUser",
                url=userid
                )
	return r['user']['id'] 

def GetUserfriends(userid):
	h = open('/home/chandrasg/Desktop/%s_friends.json'%userid,'wb')
	h=convert(h)
	q= flickr_api.method_call.call_api(
                        method = "flickr.contacts.getPublicList",
                        user_id = userid,
			format='xml'
                    )
	q=convert(q)
	g.write(str(q))
	g.close() 

with open('users.txt','rb') as infile:
	reader=csv.reader(infile)
	for user in reader:
		userid=user[0]
		if userid[0].isdigit():
			print userid
			
			SizeToDownload = 'Large'
			PhotoList = GetFavorites(userid)
			print "Found %s Photos..." % (len(PhotoList))
			SourceList = GetSource(PhotoList,SizeToDownload)
			print "Downloading %s Photos..." % (len(SourceList))
			DownloadSource(SourceList,userid)
			GetInfo(PhotoList,userid)
			GetUserfriends(userid)
			os.remove('./downloadstack')
		else:
			print userid
			userid=GetUserid(userid)
			userid=convert(userid)
			print userid
			
			SizeToDownload = 'Large'
			PhotoList = GetFavorites(userid)
			print "Found %s Photos..." % (len(PhotoList))
			SourceList = GetSource(PhotoList,SizeToDownload)
			print "Downloading %s Photos..." % (len(SourceList))
			DownloadSource(SourceList,userid)
			GetInfo(PhotoList,userid)
			GetUserfriends(userid)
			os.remove('./downloadstack')
