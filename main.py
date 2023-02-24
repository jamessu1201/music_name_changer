import asyncio
from shazamio import Shazam
import os

ban_char=['"','/','\\']

def split_name():   #split path and filename
	inp=input()
	path=os.path.split(inp)
	return path[0]+'/',path[1]

async def song_search(position,filename): #search the song
	shazam = Shazam()
	song = await shazam.recognize_song(position+filename)
	if not song['matches']:		#if shazam can't regonized the song then pass it
		return False,'no match song'
	title=str(song['track']['title'])
	subtitle=str(song['track']['subtitle'])
	for ban in ban_char:
		title=title.replace(ban,' ')
		subtitle=subtitle.replace(ban,' ')
	songname=title+' - '+subtitle+'.mp3'
	return True,songname

async def song_rename(position,filename):
	
	if(not os.path.isfile(position+filename)):	#if file not exist then return
		return False,'file not found.'
	
	if(' - ' in filename):  #if filename is renamed then pass it
		return False,'file renamed.'

	
	fail_code,songname=await song_search(position,filename)
	if(fail_code==False):
		return False,songname

	if(not os.path.isfile(position+songname)):
		os.rename(position+filename,position+songname)
		return True,'successful! renamed '+songname
	return False,songname+" name exists,"+filename+" can't rename"








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
	fail_code,fail_content=loop.run_until_complete(song_search(path,name))
	print(fail_content)