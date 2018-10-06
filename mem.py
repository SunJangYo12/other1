from ssh.client import Client
from ssh.models import *
import os

print "Running    ..."
cmain = open("/root/AL/control.txt",'r')
if cmain.read() == "run":
	cmain = open("/root/AL/control.txt",'w')
	cmain.write("nonrun")
	client = Client('085731276166','{pesawat}')
	client.listen()
cmain.close()

dssh = open("/root/AL/isi.txt",'r')
if dssh.read() == "u'kamera'":
	import pygame
	import pygame.camera

	pygame.camera.init()
	cam = pygame.camera.Camera("/dev/video0", (640,480))
	cam.start()
	img = cam.get_image()
	pygame.image.save(img, "/root/al.jpg")
	cam.stop()
	
	sukses = client.sendLocalImage("/root/al.jpg", thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
	if sukses:
		os.system("rm /root/al.jpg")
		client.send(Message(text = 'respon ...'), thread_id=100022394016980, thread_type=ThreadType.USER)

dssh.close()

def main():
	akses = True
	while akses:
		perintah = raw_input("--->> Perintah : ")
		if perintah == "upload":
			pilihan = raw_input("---> gambar/text/db --->")
			if pilihan == "gambar":
				jenis = raw_input("---> ENTER=camera, gambar=path --->")
				if jenis != "":
					print online_db(True, "gambar")
				else:
					print online_db(True, "camera")
			elif pilihan == "text":
				client = Client("081229059446", "{pesawat}") # AL
				client.send(Message(text = "msgText"), thread_id=100022394016980, thread_type=ThreadType.USER) # ke shun
			elif pilihan == "db":
				print online_db(True, "db")
		elif perintah == "listen":
			client = Client('085731276166','{pesawat}')
			client.listen()
		elif perintah == "history":
			lihat = raw_input("==>> Lihat = t/n/cari/reset : ")
			if lihat == "t":
				print offline_db("lihat")
			elif lihat == "n":
				print offline_db("lihat urut")
			elif lihat == "cari":
				print offline_db("cari")
		elif perintah == "q":
			akses = False
		elif perintah == "help":
			print "1. upload  = gambar/text atau ENTER database"
			print "    -> jika gambar maka masukan pathnya"
			print "        misal : /root/Unduhan/skema.jpg"
			print "    -> jika kamera pertama tekan ENTER"
			print "        begitu pula jika ingin mengulangi ENTER"
			print "    -> jika text maka masukan textnya"
			print "    -> jika database maka masukan db"
			print "2. listen  = mode pesan mesenger"
			print "3. history = urutan t(tanggal), n(nama), cari(mencari history), reset(hapus \n    semua history)"
			print "4. browser"
			print "\n\n"
		elif perintah == "browser":
			os.system("firefox https://http-www-bing-com.0.freebasics.com/search?iorg_service_id_internal=803478443041409%3BAfrEX0ng8fF-69Ni&iorgbsid=AZwXpPHKQLV_zW2EUSXZjJi7iOTUenLobrssI_iyhhE-ZkJDQNQRKAxWEXjqZnXWMUkQSRxPxVcN-tItD7kwpF1k&q=cara&qs=&form=QBLH&pc=FBIO")
		else:
			print offline_db("buat", perintah)
