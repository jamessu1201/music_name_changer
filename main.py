import asyncio
from shazamio import Shazam
import os

def split_name():   #split path and filename
	path=input()
	a=path.rfind('/',0,len(path)-1)
	name=path[a+1:]
	path=path[:a+1]
	return path,name

async def song_search(position,filename): #search the song but not renamed(for developer)
    shazam = Shazam()
    song = await shazam.recognize_song(position+filename)
    if not song['matches']:
        print('no match song.')
        return False,'no match song'
    songname=song['track']['title']+' - '+song['track']['subtitle']+'.mp3'
    print(songname)

async def song_rename(position,filename):
    
	if(not os.path.isfile(position+filename)):	#if file not exist then return
		return False,'file not found.'
	
	if(' - ' in filename):  #if filename is renamed then pass it
		return True,'file renamed.'

	shazam = Shazam()
	song = await shazam.recognize_song(position+filename)
	if not song['matches']:     #if shazam can't regonized the song then pass it
		return False,'no match song.'

	songname=song['track']['title']+' - '+song['track']['subtitle']+'.mp3'
	os.rename(position+filename,position+songname)
	return True,'successful! renamed'+songname








print('1:one file 2:multiple files:')
choose=int(input())
while choose!=1 and choose!=2 and choose!=3:
	print('no instruction!')
	print('1:one file 2:files in folder:')
	choose=int(input())

if choose==1:
	print("input file's path(ex. C://aaa.mp3):")
	path,name=split_name()
	loop = asyncio.get_event_loop()
	fail_code,fail_content=loop.run_until_complete(song_rename(path,name))
	while fail_code==False:
		print(fail_content,'please try again:')
		path,name=split_name()
		fail_code,fail_content=loop.run_until_complete(song_rename(path,name))
	print(fail_content)

elif choose==2:
	print("input folder path:")
	path=input()
	files=os.listdir(path)
	for file in files:
		loop = asyncio.get_event_loop()
		fail_code,fail_content=loop.run_until_complete(song_rename(path+'/',file))
		print(fail_content)

elif choose==3:
    print("input:")
    path,name=split_name()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(song_search(path,name))