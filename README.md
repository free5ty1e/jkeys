# jkeys
Automatically exported from code.google.com/p/jkeys


Translate joystick axis/buttons to xserver key pushes

Note: you will need to install python-xlib and python-pygame first

in ubuntu

sudo apt-get install python-xlib python-pygame


August 28th, 2008 #1 KillerKiwi's Avatar KillerKiwi  KillerKiwi is offline
Frothy Coffee!

Join Date
Jun 2005
Beans
188
Jkeys - simple joystick to keyboard mapping
Ok here's a little app I setup so I could use my mythbox with a gamepad and some games

A lot of linux games dont have joystick support so this little app will map you joystick buttons/axis to key presses

you run a game by going
Code:
jkeys example-config.joy armagetronad
where example-config.joy is a simple xml file with the key mappings like so
Code:
<config>
    <joystick id="0">
        <axis number="0" low="Left" high="Right" />
        <axis number="1" low="Down" high="Up" />
        <button number="0" key="Space" />
        <button number="1" key="Return" />
        <button number="2" key="a" />
        <button number="3" key="b" />
        <button number="4" key="c" />
        <button number="5" key="d" />
        <button number="6" key="z" />
        <button number="7" key="x" />
        <button number="9" key="Escape" />
        <button number="10" key="p" />
    </joystick>
</config>
It should allow for multi axis any number of buttons and mutliple joysticks etc, although its only been tested with my gamepad 
