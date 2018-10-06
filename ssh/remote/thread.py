import thread
import time
import os

def print_time(threadName, delay):
#	count = 0
#	while count < 5:
#		time.sleep(delay)
	#	count += 1
	while True:
		time.sleep(1)
		print "%s: %s"% (threadName, time.ctime(time.time()) )
def term(data=None):
	os.system(data)
try:
	thread.start_new_thread(print_time, ("Thread-1", 2, ))
	thread.start_new_thread(term("python mata.py"))
	thread.start_new_thread(term("xterm -e python thread.py"))

except:
	print "error"

while 1:
	pass
