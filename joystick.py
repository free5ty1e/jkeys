
import pygame
from xml.dom.minidom import *

from threads import threaded
from xkeys import XKeys

class JoyStickAxis():
    def __init__(self, lowKey, highKey):
        self.low = lowKey
        self.high = highKey

class JoyStick():
    def __init__(self):
        self.axis = { }
        self.buttons = { }
        
    def print_info(self):
        print "== Joystick %s ========================" % self.number
        for axis in self.axis:
            print " - axis %s direction low mapped to key %s" % (self.axis[axis].number, self.axis[axis].low)
            print " - axis %s direction high mapped to key %s" % (self.axis[axis].number, self.axis[axis].high)
            
        for key in self.buttons:
            print " - button %s mapped to key %s" % (key, self.buttons[key])
    
class JKeys:
    def __init__(self, conf):
    
        self.joysticks = {}
    
        # read config from xml doc
        f = open(conf, "r")
        xml = f.read()
        f.close()
        document = parseString(xml)
    
        for joy_node in document.getElementsByTagName("joystick"):
            joy = JoyStick()

            for axis_node in joy_node.getElementsByTagName("axis"):
                axis = JoyStickAxis( axis_node.getAttribute("low"), axis_node.getAttribute("high"))
                joy.axis[ axis_node.getAttribute("number") ] = axis
            
            for button_node in joy_node.getElementsByTagName("button"):
                joy.buttons[button_node.getAttribute("number")] = button_node.getAttribute("key")
            
            self.joysticks[int(joy_node.getAttribute("id"))] = joy
 
        
        pygame.init()
        

        self.nbJoy = pygame.joystick.get_count()

        for i in range(self.nbJoy):
            pygame.joystick.Joystick(i).init()
            
        if self.nbJoy == 0:
            print "Sorry no joysticks found!!"   
            
        elif self.nbJoy != len(self.joysticks):
            print "%d joysticks configured, only %d joysticks found" % (len(self.joysticks), self.nbJoy)
        
        self.debug = False

    @threaded
    def run(self):
    
        if self.nbJoy != 0:
            pygame.display.init()
            pygame.time.set_timer(1, 100)
            capture_events = [pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION, pygame.JOYBUTTONUP, pygame.JOYHATMOTION]
            x = XKeys()
            
            # clear out all pre existing pygame events else we get 1 of each
            pygame.event.clear()
            
            
            while True:
                pygame.event.pump()
                ev = pygame.event.wait()
                
                if ev.type in capture_events:

                    joy = self.joysticks[ ev.joy ]
                    
                    if ev.type == pygame.JOYHATMOTION:
                        res = gethatcode(ev)
                        if self.debug: print "UNHANDLED JOY HAT code: ", res
                        
                    elif ev.type == pygame.JOYBUTTONDOWN:
                        button = str(ev.button)
                        if joy.buttons.has_key(button):
                            key_code = joy.buttons[button]
                            if self.debug: print "Button down : " + key_code
                            x.SendKeyPress( key_code )
                    elif ev.type == pygame.JOYBUTTONUP:
                        button = str(ev.button)
                        if joy.buttons.has_key(button):
                            key_code = joy.buttons[button]
                            if self.debug: print "Button up : " + key_code
                            x.SendKeyRelease( key_code )
                        
                      
                    elif ev.type == pygame.JOYAXISMOTION:
                        axis_number = str(ev.axis)

                        if joy.axis.has_key(axis_number):
                        
                            axis = joy.axis[axis_number]
                            print axis.high
                            if ev.value < 0:
                                if self.debug: print "Button down : " + axis.low
                                x.SendKeyPress( axis.low )
                            
                            elif ev.value > 0:
                                if self.debug: print "Button down : " + axis.high
                                x.SendKeyPress( axis.high )
                            
                            else:
                                if self.debug: print "Button up : " + axis.low
                                if self.debug: print "Button up : " + axis.high
                                x.SendKeyRelease( axis.high )
                                x.SendKeyRelease( axis.low )

            pygame.display.quit()
            return res

    def __del__(self):
        pygame.quit()
 
