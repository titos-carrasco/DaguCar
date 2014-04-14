# -*- coding: utf-8 -*-
"""Bluetooth control for the DaguCar/iRacer car.

Implements the commands required to control de DaguCar/iRacer car via
bluetooth.

You can read the spec in the "DaguCarCommands.pdf" file.

More info in https://www.sparkfun.com/products/11162
"""

import serial
import threading


class DaguCar:
    """Class to control the car

    Usage:
        car = DaguCar("/dev/rfcomm0")
        if(car.IsConnected()):
            car.Move(DaguCar.CMD_FORWARD, 15)
            time.sleep(1)
            car.Stop()
            car.Close()
    """
    def __init__(self, port):
        """Create the DaguCar/iRacer object and open a connection to the car.

        Args:
            port: The serial port to use (string)

        Raises:
            KeyboardInterrupt
        """
        self._lock = threading.Lock()
        self._ser = None
        self._lastCmd = 0x00
        for t in range(4):
            try:
                self._ser = serial.Serial(port, baudrate=9600, bytesize=8,
                                          parity='N', stopbits=1, timeout=1)
                self._Debug('DaguCar.Init: Connected to %s, 9600 bps' %
                            (port))
                break
            except serial.SerialException:
                self._Debug('DaguCar.Init: SerialException')
            except ValueError:
                self._Debug('DaguCar.Init: ValueError')
            except IOError:
                self._Debug('DaguCar.Init: IOError')
            except KeyboardInterrupt:
                self._Debug('DaguCar.Init: KeyboardInterrupt')
                raise

    def _Lock(self):
        """Get an exclusive access to the car."""
        self._lock.acquire()
        if(self._ser!=None and self._ser.isOpen()):
            return True
        else:
            self._lock.release()
            return False

    def _Unlock(self):
        """Release the exclusive access to the car."""
        try:
            self._lock.release()
        except:
            pass

    def _Debug(self, val):
        """Simple console debug."""
        print val

    def IsConnected(self):
        """True if connected to the car."""
        try:
            if(self._ser.isOpen()):
                return True
        except:
            pass
        return False

    def Close(self):
        """Close the connection to the car."""
        if(self._Lock()):
            self._ser.close()
            self._ser = None
            self._Unlock()

    # Commands for the car
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
        """Move the car

        Args:
            direction: The direction for the car (DaguCar.CMD_XXX)
            speed: 0 to 15
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
            except serial.SerialTimeoutException:
                self._Debug('DaguCar.Move: SerialTimeoutException')
                cmd = -1
            except serial.SerialException:
                self._Debug('DaguCar.Move: SerialException')
            except:
                self._Debug('DaguCar.Move: Unexpected Exception')
            self._Unlock()

    def Stop(self):
        """Stop the car."""
        self.Move(DaguCar.CMD_STOP, 0)
