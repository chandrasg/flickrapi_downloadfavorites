import pprint, os, sys,argparse,json,csv,math
path = '.'
files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and os.stat(i).st_size>2 and '_SourceList' in i]
userids=[]
	
i=0
for filename in files:
	userids.append(filename.split("_",1)[0])

with open('psychoflickr_output.csv','wb') as out:
	out.write(',image_url,photo_url,label,_split\n')
	for userid in userids:
		filename=str(userid)+'_SourceList'
		with open(filename,'rb') as infile:	
			reader=csv.reader(infile)
			reader_list=list(reader)
			train_split=int(math.ceil(0.80*len(reader_list)))
			split_count=0
			for url in reader_list:
				page=url[0].rsplit('/',1)[1]
				page=page.split("_",1)[0]
				if split_count > train_split:
					Output=str(page)+','+str(url[0])+','+'http://www.flickr.com/photos/'+str(userid)+'/'+str(page)+','+str(i)+',test'
				else:
					Output=str(page)+','+str(url[0])+','+'http://www.flickr.com/photos/'+str(userid)+'/'+str(page)+','+str(i)+',train'
				out.write('%s\n' % str(Output))
				out.flush()
				split_count=split_count+1
		i=i+1
	out.close()

clean_lines = []
with open('psychoflickr_output.csv', "r") as f:
    lines = f.readlines()
    clean_lines = [l.strip() for l in lines if l.strip()]

with open('psychoflickr_output.csv', "w") as f:
    f.writelines('\n'.join(clean_lines))
