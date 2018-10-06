from client import *


if __name__ == '__main__':
    try:
        try:
        	s = Starting()
        	if (s.setDatabase(control='getKonstanta', read='p') == "ping_destroy"):
        		client = Client('','')
        	else:
        		print "ping sudah dijalankan!!"
        except KeyboardInterrupt:
        	print " : ping onDestroy"
        	s = Starting()
        	s.setDatabase(control='setKonstanta', isi='ping_destroy')

    except Exception, e:
        print e

