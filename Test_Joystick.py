#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple test for the DaguCar/iRacer API

A simple GUI (Glade) + Joystick to control the DaguCar/iRacer car.
We use a thread to read the joystick
"""

from gi.repository import Gtk
from threading import Thread
import pygame
import time

import sys
sys.path.append('./')
from DaguCar import DaguCar


class Main:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Resources/DaguCar.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")
        self.window.show_all()
        self.car = None
        self.MoveButtons = self.builder.get_object("MoveButtons")
        self.Speed = self.builder.get_object("Speed")
        self.Speed.props.adjustment=self.builder.get_object("SpeedAdjustment")
        self.SpeedValue = int(self.Speed.props.adjustment.get_value())
        self.Port = self.builder.get_object("Port")
        self.Connect = self.builder.get_object("Connect")
        self.StatusBar = self.builder.get_object("StatusBar")
        self.SbContextId = self.StatusBar.get_context_id("MainMessages")
        self.TJoystick = None

    def OnDeleteWindow(self, *args):
        """Process the Delete Window event."""
        self.OnQuit(*args)

    def OnQuit(self, *args):
        """Process the Quit event."""
        self.Connect.set_active(False)
        Gtk.main_quit()

    def OnActive(self, *args):
        """Process the On/Off event."""
        if(self.Connect.get_active()):
            self._SbSetMessage()
            self.car = DaguCar(self.Port.get_text())
            if(self.car.IsConnected()):
                self.MoveButtons.set_sensitive(True)
                self.Speed.set_sensitive(True)
                self.Port.set_sensitive(False)
                self._SbSetMessage("Conectado a %s" % (self.Port.get_text()))
                pygame.init()

                # start the Joystock thread
                if(pygame.joystick.get_count()>0):
                    self.TJoystick = Thread(target=self._Joystick, args=())
                    self.TJoystick.start()
            else:
                self.Connect.set_active(False);
                self.car = None
                self._SbSetMessage("Error al conectar")
        else:
            if(self.car!=None):
                self.car.Close()
                self.car = None
                self.MoveButtons.set_sensitive(False)
                self.Speed.set_sensitive(False)
                self.Port.set_sensitive(True)
                self._SbSetMessage("Desconectado")

                # stop the joystick thread
                if(self.TJoystick!=None):
                    self.TJoystick.join()
                    self.TJoystick = None
                pygame.quit()
        return

    def OnSpeedChanged(self, *args):
        """Process the speed change event."""
        self.SpeedValue = int(self.Speed.props.adjustment.get_value())

    def OnUp(self, *args):
        """Process the Up event."""
        self.car.Move(DaguCar.CMD_FORWARD, self.SpeedValue)

    def OnUpLeft(self, *args):
        """Process the Up Left event."""
        self.car.Move(DaguCar.CMD_LEFT_FORWARD, self.SpeedValue)

    def OnUpRight(self, *args):
        """Process the Up Right event."""
        self.car.Move(DaguCar.CMD_RIGHT_FORWARD, self.SpeedValue)

    def OnDown(self, *args):
        """Process the Down event."""
        self.car.Move(DaguCar.CMD_BACKWARD, -self.SpeedValue)

    def OnDownLeft(self, *args):
        """Process the Down Right event."""
        self.car.Move(DaguCar.CMD_LEFT_BACKWARD, self.SpeedValue)

    def OnDownRight(self, *args):
        """Process the Down Right event."""
        self.car.Move(DaguCar.CMD_RIGHT_BACKWARD, self.SpeedValue)

    def OnLeft(self, *args):
        """Process the Left event."""
        self.car.Move(DaguCar.CMD_LEFT,self.SpeedValue)

    def OnRight(self, *args):
        """Process the Right event."""
        self.car.Move(DaguCar.CMD_RIGHT, self.SpeedValue)

    def OnStop(self, *args):
        """Process the Release Buttons events."""
        self.car.Stop()

    def _SbSetMessage(self, msg=None):
        """Put a message in the status bar."""
        self.StatusBar.pop(self.SbContextId)
        if(msg!=None):
            self.StatusBar.push(self.SbContextId, msg)

    def _Joystick(self, *args):
        """Thread to process the joystick events."""
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        axes = [0]*joystick.get_numaxes()
        (_x, _y) = (0, 0)

        # process while the object exists
        while(self.car!=None):
            try:
                pygame.event.pump()
                for i in range(len(axes)):
                    axes[i] = round(joystick.get_axis(i),0)
                (x, y) = (axes[0], -axes[1])
                if((_x, _y)!=(x, y)):
                    (_x, _y) = (x, y)
                    if(x==0 and y==1):
                        self.OnUp();
                    elif(x==0 and y==-1):
                        self.OnDown();
                    elif(x==-1 and y==1):
                        self.OnUpLeft();
                    elif(x==1 and y==1):
                        self.OnUpRight();
                    elif(x==-1 and y==-1):
                        self.OnDownLeft();
                    elif(x==1 and y==-1):
                        self.OnDownRight();
                    elif(x==-1 and y==0):
                        self.OnLeft();
                    elif(x==1 and y==0):
                        self.OnRight();
                    else:
                        self.OnStop()
                time.sleep(0.1)
            except:
                break


def main():
    """main() for the application."""
    app = Main()
    Gtk.main()

if __name__ == "__main__":
    main()
