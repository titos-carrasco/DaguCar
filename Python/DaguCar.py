# -*- coding: utf-8 -*-
"""Clase para controlar el auto DaguCar/iRacer vía bluetooth.

Implementa los comandos requeridos para controlar el auto DaguCar/iRacer vía
bluetooth.

Las especificaciones pueden ser encontradas el archivo "DaguCarCommands.pdf".

Mayor información se puede encontrar en
https://www.sparkfun.com/products/11162
"""

import serial
import threading
import time

class DaguCar:
    """Clase para controlar el auto DaguCar/iRacer.

    Uso:
        from DaguCar import DaguCar
        try:
            car = DaguCar("/dev/rfcomm1")
        except Exception as e:
            print(e)
            sys.exit(1)
        car.Move(DaguCar.CMD_FORWARD, 15)
        car.Wait(1000)
        car.Stop()
        car.Close()

    """
    # Comandos para el auto
    CMD_STOP = 0
    CMD_FORWARD = 1
    CMD_BACKWARD = 2
    CMD_LEFT = 3
    CMD_RIGHT = 4
    CMD_LEFT_FORWARD = 5
    CMD_RIGHT_FORWARD = 6
    CMD_LEFT_BACKWARD = 7
    CMD_RIGHT_BACKWARD = 8

    def __init__(self, port, bauds=9600, timeout=3):
        """Crea el objeto DaguCar/iRacer y abre una comunicación serial.
        La pausa de 4 segundos es requerida para que se estabilice

        Args:
            port: La puerta serial a utilizar (string)
            bauds: La velocidad de la conexión (9600)
            timeout: El tiempo de espera por la conexión (3 segundos)

        Excepciones:
            Las generadas por serial.Serial() y otras de valor en los
            parámetros
        """
        self._lock = threading.Lock()
        self._ser = None
        self._lastCmd = 0x00
        for t in range(10):
            try:
                self._ser = serial.Serial(port, baudrate=bauds, bytesize=8,
                                          parity='N', stopbits=1, timeout=timeout)
                self._Debug('DaguCar.Init: Conectado en %s a %d bps' %
                            (port, bauds))
                self.Wait(4000)
                return
            except serial.SerialException as e:
                self._Debug(e)
                self._Debug('DaguCar.Init: SerialException (%d)' % (t + 1))
            except Exception as e:
                self._Debug(e)
                self._Debug('DaguCar.Init: Error no considerado')
                raise
        raise serial.SerialException("DaguCar.Init: No es posible establecer la conexión")

    def _Lock(self):
        """Obtiene acceso exclusivo al auto."""
        self._lock.acquire()
        if(self._ser!=None and self._ser.isOpen()):
            return True
        else:
            self._lock.release()
            return False

    def _Unlock(self):
        """Libera el acceso exclusivo al auto."""
        try:
            self._lock.release()
        except Exception as e:
            pass

    def _Debug(self, val):
        """Debug simple para consola."""
        print(val)

    def IsConnected(self):
        """True si estamos conectados al auto."""
        try:
            if(self._ser.isOpen()):
                return True
        except Exception as e:
            pass
        return False

    def Close(self):
        """Cerramos la conexión al auto."""
        if(self._Lock()):
            self._ser.close()
            self._ser = None
            self._Unlock()

    def Wait(self, ms):
        time.sleep(ms/1000.0)

    def Move(self, direction, speed):
        """Mueve el auto.

        Args:
            direction: La dirección del auto (DaguCar.CMD_XXX)
            speed: 0 a 15

        Excepciones:
            Generadas principalmente por serial.write()
        """
        if(self._Lock()):
            try:
                direction = int(direction)
                if(direction<0 or direction>8):
                    direction = 0
                direction = direction << 4
                speed = abs(int(speed)) & 0x0F
                cmd = direction | speed
                if(cmd!=self._lastCmd):
                    self._ser.write(chr(cmd))
                    self._lastCmd=cmd
            except Exception as e:
                self._Debug(e)
                self._Unlock()
                raise
            self._Unlock()

    def Stop(self):
        """Detiene el auto."""
        self.Move(DaguCar.CMD_STOP, 0)
