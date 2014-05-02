#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple test for the DaguCar/iRacer API

A simple interface to control the car using the CV2 and Numpy libraries
"""

import cv2
import numpy as np

import sys
sys.path.append('./')
from DaguCar import DaguCar


class Main:
    def __init__(self):
        self._tps = cv2.getTickFrequency()
        self._imgH = 240
        self._imgW = 320
        self._zonaL = self._imgW/3
        self._zonaR = self._imgW/3*2
        self._zonaT = self._imgH/3
        self._zonaB = self._imgH/3*2
        self._speed = 0

    def _TBSpeed(self, speed):
        self._speed = speed

    def _DetectObject(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (0, 0), 5)
        circles = cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
                            param1=50, param2=40, minRadius=30, maxRadius=100)
        if(circles != None):
            c = circles[0][0]
            cv2.circle(img, (c[0], c[1]), c[2], (0,255,0), 1)
            cv2.circle(img, (c[0], c[1]), 2, (0,0,255),2)
            return img, (c[0], c[1])
        return img, None

    def Run(self, device, robot):
        # abrimos dispositivo de captura
        cap = cv2.VideoCapture(0)

        # establecemos dimensiones
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self._imgH)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self._imgW)

        # preparamos las ventanas
        cv2.namedWindow('Frames', cv2.CV_WINDOW_AUTOSIZE)
        cv2.createTrackbar('Speed', 'Frames', 0, 15, self._TBSpeed )

        # procesamos hasta que recibamos ESC
        useRobot = 0
        t1=cv2.getTickCount()
        while True:
            # capturamos un cuadro
            ret, img = cap.read()
            if(not ret):
                break

            # procesamos el cuadro
            img = cv2.flip(img,1)
            frame, center = self._DetectObject(img)

            # añadimos lineas de zonas
            cv2.line(frame, (self._zonaL,0), (self._zonaL, self._imgH),
                     (0,0,0), 1)
            cv2.line(frame, (self._zonaR,0), (self._zonaR, self._imgH),
                     (0,0,0), 1)
            cv2.line(frame, (0, self._zonaT), (self._imgW, self._zonaT),
                     (0,0,0), 1)
            cv2.line(frame, (0, self._zonaB), (self._imgW, self._zonaB),
                     (0,0,0), 1)

            # calculamos FPS y mostramos el frame procesado
            t2=cv2.getTickCount()
            cv2.putText(frame, "%04.2f FPS" % (1/((t2-t1)/self._tps)),
                        (10, self._imgH-10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,0,0))
            cv2.imshow('Frames', frame)
            t1=t2

            # control por teclado
            k = cv2.waitKey(5)
            if(k==27):
                break
            elif(k==115): # 's'
                if(useRobot):
                    robot.Stop()
                useRobot = ~useRobot

            # movemos el robot
            if(useRobot):
                if(center!=None):
                    x, y = center
                    if(x<self._zonaL):
                        if(y<self._zonaT):
                            robot.Move(DaguCar.CMD_LEFT_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            robot.Move(DaguCar.CMD_LEFT_BACKWARD, self._speed)
                        else:
                            robot.Move(DaguCar.CMD_LEFT, self._speed)
                    if(x>self._zonaR):
                        if(y<self._zonaT):
                            robot.Move(DaguCar.CMD_RIGHT_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            robot.Move(DaguCar.CMD_RIGHT_BACKWARD, self._speed)
                        else:
                            robot.Move(DaguCar.CMD_RIGHT, self._speed)
                    else:
                        if(y<self._zonaT):
                            robot.Move(DaguCar.CMD_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            robot.Move(DaguCar.CMD_BACKWARD, self._speed)
                        else:
                            robot.Move(DaguCar.CMD_STOP, self._speed)
                else:
                    robot.Stop()

        # eso es todo
        cap.release()
        cv2.destroyAllWindows()


def main():
    """main() for the application."""
    app = Main()
    robot = DaguCar("/dev/rfcomm1")
    app.Run(0, robot)


if __name__ == "__main__":
    main()
