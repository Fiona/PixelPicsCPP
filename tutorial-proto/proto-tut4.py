#!/usr/bin/python2

import pygame
import os
import sys
import time
from collections import namedtuple
from pygame.locals import *

TS = 75
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
		time.sleep(0.17)

		
def draw_background():
	screen.fill((0,128,128))
	
		
def draw_unknown(i,j):
	pygame.draw.rect(screen,(0,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),1)
	
		
def draw_filled(i,j,colour):
	pygame.draw.rect(screen,colour,(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),0)
	
	
def draw_empty(i,j,colour):
	pygame.draw.rect(screen,colour,(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),1)
	pygame.draw.line(screen,colour,(SW-5*TS+i*TS,SH-5*TS+j*TS),(SW-5*TS+i*TS+TS,SH-5*TS+j*TS+TS),2)
	pygame.draw.line(screen,colour,(SW-5*TS+i*TS+TS,SH-5*TS+j*TS),(SW-5*TS+i*TS,SH-5*TS+j*TS+TS),2)

	
def draw_highlight(i,j):
	pygame.draw.rect(screen,(255,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),3)


def draw_question(i,j,colour):
	pygame.draw.rect(screen,colour,(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),1)
	screen.blit(bigfont.render("?",False,colour),(SW-5*TS+i*TS,SH-5*TS+j*TS))
		
		
def draw_board(highlight=set(),hknown=False):
	pygame.draw.rect(screen,(255,255,255),(SW-5*TS,SH-5*TS,5*TS,5*TS))
	# col clues
	for i in range(5):
		for n,c in enumerate(reversed(clues[0][i])):
			screen.blit(font.render(str(c),False,(0,0,0)),(SW-5*TS+i*TS+TS/2,SH-5*TS-(n+1)*TS/2))
		if (i,-1) in highlight:
			draw_highlight(i,-1)
	# row clues
	for j in range(5):
		for n,c in enumerate(reversed(clues[1][j])):
			screen.blit(font.render(str(c),False,(0,0,0)),(SW-5*TS-(n+1)*TS/2,SH-5*TS+j*TS+TS/2))
		if (-1,j) in highlight:
			draw_highlight(-1,j)
	# board
	for j in range(5):
		for i in range(5):
			hlt = (i,j) in highlight
			filled,known = board[j][i]
			
			if not known:
				draw_unknown(i,j)
			elif filled:
				draw_filled(i,j,(0,0,0))
			else:
				draw_empty(i,j,(0,0,0))
				
			if hlt:
				draw_highlight(i,j)				
				
def draw_text(*lines):
	for i,line in enumerate(lines):
		screen.blit(font.render(line,False,(0,0,128)),(0,32*i))


def render():
	pygame.display.flip()


def clicked_square(pos):
	if not (SW-5*TS <= pos[0] < SW and SH-5*TS <= pos[1] < SH): return (-1,-1)
	return (pos[0]-(SW-5*TS))/TS, (pos[1]-(SH-5*TS))/TS


def stage(highlight,hknown,*text):
	draw_background()
	draw_board(highlight,hknown)
	draw_text(*text)
	render()
	return await_input()


def click_these(squares,highlight,*lines):
	while True:
		if all([board[s[1]][s[0]][1] for s in squares]): break
		clk = stage(highlight,True,*lines)
		sq = clicked_square(clk.pos)
		fill = board[sq[1]][sq[0]][0]
		if sq in squares and clk.right == fill:
			board[sq[1]][sq[0]] = fill,1
		elif sq == (-1,-1):
			stage(set(),False,
					"You must click on the board",
					"[click]")
		elif sq not in squares:
			stage(set(),False,
					"Focus on the highlighted squares for now",
					"[click]")
		elif fill and not clk.right:
			stage(set(),False,
					"Use the RIGHT mouse button to mark squares filled",
					"[click]")
		elif not fill and clk.right:
			stage(set(),False,
					"Use the LEFT mouse button to mark squares empty",
					"[click]")

					
def on_your_own():
	while True:
		if all(sum([[s[1] for s in r] for r in board],[])): break
		clk = stage(set(),False,
			"Now finish the rest of the puzzle using what you've learnt")
		sq = clicked_square(clk.pos)
		if sq == (-1,-1):
			stage(set(),False,
					"You must click on the board",
					"[click]")
		elif board[sq[1]][sq[0]][1]:
			stage(set(),False,
					"That square is already completed",
					"[click]")
		elif board[sq[1]][sq[0]][0] != int(clk.right):
			stage(set(),False,
					"That's incorrect.",
					"Use the RIGHT mouse button to mark squares filled.",
					"Use the LEFT mouse button to mark squares empty.",
					"[click]")
		else:
			board[sq[1]][sq[0]] = board[sq[1]][sq[0]][0],1
			
	
pygame.init()
screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Tutorial")
font = pygame.font.Font(None,32)
bigfont = pygame.font.Font(None,96)

board = [
	[(0,0),(1,0),(1,0),(1,0),(0,0)],
	[(0,0),(0,0),(1,0),(0,0),(0,0)],
	[(1,0),(1,0),(1,0),(1,0),(0,0)],
	[(1,0),(0,0),(0,0),(1,0),(0,0)],
	[(0,0),(0,0),(0,0),(1,0),(0,0)],
]
clues = [(2,),(1,1),(3,),(1,3),(0,)],[(3,),(1,),(4,),(1,1),(1,)]

stage(set(),False,
		"Your goal is to deduce which squares are filled and which are empty",
		"[click]")
stage({(0,-1),(1,-1),(2,-1),(3,-1),(4,-1),(-1,0),(-1,1),(-1,2),(-1,3),(-1,4)},False,
		"The numbers on each row and column indicate the groups of filled ",
		"squares that can be found there",
		"[click]")		
click_these({(4,0),(4,1),(4,2),(4,3),(4,4)}, {(4,-1),(4,0),(4,1),(4,2),(4,3),(4,4)},
		"Zero means there are no filled squares. Left click to mark the empty",
		"squares in this column")
click_these({(0,2),(1,2),(2,2),(3,2)}, {(-1,2),(0,2),(1,2),(2,2),(3,2),(4,2)},
		"This row contains a group of 4 filled squares. There's only one place",
		"it could be. Right click to mark the filled squares on this row")
stage({(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0)},False,
		"This row contains a group of 3 filled squares. There are 2 places that",
		"it could be",
		"[click]")
click_these({(1,0),(2,0)}, {(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0)},
		"But there is a 2 square OVERLAP which is definitely filled. Mark the",
		"filled squares on this row")
click_these({(3,0),(3,1),(3,3),(3,4)}, {(3,-1),(3,0),(3,1),(3,2),(3,3),(3,4)},
		"Groups always appear IN THE ORDER SHOWN. They are always ",
		"SEPARATED by at least 1 empty square. Mark the filled and empty",
		"squares in this column")
click_these({(2,3)}, {(-1,3),(0,3),(1,3),(2,3),(3,3),(4,3)},
		"Groups must be separated, so they have an empty square on either side",
		"of them. Mark the empty square on this row")
click_these({(1,1),(1,3),(1,4)}, {(1,-1),(1,0),(1,1),(1,2),(1,3),(1,4)},
		"It's important to mark empty squares once all the filled squares on a",
		"row or columnn have been found. Mark the empty squares in this column")
on_your_own()
stage(set(),False,
		"You have completed the tutorial. Now try the first puzzle category")
