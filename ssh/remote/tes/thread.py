import time

def thread1():
	b = 0
	while True:
		b += 1
		print b
		time.sleep(1)
		pass
def thread2():
	a = 0
	while True:
		a += 1
		print a
		time.sleep(1)
		if a == 5:
			break
		else:
			pass
thread1() & thread2()
