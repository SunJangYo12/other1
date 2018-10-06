import cv2
from index import *
import datetime

class runCV:
	def __init__(self):
		face_cascade = cv2.CascadeClassifier('/usr/local/lib/python2.7/dist-packages/cv2/data/haarcascade_frontalface_alt.xml')
		eye_cascade = cv2.CascadeClassifier('/usr/local/lib/python2.7/dist-packages/cv2/data/haarcascade_eye.xml')

		cap = cv2.VideoCapture(0)
		waktu_kamera = datetime.datetime.now().strftime("%H:%M")
		hari_kamera = datetime.datetime.now().strftime("%Y-%m-%d   %H:%M")
		index = Starting()

		while True:
			print "oke"
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			waktu_kamera = datetime.datetime.now().strftime("%H:%M")
			hari_kamera = datetime.datetime.now().strftime("%Y-%m-%d   %H:%M")

			if waktu_kamera == "08:45":
				print "Setor perhari"
				cv2.imwrite('/root/AL/setor.jpg',frame)
				index.setLocal('setor')
				#client.send(Message(text = 'Tanggal : [ %s ]'%hari_kamera), thread_id=100022394016980, thread_type=ThreadType.USER)
				#client.sendLocalImage("/root/AL/kamera.jpg", thread_id=100022394016980, thread_type=ThreadType.USER)
			if index.getLocal() == 'kamera':
				cv2.imwrite('/root/AL/kamera.jpg',frame)
				index.setLocal('sukses kamera')

			faces = face_cascade.detectMultiScale(gray, 1.3, 5)
			for (x,y,w,h) in faces:
				print "     Danger !!!"
				cv2.imwrite('/root/AL/adaorang.jpg',frame)
				
				cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color= frame[y:y+h, x:x+w]

				eyes = eye_cascade.detectMultiScale(roi_gray)
				for (ex,ey,ew,eh) in eyes:
					cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,0,255), 2)

			cv2.imshow("Mata", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		cap.release()
		cv2.destroyAllWindows()

if __name__ == "__main__":
	#os.system("sh /root/AL/ping.sh")
	try:
        try:
        	s = Starting()
        	if (s.setDatabase(control='getKonstanta', read='m') == "mata_destroy"):
				s.setDatabase(control='setKonstanta', isi='mata_run')
				ma = runCV()
        	else:
        		print "mata sudah dijalankan!!"
        except KeyboardInterrupt:
        	print " : mata onDestroy"
        	s = Starting()
        	s.setDatabase(control='setKonstanta', isi='mata_destroy')

    except Exception, e:
        print e
