#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test simple para la API del DaguCar/iRacer

GUI desarrollada en Glade3 para controlar con joystick y teclado
el auto DaguCar/iRacer.

Utilizamos un hilo para procesar el joystick.
"""

from gi.repository import Gtk
from threading import Thread
import pygame
import time
from DaguCar import DaguCar


class MyApp:
    def __init__(self):
        """Construye la GUI desde el archivo glade"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Resources/GUI.glade")
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
        """Procesa el evento de cerrar ventana - Delete Window."""
        self.OnQuit(*args)

    def OnQuit(self, *args):
        """Procesa el evento de salir - Quit."""
        self.Connect.set_active(False)
        Gtk.main_quit()

    def OnActive(self, *args):
        """Procesa el evento OnActive del boton On/Off tipo switch."""
        if(self.Connect.get_active()):
            self._SbSetMessage("Conectando...")
            try:
                self.car = DaguCar(self.Port.get_text())
            except Exception as e:
                self.Connect.set_active(False)
                self._SbSetMessage("Error al conectar...")
                return
            self.MoveButtons.set_sensitive(True)
            self.Speed.set_sensitive(True)
            self.Port.set_sensitive(False)
            self.Connect.set_label("Desconectar")
            self._SbSetMessage("Conectado a %s" % (self.Port.get_text()))

            # Inicia el hilo del joystick
            pygame.init()
            if(pygame.joystick.get_count()>0):
                self.TJoystick = Thread(target=self._Joystick, args=())
                self.TJoystick.start()
        else:
            if(self.car!=None):
                self.car.Close()
                self.car = None
                self.MoveButtons.set_sensitive(False)
                self.Speed.set_sensitive(False)
                self.Port.set_sensitive(True)
                self.Connect.set_label("Conectar")
                self._SbSetMessage("Desconectado...")

                # stop the joystick thread
                if(self.TJoystick!=None):
                    self.TJoystick.join()
                    self.TJoystick = None
                pygame.quit()

    def OnSpeedChanged(self, *args):
        """Procesa el evento de cambio de velocidad - SpeedChange."""
        self.SpeedValue = int(self.Speed.props.adjustment.get_value())

    def OnUp(self, *args):
        """Procesa el evento de avanzar - Up."""
        self.car.Move(DaguCar.CMD_FORWARD, self.SpeedValue)

    def OnUpLeft(self, *args):
        """Procesa el evento avanzar izquierda - UpLeft."""
        self.car.Move(DaguCar.CMD_LEFT_FORWARD, self.SpeedValue)

    def OnUpRight(self, *args):
        """Procesa el evento de avanzar derecha - UpRight."""
        self.car.Move(DaguCar.CMD_RIGHT_FORWARD, self.SpeedValue)

    def OnDown(self, *args):
        """Procesa el evento de retroceder - Down."""
        self.car.Move(DaguCar.CMD_BACKWARD, -self.SpeedValue)

    def OnDownLeft(self, *args):
        """Procesa el evento de retroceder izquierda - DownLeft."""
        self.car.Move(DaguCar.CMD_LEFT_BACKWARD, self.SpeedValue)

    def OnDownRight(self, *args):
        """Procesa el evento de retroceder derecha - DownRight."""
        self.car.Move(DaguCar.CMD_RIGHT_BACKWARD, self.SpeedValue)

    def OnLeft(self, *args):
        """Procesa el evento mover izquierda - Left."""
        self.car.Move(DaguCar.CMD_LEFT,self.SpeedValue)

    def OnRight(self, *args):
        """Procesa el evento de mover derecha - Right."""
        self.car.Move(DaguCar.CMD_RIGHT, self.SpeedValue)

    def OnStop(self, *args):
        """Procesa el evento de detener - Stop."""
        self.car.Stop()

    def _SbSetMessage(self, msg=None):
        """Coloca un mensaje en la barra de estado."""
        self.StatusBar.pop(self.SbContextId)
        if(msg!=None):
            self.StatusBar.push(self.SbContextId, msg)

    def _Joystick(self, *args):
        """Hilo que procesa los eventos del joystick."""
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        axes = [0]*joystick.get_numaxes()
        (_x, _y) = (0, 0)

        # procesa mientras el objeto del auto exista
        while(self.car!=None):
            try:
                events = pygame.event.get()
                for event in events:
                    if(event.type == pygame.JOYAXISMOTION and event.joy == 0):
                        axes[event.axis] = int(round(event.value, 0))
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
    """main() para la aplicación."""
    app = MyApp()
    Gtk.main()

if __name__ == "__main__":
    main()
