#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        self.dc = None
        self.MoveButtons = self.builder.get_object("MoveButtons")
        self.Speed = self.builder.get_object("Speed")
        self.Speed.props.adjustment=self.builder.get_object("SpeedAdjustment")
        self.Port = self.builder.get_object("Port")
        self.Connect = self.builder.get_object("Connect")
        self.StatusBar = self.builder.get_object("StatusBar")
        self.SbContextId = self.StatusBar.get_context_id("MainMessages")
        self.TJoystick = None


    def OnDeleteWindow(self, *args):
        self.OnQuit(*args)


    def OnQuit(self, *args):
        self.Connect.set_active(False)
        Gtk.main_quit()
        

    def OnActive(self, *args):
        if(self.Connect.get_active()):
            self._SbSetMessage()
            self.dc = DaguCar(self.Port.get_text())
            if(self.dc!=None and self.dc.IsConnected()):
                self.MoveButtons.set_sensitive(True)
                self.Speed.set_sensitive(True)
                self.Port.set_sensitive(False)
                self.dc.SetSpeed(int(self.Speed.props.adjustment.get_value()))
                self._SbSetMessage("Conectado a %s" % (self.Port.get_text()))
                pygame.init()
                if(pygame.joystick.get_count()>0):
                    self.TJoystick = Thread(target=self._Joystick, args=())
                    self.TJoystick.start()
            else:
                self.Connect.set_active(False);
                self.dc = None
                self._SbSetMessage("Error al conectar")
        else:
            if(self.dc!=None):
                self.dc.Close()
                self.dc = None
                self.MoveButtons.set_sensitive(False)
                self.Speed.set_sensitive(False)
                self.Port.set_sensitive(True)
                self._SbSetMessage("Desconectado")
                if(self.TJoystick!=None):
                    self.TJoystick.join()
                    self.TJoystick = None
                pygame.quit()
        return
        

    def OnSpeedChanged(self, *args):
        self.dc.SetSpeed(int(self.Speed.props.adjustment.get_value()))
        

    def OnUp(self, *args):
        self.dc.Move(0, 1)
            

    def OnUpLeft(self, *args):
        self.dc.Move(-1, 1)
            

    def OnUpRight(self, *args):
        self.dc.Move(1, 1)
            

    def OnDown(self, *args):
        self.dc.Move(0, -1)
            

    def OnDownLeft(self, *args):
        self.dc.Move(-1, -1)
            

    def OnDownRight(self, *args):
        self.dc.Move(1, -1)
            

    def OnLeft(self, *args):
        self.dc.Move(-1,0)
            

    def OnRight(self, *args):
        self.dc.Move(1, 0)
            

    def OnStop(self, *args):
        self.dc.Move(0, 0)
        

    def _SbSetMessage(self, msg=None):
        self.StatusBar.pop(self.SbContextId)
        if(msg!=None):
            self.StatusBar.push(self.SbContextId, msg)


    def _Joystick(self, *args):
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        axes = [0]*joystick.get_numaxes()
        (_x, _y) = (0, 0)
        while(self.dc!=None):
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


if __name__=="__main__":
    app = Main()
    Gtk.main()
