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

def GetUserInfo(userid):
	n = flickr_api.method_call.call_api(method = "flickr.people.getInfo",user_id=userid)
	realname=n['person']['realname']
	location=n['person']['location']
	numberofphotos=n['person']['photos']['count']
	url=n['person']['photosurl']
	Details = 'Name: '+str(realname)+'\t Location: '+str(location)+'\t PhotoCount: '+str(numberofphotos)+'\t PhotosURL: '+url
	#print Details
	return Details

with open('usersname.txt','rb') as infile:
	with open('psychoflickr_userinfo', 'wb') as m:
		reader=csv.reader(infile)
		for user in reader:
		  try:
			userid=user[0]
			print userid
			if userid[0].isdigit():
				Details=GetUserInfo(userid)
				Details='UserID: '+str(userid)+'\t'+Details
				m.write(' %s\n' % str(Details))
				m.flush()
				#m.write('UserID: %s \t %s \n' % (str(userid),str(Details)))
			
			else:
				username=userid
				userid=GetUserid(userid)
				userid=convert(userid)
				Details=GetUserInfo(userid)
				Details='UserID: '+str(userid)+'\t'+Details+'\t Username: '+username
				m.write(' %s\n' % str(Details))
				m.flush()				
						
		  except:
			a = open('FailedUsers2.txt','a')
			a.write(str(userid))
			a.write('\n')
		  	pass
