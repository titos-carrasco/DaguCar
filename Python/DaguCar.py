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


class DaguCar:
    """Clase para controlar el auto DaguCar/iRacer.

    Uso:
        try:
            car = DaguCar("/dev/rfcomm0")
        except:
            sys.exit(1)
        car.Move(DaguCar.CMD_FORWARD, 15)
        time.sleep(1)
        car.Stop()
        car.Close()

    """

    def __init__(self, port):
        """Crea el objeto DaguCar/iRacer y abre una comunicación serial.

        Args:
            port: La puerta serial a utilizar(string)

        Excepciones:
            Las generadas por serial.Serial() y otras de valor en los
            parámetros
        """
        self._lock = threading.Lock()
        self._ser = None
        self._lastCmd = 0x00
        for t in range(4):
            try:
                self._ser = serial.Serial(port, baudrate="9600", bytesize=8,
                                          parity='N', stopbits=1, timeout=1)
                self._Debug('DaguCar.Init: Conectado a %s, 9600 bps' %
                            (port))
                return
            except serial.SerialException:
                self._Debug('DaguCar.Init: SerialException (%d)' % (t + 1))
            except Exception as e:
                raise
        raise serial.SerialException

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
                self._Unlock()
                raise
            self._Unlock()

    def Stop(self):
        """Detiene el auto."""
        self.Move(DaguCar.CMD_STOP, 0)
