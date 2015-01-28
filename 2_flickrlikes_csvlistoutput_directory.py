"""
Run this first on unix

for i in $(ls); do                        # runs through the 'items' in this dir                               
  if [ -d $i ]; then                      # if this is a dir
     fname=${i##*/}                 # pick up the dir name which will be used as prefix
     echo $fname                           
     cd -- $i                                    # move into the dir       
     for z in *.jpg; do               # loop over files starting with test and fq extension
       echo $z  
       mv -- $z ${fname}_${z}         # put the prefix to the file.               
     done                                        
     cd ..                                         
  fi                                              
done

This will rename all files by adding the foldername as the prefix
 Script to write a csv file with paths of original psychoflickr dataset given the 
folders of the dataset are in path
"""
import pprint, os, sys,argparse,json,csv,math,pandas
from os import listdir
from os.path import isfile, join

path = '/home/sharathc001/psychoflickr/Flickr_Personality_SelfCollected'
folders=dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
i=0

with open(path+'/psychoflickr_newset_output.csv','wb') as out:
	out.write(',image_url,_split,label\n')
	for folder in folders:
		train_split=int(math.ceil(0.80*len(os.listdir(path+'/'+folder))))
#		print 'train_split is '+str(train_split)
		split_count=0
		split=[]
		for filename in os.listdir(path+'/'+folder):
			if filename.endswith(".jpg"):
				name= filename.rsplit('_',1)[0]
				filepath=folder+'/'+filename
				if split_count < train_split:
					split='train'
					#print split
				else:
					split='test'
					#print split
				#output=name+','+path+'/'+filepath+','+split+','+str(i)
				output=path+'/'+filepath+','+str(i) #For FeatExtraction
				out.write('%s\n' %str(output))
				out.flush()
				split_count=split_count+1				
#				print 'split_count is '+str(split_count)
		i=i+1

clean_lines = []
with open(path+'/psychoflickr_newset_output.csv', "r") as f:
    lines = f.readlines()
    clean_lines = [l.strip() for l in lines if l.strip()]

#print "over"

with open(path+'/psychoflickr_newset_output.csv', "w") as f:
    f.writelines('\n'.join(clean_lines))


#Do this on unix - no need of python to move images. 
# find ./ -name '*.jpg' -exec cp '{}' ./ \; To copy all images in subdirectories into the parent directory
# mv *.jpg images/

#mypath='/home/sharathc001/images'
#cols=['image_url','_split','label']
#indata=pandas.read_csv('psychoflickr_output.csv',names=cols)
#urls=list(indata.image_url)
#split=list(indata._split)
#labels=list(indata.label)

#with open('train.csv','wb') as train, open('test.csv',wb') as test:
#	files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
#	for url in 	
	
	
		


