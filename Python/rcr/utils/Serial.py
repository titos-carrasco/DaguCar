# -*- coding: utf-8 -*-

import serial
import threading
import time

class Serial:
    def __init__( self, port, bauds, timeout ):
        REAL_TIMEOUT = 1.0
        USER_TIMEOUT = timeout
        self._TRIES = USER_TIMEOUT / REAL_TIMEOUT
        self._lock = threading.Lock()
        try:
            self._ser = serial.Serial(port, baudrate=bauds, bytesize=8,
                                     parity='N', stopbits=1,
                                     timeout=REAL_TIMEOUT / 1000.0 )
            self._ser.flushInput()
            self._ser.flushOutput()
        except Exception as e:
            raise

    def Close( self ):
        try:
            self._Lock()
            self._ser.close()
            self._ser = None
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def Write( self, bytes ):
        try:
            self._Lock()
            self._ser.write( bytes )
            self._ser.flush()
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def ReadLine( self, maxLen ):
        try:
            self._Lock()
            bytes = ''
            pos = 0
            tries = 0
            while( pos < maxLen + 1 and tries < self._TRIES ):
                b = self._ser.read(1)
                if( b == '' ):
                    tries = tries + 1
                    continue
                if( b == "\n" ):
                    return bytes
                bytes = bytes + b
                tries = 0
            raise serial.SerialTimeoutException
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def Read( self, nbytes ):
        try:
            self._Lock()
            bytes = bytearray( nbytes )
            pos = 0
            tries = 0
            while( pos < nbytes and tries < self._TRIES ):
                b = self._ser.read(1)
                if( b == '' ):
                    tries = tries + 1
                    continue
                bytes[ pos ] = b
                pos = pos + 1
                tries = 0
            if( pos < nbytes ):
                raise serial.SerialTimeoutException
            return bytes
        except Exception as e:
            raise
        finally:
            self._Unlock()

    def FlushRead( self, timex ):
        t1 = time.time()
        t2 = t1
        while( t2 -t1 <= timex ):
            try:
                self._ser.read(1)
            except:
                pass
            t2 = time.time()

    def Read1UByte( self ):
        b = self.Read(1)
        return b[0] & 0xFF

    def Read2UBytes( self ):
        b = self.Read(2)
        n = b[0] & 0x000000FF;
        n = ( n<<8 ) | ( b[1] & 0xFF )
        return n

    def Read4UBytes( self ):
        b = self.Read(4)
        n = b[0] & 0x000000FF
        n = ( n << 8 ) | ( b[1] & 0xFF )
        n = ( n << 8 ) | ( b[2] & 0xFF )
        n = ( n << 8 ) | ( b[3] & 0xFF )
        if( ( n & 0x80000000 ) != 0 ):
            return n - 0xFFFFFFFF -1
        else:
            return n;

    def Read4Bytes(self):
        n = self.Read4UBytes();
        return int( n )

    def Pause( self, ms ):
        time.sleep(ms/1000.0)

    #### Privadas

    def _Lock( self ):
        """Obtiene acceso exclusivo."""
        self._lock.acquire()

    def _Unlock( self ):
        """Libera el acceso exclusivo."""
        self._lock.release()
