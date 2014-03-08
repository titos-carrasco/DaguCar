#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import time

import sys
sys.path.append('./')
from DaguCar import DaguCar

def AddText(text, left, top):
	font = pygame.font.Font(None, 20)
	text = font.render(text, 1, (0, 0, 0))
	textpos = text.get_rect()
	textpos.left = left
	textpos.top  = top
	return text, textpos

def Main():
	pygame.init()
	if(pygame.joystick.get_count()<=0):
		print 'No Joystick detected: Aborting.'
		pygame.quit()
		return

	joystick = pygame.joystick.Joystick(0)
	joystick.init()

	buttons = [0]*joystick.get_numbuttons()
	axes = [0]*joystick.get_numaxes()

	screen = pygame.display.set_mode((320, 240))
	pygame.display.set_caption('DaguCar Test')
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0xff, 0xff, 0xff))
	background.blit(*AddText("Button 1: More speed", 10, 10))
	background.blit(*AddText("Button 3: Less speed", 10, 25))
	background.blit(*AddText("Button 5: Quit", 10, 40))

	speedUp = 0
	speedDown = 0

	dc = DaguCar('/dev/rfcomm0')
	if(not dc.IsConnected()):
		pygame.quit()
		return;

	while(True):
		pygame.event.pump()
		try:
			for i in range(len(buttons)):
				buttons[i] = joystick.get_button(i)

			if(buttons[4]==1):
				break
			elif(buttons[0]==1 and speedUp==0):
				speedUp = 1
			elif(buttons[0]==0 and speedUp==1):
				speedUp = 0
				dc.SetSpeed(dc.GetSpeed() + 1)
			elif(buttons[2]==1 and speedDown==0):
				speedDown = 1
			elif(buttons[2]==0 and speedDown==1):
				speedDown = 0
				dc.SetSpeed(dc.GetSpeed() - 1)

			for i in range(len(axes)):
				axes[i] = round(joystick.get_axis(i),0)

			(x, y) = (axes[0], -axes[1])
			dc.Move(x, y)

			background.fill(pygame.Color("white"), (0, 60, 320, 240))
			background.blit(*AddText("(x, y, speed) = (%d, %d, %d)" % (x, y, dc.GetSpeed()), 10, 60))

		except KeyboardInterrupt:
			break

		screen.blit(background, (0, 0))
		pygame.display.flip()

	dc.Close()
	pygame.quit()

# Show Time
Main()
