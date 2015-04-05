#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rcr.robots.dagucar.DaguCar import DaguCar

import cv2
import numpy as np

_tbData = {
    'H' : 0,
    'S' : 0,
    'V' : 0,
    'Area' : 300
    }

def procesaCuadro(img, imgH, imgW):
    global _tbData

    # minimizamos ruido
    blur = cv2.GaussianBlur(img, (9,9), 0)

    # trabajaremos en el espacio hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    # ajustamos umbral acorde a los trackbar
    h = cv2.threshold(h, _tbData['H'], 255, cv2.THRESH_BINARY)[1]
    s = cv2.threshold(s, _tbData['S'], 255, cv2.THRESH_BINARY)[1]
    v = cv2.threshold(v, _tbData['V'], 255, cv2.THRESH_BINARY)[1]

    # mostramos las ventanas h,s,v
    cv2.imshow('H', h)
    cv2.imshow('S', s)
    cv2.imshow('V', v)

    # aplicamos umbral y otros filtros
    objs = h & s & v
    objs = cv2.erode(objs, None, iterations=5)
    objs = cv2.dilate(objs, None, iterations=10)
    canny = cv2.Canny(objs, 15, 15*3)

    # buscamos y trazamos los contornos
    contours = cv2.findContours(canny, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    objs = cv2.cvtColor(objs, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(objs, contours, -1, (0,0,255), 2)
    cv2.imshow('Mask', objs)

    # buscamos el contorno de mayor área
    contour = (None, 0)
    for cnt in contours:
        #moments = cv2.moments(cnt)
        #area = cv2.contourArea(cnt)
        #perimeter = cv2.arcLength(cnt,True)
        #approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
        #hull = cv2.convexHull(cnt)
        area = cv2.contourArea(cnt)
        if(area>contour[1] and area>_tbData['Area']):
            contour = (cnt, area)

    # dibujamos el mayor de los contornos
    frame = img.copy()
    if(contour[0]!=None):
        (x,y),radius = cv2.minEnclosingCircle(contour[0])
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(frame,center,radius,(0,255,0),1)
        cv2.circle(frame,center,2,(0,0,255),2)
        return frame, center
    else:
        return frame, None


def tbHUmbral(nivel):
    global _tbData
    _tbData['H'] = nivel


def tbSUmbral(nivel):
    global _tbData
    _tbData['S'] = nivel


def tbVUmbral(nivel):
    global _tbData
    _tbData['V'] = nivel


def tbArea(nivel):
    global _tbData
    _tbData['Area'] = nivel


def main(rob):
    # ticks por segundos
    tps = cv2.getTickFrequency()

    # abrimos dispositivo de captura
    device = 0
    cap = cv2.VideoCapture(device)

    # establecemos dimensiones
    imgH,imgW = 240, 320
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, imgH)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, imgW)

    # preparamos las ventanas
    cv2.namedWindow('Frames', cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow('H', cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow('S', cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow('V', cv2.CV_WINDOW_AUTOSIZE)
    cv2.namedWindow('Mask', cv2.CV_WINDOW_AUTOSIZE)

    # preparamos las barras de umbral
    cv2.createTrackbar('H Mask', 'H', 0, 255, tbHUmbral )
    cv2.createTrackbar('S Mask', 'S', 0, 255, tbSUmbral )
    cv2.createTrackbar('V Mask', 'V', 0, 255, tbVUmbral )
    cv2.createTrackbar('Area', 'Frames', 300, 5000, tbArea )

    # init interno
    robUsar = False
    robEstado = 'S'
    zonaL = imgW/3
    zonaR = imgW/3*2

    # procesamos hasta que recibamos ESC
    t1=cv2.getTickCount()
    while True:
        # capturamos un cuadro
        ret, img = cap.read()
        if(not ret):
            break

        # procesamos el cuadro
        img = cv2.flip(img,1)
        frame, center = procesaCuadro(img, imgH, imgW)

        # añadimos lineas de zonas
        cv2.line(frame, (zonaL,0), (zonaL,imgH), (0,0,0), 1)
        cv2.line(frame, (zonaR,0), (zonaR,imgH), (0,0,0), 1)

        # calculamos FPS y mostramos el frame procesado
        t2=cv2.getTickCount()
        cv2.putText(frame, "%04.2f FPS" % (1/((t2-t1)/tps)), (10, imgH-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
        cv2.imshow('Frames', frame)
        t1=t2

        # movemos el robot
        if(robUsar and center<>None):
            if(center[0]<=zonaL):
                if(robEstado<>'L'):
                    rob.MoveLeft( 15 )
                    robEstado='L'
            elif(center[0]>=zonaR):
                if(robEstado<>'R'):
                    rob.MoveRight( 15 )
                    robEstado='R'
            else:
                if(robEstado<>'S'):
                    rob.Stop()
                    robEstado='S'

        # control por teclado
        k = cv2.waitKey(5)

        # esc para abortar
        if(k==27):
            if(robEstado <> 'S'):
                rob.SetMotors(0, 0)
            break
        # r: inicia control del robot
        elif(k==114):
            robUsar = True
        # s: libera control del robot
        elif(k==115):
            if(robEstado<>'S'):
                rob.stop()
                robEstado = 'S'
            robUsar = False

    cap.release()
    cv2.destroyAllWindows()


# Show time
print( "1. Desplazar las 5 ventanas para visualizarlas" )
print( "2. Colocar un objeto circular de un sólo color frente a la cámara" )
print( "3. Desplazar el slider de las ventana HSV tal que el objeto se vea blanco en cada una de ellas" )
print( "4. Continuar moviendo los sliders hasta que el objeto circular sea el único que se ve en Mask" )
print( "5. En la ventana Frames posicionar el objeto en el centro" )
print( "6. Presionar la tecla R y mover el objeto hacia los extremos: el robot se moverá" )
print( "7. Presionar la tecla S para detenerlo" )
print( "8. Presionar ESC para finalizar" )

rob = DaguCar( "/dev/rfcomm1", 500 )
main(rob)
