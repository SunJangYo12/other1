import os
import requests as req
from os import path
from subprocess import call
from client import Client
from fbssh.models import *

def online_db(control, isi):
	ftemp = ""
	try:
		client = Client("081229059446", "#pesawatjet") # AL
		if isi == "online":
			client.listen()
		while control:
			if isi == "gambar":
				pathku = raw_input("/root/gambar.png ---> ")
				if pathku != "":
					sukses = client.sendLocalImage(""+pathku+"", thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
					if sukses:
						print "\nSukses\n"
				else:
					control = False
			elif isi == "camera":
				delay = raw_input("ENTER untuk lagi atau q untuk keluar ---> ")
				if delay == "":
					foto()
					sukses = client.sendLocalImage("/root/al.jpg", thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
					if sukses:
						print "\nsukses\n"
				else:
					control = False
			elif isi == "text":
				msgText = raw_input("---> Masukan isi text q untuk exit ---> ")
				if msgText == "q":
					control = False
				else:
					kirim = client.send(Message(text = msgText), thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
					if kirim:
						print "\nsukses\n"
			elif isi == "db":
				uploadDB = ""
				uploadDB = offline_db("lihat")
				kirim = client.send(Message(text = uploadDB), thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
				if kirim:
					print "database sukses di upload"
					control = False
	except Exception, e:
		print "\nKoneksi gagal. karena : ", e	
	return ftemp
	
	

def offline_db(control, isi=None):
	pathDB = "/root/AL/"
	if control == "lihat":
		otak = open(pathDB+"offlineDB.sh",'w')
		otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect * from catatan;\nEOF")
		otak.close()
		db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
		db = os.popen("sh "+pathDB+"offlineDB.sh").read()
	elif control == "lihat urut":
		otak = open(pathDB+"offlineDB.sh",'w')
		otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nSELECT * FROM catatan ORDER BY isi;\nEOF")
		otak.close()
		db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
		db = os.popen("sh "+pathDB+"offlineDB.sh").read()
	elif control == "buat":
		otak = open(pathDB+"offlineDB.sh",'w')
		otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\ninsert into catatan values("+"'"+isi+"'"+");\nEOF")
		otak.close()
		db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
		db = os.popen("sh "+pathDB+"offlineDB.sh").read()
	elif control == "reset":
		otak = open(pathDB+"offlineDB.sh",'w')
		otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nDELETE FROM catatan;\nEOF")
		otak.close()
		db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
		db = os.popen("sh "+pathDB+"offlineDB.sh").read()
	elif control == "cari":
		cari = raw_input("Cari Huruf pertama : ")
		otak = open(pathDB+"offlineDB.sh",'w')
		otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect * from catatan where substring(isi, 1, 1)="+"'"+cari+"'"+";\nEOF")
		otak.close()
		db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
		db = os.popen("sh "+pathDB+"offlineDB.sh").read()
	return db
