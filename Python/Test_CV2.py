#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test simple para la API del DaguCar/iRacer

Una interface simple para controlar el auto utilizando las librerías
CV2 y Numpy a través de la detección de un círculo y el desplazamiento
de éste.
"""

import cv2
import numpy as np
from DaguCar import DaguCar


class MyApp:
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

    def Run(self, device, car):
        # abrimos dispositivo de captura
        cap = cv2.VideoCapture(0)

        # establecemos dimensiones
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self._imgH)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self._imgW)

        # preparamos las ventanas
        cv2.namedWindow('Frames', cv2.CV_WINDOW_AUTOSIZE)
        cv2.createTrackbar('Speed', 'Frames', 0, 15, self._TBSpeed )

        # procesamos hasta que recibamos ESC
        useCar = 0
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

            # ESC finaliza
            k = cv2.waitKey(5)
            if(k==27):
                break
            # La tecla S habilita/deshabilita el control del auto
            elif(k==115):
                if(useCar):
                    car.Stop()
                useCar = ~useCar

            # movemos el auto
            if(useCar):
                if(center!=None):
                    x, y = center
                    if(x<self._zonaL):
                        if(y<self._zonaT):
                            car.Move(DaguCar.CMD_LEFT_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            car.Move(DaguCar.CMD_LEFT_BACKWARD, self._speed)
                        else:
                            car.Move(DaguCar.CMD_LEFT, self._speed)
                    if(x>self._zonaR):
                        if(y<self._zonaT):
                            car.Move(DaguCar.CMD_RIGHT_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            car.Move(DaguCar.CMD_RIGHT_BACKWARD, self._speed)
                        else:
                            car.Move(DaguCar.CMD_RIGHT, self._speed)
                    else:
                        if(y<self._zonaT):
                            car.Move(DaguCar.CMD_FORWARD, self._speed)
                        elif(y>self._zonaB):
                            car.Move(DaguCar.CMD_BACKWARD, self._speed)
                        else:
                            car.Move(DaguCar.CMD_STOP, self._speed)
                else:
                    car.Stop()

        # eso es todo
        cap.release()
        cv2.destroyAllWindows()


def main():
    """main() de la aplicación."""
    app = MyApp()
    try:
        car = DaguCar("/dev/rfcomm1")
        app.Run(0, car)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
