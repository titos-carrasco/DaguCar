#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DaguCar import DaguCar

def main():
    try:
        car = DaguCar("/dev/rfcomm1")
    except Exception as e:
        print(e)
        return
    print "¿Conectado?:", car.IsConnected()
    car.Move(DaguCar.CMD_FORWARD, 15)
    car.Wait(3000)
    car.Move(DaguCar.CMD_BACKWARD, 15)
    car.Wait(3000)
    car.Stop()
    car.Close()
###
main()
