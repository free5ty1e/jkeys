from ctypes import *

class XKeys(object):

	def __init__(self):
		self.__Xtst = CDLL("libXtst.so.6")
		self.__Xlib = CDLL("libX11.so.6")
		self.__dpy = self.__Xtst.XOpenDisplay(None)
	
	def SendInput(self, txt):
		for c in txt:
			sym = self.__Xlib.XStringToKeysym(c)
			code = self.__Xlib.XKeysymToKeycode(self.__dpy, sym)
			self.__Xtst.XTestFakeKeyEvent(self.__dpy, code, True, 0)
			self.__Xtst.XTestFakeKeyEvent(self.__dpy, code, False, 0)
			self.__Xlib.XFlush(self.__dpy)


	def SendKeyPress(self, key):
		sym = self.__Xlib.XStringToKeysym(str(key))
		code = self.__Xlib.XKeysymToKeycode(self.__dpy, sym)
		self.__Xtst.XTestFakeKeyEvent(self.__dpy, code, True, 0)
		self.__Xlib.XFlush(self.__dpy)

	def SendKeyRelease(self, key):
		sym = self.__Xlib.XStringToKeysym(str(key))
		code = self.__Xlib.XKeysymToKeycode(self.__dpy, sym)
		self.__Xtst.XTestFakeKeyEvent(self.__dpy, code, False, 0)
		self.__Xlib.XFlush(self.__dpy)
		
	def SendMouseButtonPress(self, button):
	    self.__Xtst.XTestFakeButtonEvent(self.__dpy,button,1, 10);
	    self.__Xlib.XFlush(self.__dpy)
	    
	def SendMouseButtonRelease(self, button):
	    self.__Xtst.XTestFakeButtonEvent(self.__dpy,button,0, 10);
	    self.__Xlib.XFlush(self.__dpy)	    
