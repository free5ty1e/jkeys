import threading
import time

def threaded(f):
	def wrapper(*args):
		t = threading.Thread(target=f, args=args)
		t.setDaemon(True) # wont keep app alive
		t.start()
	return wrapper
