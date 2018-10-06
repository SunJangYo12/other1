from client import *
import os

client = Client('082314542546','#0987654321')

while True:
	#msg = input("oke")
	client.send(Message(text = "msg"), thread_id=100022394016980, thread_type=ThreadType.USER)

