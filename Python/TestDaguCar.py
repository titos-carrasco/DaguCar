#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rcr.robots.dagucar.DaguCar import DaguCar

def main():
    car = DaguCar( "/dev/rfcomm1", 500 )
    car.MoveForward( 15 )
    car.Pause( 1000 )
    car.MoveBackward( 15 )
    car.Pause( 1000 )
    car.MoveLeft( 15 )
    car.Pause( 1000 )
    car.MoveRight( 15 )
    car.Pause( 1000 )
    car.MoveForwardLeft( 15 )
    car.Pause( 1000 )
    car.MoveForwardRight( 15 )
    car.Pause( 1000 )
    car.MoveBackwardLeft( 15 )
    car.Pause( 1000 )
    car.MoveBackwardRight( 15 )
    car.Pause( 1000 )
    car.Stop()
    car.Close()

###
main()
