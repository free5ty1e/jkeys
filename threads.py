import threading
import time

def threaded(f):
	def wrapper(*args):
		t = threading.Thread(target=f, args=args)
		t.start()
	return wrapper
