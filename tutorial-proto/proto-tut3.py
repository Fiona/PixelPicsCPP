#!/usr/bin/python2

import pygame
import os
import sys
import time
from collections import namedtuple
from pygame.locals import *

TS = 50
SW = 800
SH = 600

Click = namedtuple("Click","right pos")


def await_input():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				sys.exit(0)
			elif event.type == MOUSEBUTTONUP and event.button in (1,3):
				return Click(event.button==3,event.pos)			
		time.sleep(0.017)

		
def draw_background():
	screen.fill((0,128,128))
	
		
def draw_unknown(i):
	size = len(levels[level][1])
	pygame.draw.rect(screen,(0,0,0),(SW/2-size*TS/2+i*TS,SH/2-TS/2,TS,TS),1)
	
		
def draw_filled(i,colour):
	size = len(levels[level][1])
	pygame.draw.rect(screen,colour,(SW/2-size*TS/2+i*TS,SH/2-TS/2,TS,TS),0)

	
def draw_empty(i,colour):
	size = len(levels[level][1])
	left,top = SW/2-size*TS/2+i*TS, SH/2-TS/2
	pygame.draw.rect(screen,colour,(left,top,TS,TS),1)
	pygame.draw.line(screen,colour,(left,top),(left+TS,top+TS),2)
	pygame.draw.line(screen,colour,(left,top+TS),(left+TS,top),2)
	

def draw_board(highlight=set(),hknown=False):
	size = len(levels[level][1])
	numclues = len(levels[level][0])
	pygame.draw.rect(screen,(255,255,255),(SW/2-size*TS/2,SH/2-TS/2,TS*size,TS))
	for n,c in enumerate(levels[level][0]):
		screen.blit(font.render(str(c),False,(0,0,0)),(SW/2-size*TS/2-numclues*TS+n*TS,SH/2))
	for i in range(size):
		filled,known = levels[level][1][i]
		if filled is None or not known:
			draw_unknown(i)
		elif filled is True:
			draw_filled(i,(0,0,0))
		else:
			draw_empty(i,(0,0,0))
	

def draw_text(*lines):
	for i,line in enumerate(lines):
		screen.blit(font.render(line,False,(0,0,128)),(0,32*i))


def render():
	pygame.display.flip()


def clicked_square(pos):
	size = len(levels[level][1])
	if not (SW/2-size*TS/2 <= pos[0] < SW/2+size*TS/2 and SH/2-TS/2 <= pos[1] < SH/2+TS/2): return -1
	return (pos[0]-(SW/2-size*TS/2))/TS


def stage(*text):
	draw_background()
	draw_board()
	draw_text(*text)
	render()
	return await_input()

					
def challenge():
	while True:
		if all([c[1] for c in levels[level][1]]): break
		clk = stage(*levels[level][2])
		sq = clicked_square(clk.pos)
		if sq == -1:
			stage("You must click on the board",
				"[click]")
		elif levels[level][1][sq][1]:
			stage("That square is already completed",
				"[click]")
		elif levels[level][1][sq][0] != clk.right:
			stage("That's incorrect.",
				"Use the RIGHT mouse button to mark squares filled.",
				"Use the LEFT mouse button to mark squares empty.",
				"[click]")
		else:
			levels[level][1][sq] = (levels[level][1][sq][0],True)
			
			
def fade_out():
	for i in range(30):
		draw_background()
		draw_board()
		pygame.draw.rect(screen,(0,0,0),(0,0,int(SW/30.0*i),SH))
		render()
		time.sleep(0.017)
	
	
def fade_in():
	for i in range(30):
		draw_background()
		draw_board()
		pygame.draw.rect(screen,(0,0,0),(0,0,int(SW/30.0*(30-i)),SH))
		render()
		time.sleep(0.017)
			

F = (True,True)
f = (True,False)
X = (False,True)
x = (False,False)
_ = (None,True)
	
pygame.init()
screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Tutorial")
font = pygame.font.Font(None,32)
bigfont = pygame.font.Font(None,96)

level = 0
levels = [
	[[5],[f,f,f,f,f],[]], # just fill
	[[3],[X,f,f,f,X],[]], # fill with empties present
	[[2],[x,X,F,F,X],[]], # mark an empty
	[[4],[F,F,F,f,x],[]], # mark a filled and an empty
	[[1,2],[f,X,X,f,f],[]], # fill 2 groups
	[[2,1],[x,f,F,X,f],[]], # fill 2 obscured groups
	[[1,3],[f,x,f,f,f],[]], # groups in order, only fits one way
	[[1,1,1],[x,F,x,x,F,x,F,x],[]], # marking the empties when complete
	[[0],[x,x,x,x,x],[]], # no groups
	[[2,1],[f,F,X,_,_],[]], # not knowing position of a group
	[[1,1],[_,x,F,x,_,_],[]], # putting empties on either side
	[[1,3],[_,_,_,_,X,f,f,f],[]], # deducing by available space
	[[4],[_,f,f,f,_],[]], # overlap
	[[3],[_,_,f,_,_],[]], # smaller overlap
	[[2],[_,F,_,x,x],[]], # empty beyond overlap
	[[1,3],[_,_,_,f,F,_],[]], # counting from the edge
	[[1,3],[_,_,x,F,f,F,x],[]], # connecting blocks
	[[2,2],[x,f,F,x,F,f,x],[]], # splitting blocks
]

while level < len(levels):
	fade_in()
	challenge()
	fade_out()
	level += 1
