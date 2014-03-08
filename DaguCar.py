#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import threading

class DaguCar:
	def __init__(self, port, bauds=9600):
		self.lock = threading.Lock()
		self.ser = None
		self.speed = 0x07
		self.lastCmd = 0x00
		for t in range(4):
			try:
				self.ser = serial.Serial(port, baudrate=bauds, bytesize=8, parity='N', stopbits=1, timeout=1)
				self._Debug('DaguCar.Init: Conectado en %s a %d bps' % (port, bauds))
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
		self.lock.acquire()


	def _Unlock(self):
		self.lock.release()


	def _Debug(self, val):
		print val


	def IsConnected(self):
		if(self.ser==None):
			return False
		else:
			return self.ser.isOpen()


	def Close(self):
		if(not self.IsConnected()):
			return

		self._Lock()
		self.ser.close()
		self.ser = None
		self._Unlock()
		self.lock = None


	def SetSpeed(self, speed):
		if(not self.IsConnected()):
			return -1

		self._Lock()
		if(speed>= 0 and speed<=0x0F):
			self.speed = speed
		r = self.speed
		self._Unlock()
		return r


	def GetSpeed(self):
		if(not self.IsConnected()):
			return -1

		self._Lock()
		r = self.speed
		self._Unlock()
		return r


	def Move(self, x, y):
		if(not self.IsConnected()):
			return

		self._Lock()
		try:
			if(x==0 and y>0):
				cmd = 0x10 | self.speed
			elif(x==0 and y<0):
				cmd = 0x20 | self.speed
			elif(x<0 and y==0):
				cmd = 0x30 | self.speed
			elif(x>0 and y==0):
				cmd = 0x40 | self.speed
			elif(x<0 and y>0):
				cmd = 0x50 | self.speed
			elif(x>0 and y>0):
				cmd = 0x60 | self.speed
			elif(x<0 and y<0):
				cmd = 0x70 | self.speed
			elif(x>0 and y<0):
				cmd = 0x80 | self.speed
			else:
				cmd = 0x00

			if(cmd!=self.lastCmd):
				self.ser.write(chr(cmd))
				self.lastCmd=cmd
		except serial.SerialTimeoutException:
			self._Debug('DaguCar.Move: SerialTimeoutException')
			cmd = -1
		except serial.SerialException:
			self._Debug('DaguCar.Move: SerialException')
			cmd = -1
		finally:
			self._Unlock()
		return cmd
