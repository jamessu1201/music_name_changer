from ShazamAPI import Shazam  #use shazam to recognize song
import os #use os to rename the file

def split_name():
	path=input()
	a=path.rfind('/',0,len(path)-1)
	name=path[a+1:]
	path=path[:a+1]
	return path,name

def song_search(position,filename):
	file = open(position+filename, 'rb').read()

	shazam = Shazam(file)
	recognize_generator = shazam.recognizeSong()
	while True:
		print(next(recognize_generator))

def song_rename(position,filename):
    
	if(not os.path.isfile(position+filename)):	#if file not exist then return
		print("file not fonud.")
		return False
	
	if(' - ' in filename):
		print("file renamed.")
		return False

	file = open(position+filename, 'rb').read()

	shazam = Shazam(file)
	recognize_generator = shazam.recognizeSong()
	song=next(recognize_generator)
	print(song)
	songname=song[1]['track']['title']+' - '+song[1]['track']['subtitle']+'.mp3'
	os.rename(position+filename,position+songname)
	print('successful! renamed',songname)
	return True

print('1:one file 2:multiple files:')
choose=int(input())
while choose!=1 and choose!=2 and choose!=3:
	print('no instruction!')
	print('1:one file 2:files in folder:')
	choose=int(input())

if choose==1:
	print("input file's path(ex. C://aaa.mp3):")
	path,name=split_name()
	fail=song_rename(path,name)
	while fail==False:
		path,name=split_name()
		fail=song_rename(path,name)

elif choose==2:
	print("input folder path:")
	path=input()
	files=os.listdir(path)
	for file in files:
		a=song_rename(path+'/',file)
		if a==123:
			break

elif choose==3:
	print("input:")
	path,name=split_name()
	song_search(path,name)