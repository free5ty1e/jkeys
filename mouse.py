
import Xlib.display
from threads import threaded
import time
from xkeys import XKeys
class mouseKeys():

    def __init__(self):
        self.__run = False
        self.__display = Xlib.display.Display()
        self.step = 2
        self.accleration_factor = 5
        self.__button = None
        self.__x = XKeys()
        return

    @threaded
    def StartMouseMove(self, key):
        self.step = 1
        if key.lower() == "up":
            x,y = 0, -self.step
        elif key.lower() == "down":
            x,y = 0, self.step
        elif key.lower() == "left":
            x,y = -self.step, 0
        elif key.lower() == "right":
            x,y = self.step, 0
        elif key.lower().startswith("click"):
            self.__button = int(key[5:])
            self.__x.SendMouseButtonPress(self.__button)
            return

        self.__run = True
        count = 0
        while self.__run:
            # move with accleration
            if count % self.accleration_factor == 0 : self.step = self.step + 1
            self.__display.warp_pointer(x * self.step, y * self.step)
            self.__display.sync()
            time.sleep(0.01)
            count = count + 1
        
    def StopMouseMove(self):
        self.__run = False
        if self.__button:
            self.__x.SendMouseButtonRelease(self.__button)
        self.__button = None
        return

