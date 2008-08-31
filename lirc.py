#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   irx game 
#   Copyright (C) 2008  Jason Taylor - killerkiwi2005@gmail.com
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.



import time
import tempfile

from threads import threaded
from xkeys import XKeys

class LircKeys:


    def __init__(self, document):

        
        self.buttons = {}
        self.config_file = None
        
        remotes = document.getElementsByTagName("remote")
        if len(remotes) > 0:
        
            try:
                import pylirc
            except:
                print "You need to install pylirc to capture remote controls"
                return
                
            remote = remotes[0]
            
            print 
            print "Remote lirc mappings found :"
            
            # create a temp file with config
            f, self.config_file = tempfile.mkstemp()
            f = open(self.config_file, "w")
            for button_node in remote.getElementsByTagName("button"):
                self.buttons[button_node.getAttribute("code")] = button_node.getAttribute("key")
            
                print " - button %s mapped to key %s" % (button_node.getAttribute("code"), button_node.getAttribute("key"))
                
                f.write("begin\n")
                f.write("\tprog = irkeys\n")
                f.write("\tbutton = %s\n" % button_node.getAttribute("code"))
                f.write("\tconfig = %s\n" % button_node.getAttribute("key"))
                f.write("end\n")
    
            f.close()    
    @threaded
    def run(self):
  
       if self.config_file:

		x = XKeys()
		import pylirc
           
           #try:
	        if(pylirc.init("irkeys", self.config_file, 0)):
	           while True:
	
		           s = pylirc.nextcode(1)
		           if s:
			           for evt in s:
	
				           command = evt["config"]
				           print "IR recived :: " + command
				           x.SendKeyPress( command )
				           time.sleep(0.1)
				           x.SendKeyRelease( command )
				           
	           # clean up
	           #pylirc.exit()
           #except:
                #pass
                
    def __del__(self):
        import pylirc
        pylirc.exit()
        os.remove(self.config_file)
