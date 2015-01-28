#! /usr/bin/env python

import flickr_api, pprint, os, sys,argparse,json,csv
flickr_api.set_keys(api_key = '52182e4e29c243689f8a8f45ee2939ae', api_secret = 'a6238b15052797dc')

def GetFavorites(userid):
	PhotoList=[]
	#filename=userid+"_PhotoList"
	#f = open(filename, 'wb')
	p = flickr_api.method_call.call_api(method = "flickr.favorites.getPublicList",user_id = userid,per_page=500)
	max_pages=p['photos']['pages']
	print "Pages Found "+ str(max_pages)
	for pages in range(1,max_pages):
		r = flickr_api.method_call.call_api(method = "flickr.favorites.getPublicList",user_id = userid,per_page=500,page=pages)
		for r in r['photos']['photo']:
			PhotoList.append(r['id'])
			#f.write('%s \n' % r['id'])
	#f.close()
	#filename2=userid+"_RawPhotoList"
	#f=open(filename2,'wb')
	#f.write(repr(PhotoList))
	#f.close()
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

def GetTagsInfo(PhotoList,userid)
	with open(userid+'_info','wb') as infile: 
		for PhotoId in PhotoList:
			tags=[]
			Loc=[]
			r=flickr_api.method_call.call_api(method = "flickr.photos.getInfo",photo_id = PhotoId)
			pageurl=r['photo']['urls']['url']
			pageurl=convert(pageurl[0])
			pageurl=pageurl['text']
			try:
				for tag in r['photo']['tags']['tag']:
					tags.append(convert(tag['text']))					
			except:
				pass
			try:
				lat=r['photo']['location']['latitude']
				long=r['photo']['location']['longitude']
				region=convert(r['photo']['location']['region']['text'])
				country=convert(r['photo']['location']['country']['text'])
				Loc='lat: '+str(lat)+',long: '+str(long)+',region: '+str(region)+',country: '+str(country)
			except:
				pass
			infile.write('PhotoID: %s \t,PageURL: %s \t,Tags: %s \t,Location: %s\n' % (str(PhotoID),str(pageurl),str(tags),str(Loc)))

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
			GetTagsInfo(PhotoList,userid)
			print userid+" Tags_Retrieved"
			#print "Found %s Photos after coming back :P..." % (len(PhotoList))
			#SourceList = GetSource(userid,PhotoList,SizeToDownload)
			print userid+" Completed"
		else:
			print userid
			userid=GetUserid(userid)
			userid=convert(userid)
			print userid
			SizeToDownload = 'Large'
			PhotoList = GetFavorites(userid)
			print userid+" PhotoList_Retrieved"
			GetTagsInfo(PhotoList,userid)
			print userid+" Tags_Retrieved"
			#print "Found %s Photos after coming back :P..." % (len(PhotoList))
			#SourceList = GetSource(userid,PhotoList,SizeToDownload)
			print userid+" Completed"
			
	  except:
		a = open('FailedUsers_info.txt','a')
		a.write(str(userid))
		a.write('\n')
	  	pass
