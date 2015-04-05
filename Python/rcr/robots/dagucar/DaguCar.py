# -*- coding: utf-8 -*-

from rcr.utils.Serial import Serial

import threading
import time

class DaguCar:
    CMD_STOP           = 0
    CMD_FORWARD        = 1
    CMD_BACKWARD       = 2
    CMD_LEFT           = 3
    CMD_RIGHT          = 4
    CMD_FORWARD_LEFT   = 5
    CMD_FORWARD_RIGHT  = 6
    CMD_BACKWARD_LEFT  = 7
    CMD_BACKWARD_RIGHT = 8

    def __init__( self, port, timeout ):
        self._lastCmd = -1
        self._lock = threading.Lock()
        for i in range( 20 ):
            try:
                self._ser = Serial(port, 9600, timeout)
                self.Pause( 1000 )
                self._ser.FlushRead( 2.0 )
                return
            except Exception as e:
                if( i > 10 ):
                    raise

    def Close( self ):
        try:
            self._Lock()
            self._ser.Close()
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def Pause( self, ms ):
        self._ser.Pause( ms )

    ###
    # Comandos para el auto
    ###


    def Stop( self ):
        try:
            self._Lock()
            self._Move( self.CMD_STOP, 0x00 )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveForward( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_FORWARD, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveBackward( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_BACKWARD, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveLeft( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_LEFT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveRight( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_RIGHT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveForwardLeft( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_FORWARD_LEFT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveForwardRight( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_FORWARD_RIGHT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveBackwardLeft( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_BACKWARD_LEFT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def MoveBackwardRight( self, speed ):
        try:
            self._Lock()
            self._Move( self.CMD_BACKWARD_RIGHT, speed & 0x0F )
        except Exception as e:
            raise
        finally:
            self._Unlock()

    ###
    # métodos privados
    ###

    def _Debug( self, val ):
        print(val)

    def _Move( self, direction, speed ):
        if( direction < self.CMD_STOP or direction > self.CMD_BACKWARD_RIGHT ):
            direction = self.CMD_STOP
        speed = speed & 0x0F

        cmd = ( direction<<4 ) | speed
        if( cmd != self._lastCmd ):
            packet = bytearray( 1 )
            packet[0] = cmd
            self._ser.Write( packet )
            self._lastCmd = cmd

    def _Lock( self ):
        """Obtiene acceso exclusivo."""
        self._lock.acquire()

    def _Unlock( self ):
        """Libera el acceso exclusivo."""
        self._lock.release()
