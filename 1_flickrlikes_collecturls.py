#! /usr/bin/env python

import flickr_api, pprint, os, sys,argparse,json,csv
flickr_api.set_keys(api_key = '52182e4e29c243689f8a8f45ee2939ae', api_secret = 'a6238b15052797dc')

def GetFavorites(userid):
	PhotoList=[]
	filename=userid+"_PhotoList"
	f = open(filename, 'wb')
	p = flickr_api.method_call.call_api(method = "flickr.favorites.getPublicList",user_id = userid,per_page=500)
	max_pages=p['photos']['pages']
	print "Pages Found "+ str(max_pages)
	for pages in range(1,max_pages):
		r = flickr_api.method_call.call_api(method = "flickr.favorites.getPublicList",user_id = userid,per_page=500,page=pages)
		for r in r['photos']['photo']:
			PhotoList.append(r['id'])
			f.write('%s \n' % r['id'])
	f.close()
	filename2=userid+"_RawPhotoList"
	f=open(filename2,'wb')
	f.write(repr(PhotoList))
	f.close()
	#print "Photos Found in"+userid+" "+"="+len(PhotoList)
	return PhotoList

def GetSource(userid,PhotoList,SizeToDownload):
	SourceList = []
	filename=userid+"_SourceList"
	f = open(filename, 'wb')
	for PhotoId in PhotoList:
		r = flickr_api.method_call.call_api(method = "flickr.photos.getSizes",photo_id = PhotoId)
		for Size in r['sizes']['size']:
			if Size['label'] == SizeToDownload:
				SourceList.append(Size['source'])
				f.write('%s \n' % Size['source'])
	f.close()	
	filename=userid+"_RawSourceList"
	f = open(filename, 'wb')
	f.write(repr(SourceList))
	f.close()
	return SourceList

def GetUserid(userid):
	userid= "http://www.flickr.com/photos/"+userid+"/"
	r = flickr_api.method_call.call_api(
                method = "flickr.urls.lookupUser",
                url=userid
                )
	return r['user']['id'] 

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

with open('usersname.txt','rb') as infile:
	reader=csv.reader(infile)
	for user in reader:
	  try:
		userid=user[0]
		#print userid
		if userid[0].isdigit():
			print userid
			SizeToDownload = 'Large'
			PhotoList = GetFavorites(userid)
			print userid+" PhotoList_Retrieved"
			#print "Found %s Photos after coming back :P..." % (len(PhotoList))
			SourceList = GetSource(userid,PhotoList,SizeToDownload)
			print userid+" Completed"
		else:
			print userid
			userid=GetUserid(userid)
			userid=convert(userid)
			print userid
			print userid
			SizeToDownload = 'Large'
			PhotoList = GetFavorites(userid)
			print userid+" PhotoList_Retrieved"
			#print "Found %s Photos after coming back :P..." % (len(PhotoList))
			SourceList = GetSource(userid,PhotoList,SizeToDownload)
			print userid+" Completed"
			
	  except:
		a = open('FailedUsers.txt','a')
		a.write(str(userid))
		a.write('\n')
	  	pass
