from client import *
import os
import datetime
import threading
exitFlag = 0
threadLock = threading.Lock()
threads = []


class myThread(threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print "Starting "+ self.name
		threadLock.acquire() # lock thread
		index(self.name, 5, self.counter)
		threadLock.release() # free thread

class Starting:
	def __init__(self, data=None):
		self.data = data
	def getOut(self, jum=None):
		ha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
		print self.data+"\n\n ----->>> [%s]"%ha+" ke - [%d] <<<------"%jum

	def getLocal(self):
		isi = open('/root/AL/variable.txt','r')
		return isi.read()
		isi.close()

	def setLocal(self, pdata):
		isi = open('/root/AL/variable.txt', 'w')
		isi.write(pdata)
		isi.close()
	
	def setKonstLocal(self, kpdata):
		isi = open('/root/AL/konstanta.txt', 'w')
		isi.write(kpdata)
		isi.close()

	def setDatabase(self, control=None, isi=None, read=None):
		pathDB = "/root/AL/"
		if control == "lihat":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect * from catatan;\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return db
		elif control == "lihat urut":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nSELECT * FROM catatan ORDER BY isi;\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return db
		elif control == "buat":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\ninsert into catatan values("+"'"+isi+"'"+");\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return "Berhasil dibuat"
		elif control == "reset":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nDELETE FROM catatan;\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return db
		elif control == "cari":
			#cari = raw_input("Cari Huruf pertama : ")
			cari = read
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect * from catatan where substring(isi, 1, 1)="+"'"+cari+"'"+";\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return db
		elif control == "setKonstanta":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\ninsert into memori values("+"'"+isi+"'"+",'');\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return "Berhasil dibuat"
		elif control == "setVariable":
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\ninsert into memori values('',"+"'"+isi+"'"+");\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			return "Berhasil dibuat"
		elif control == "getKonstanta":
			#cari = raw_input("Cari Huruf pertama : ")
			cari = read
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect konstanta from memori where substring(konstanta, 1, 1)="+"'"+cari+"'"+";\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			b = db.split("\n")
			c = b.__len__()
			return b[c-2]
		elif control == "getVariable":
			#cari = raw_input("Cari Huruf pertama : ")
			cari = read
			otak = open(pathDB+"offlineDB.sh",'w')
			otak.write("#!/bin/bash\n\n<<EOF mysql -u root;\nuse otak;\nselect variable from memori where substring(variable, 1, 1)="+"'"+cari+"'"+";\nEOF")
			otak.close()
			db = os.system("chmod 777 "+pathDB+"offlineDB.sh")
			db = os.popen("sh "+pathDB+"offlineDB.sh").read()
			b = db.split("\n")
			c = b.__len__()
			return b[c-2]
		else:
			return "urutan t(tanggal), n(nama), cari(mencari history), reset(hapus semua history)"
	
def index(threadName, counter, delay):
	mulai = Starting()
	while counter:
		time.sleep(delay)
		print "%s: %s"% (threadName, mulai.getLocal())
		
		counter -= 1

def inThread():
	thread1 = myThread(1, "Thread-1", 1)
	thread1.start()
	threads.append(thread1)
	for t in threads:
		t.join()
	print "Exiting main thread"
	inThread()
if __name__ == "__main__":
	try:
        try:
        	s = Starting()
        	if (s.setDatabase(control='getKonstanta', read='i') == "index_destroy"):
				s.setDatabase(control='setKonstanta', isi='index_run')
				inThread()
        	else:
        		print "index sudah dijalankan!!"
        except KeyboardInterrupt:
        	print " : index onDestroy"
        	s = Starting()
        	s.setDatabase(control='setKonstanta', isi='index_destroy')

    except Exception, e:
        print e
		
