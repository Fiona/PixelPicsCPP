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
		
def draw_board(highlight=[]):
	pygame.draw.rect(screen,(255,255,255),(SW-5*TS,SH-5*TS,5*TS,5*TS))
	for i in range(5):
		for n,c in enumerate(reversed(clues[0][i])):
			screen.blit(font.render(str(c),False,(0,0,0)),(SW-5*TS+i*TS+TS/2,SH-5*TS-(n+1)*TS/2))
	for j in range(5):
		for n,c in enumerate(reversed(clues[1][j])):
			screen.blit(font.render(str(c),False,(0,0,0)),(SW-5*TS-(n+1)*TS/2,SH-5*TS+j*TS+TS/2))
	for j in range(5):
		for i in range(5):
			if not board[j][i][1]:
				pygame.draw.rect(screen,(0,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),1)
			elif board[j][i][0]:
				pygame.draw.rect(screen,(0,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),0)
			else:
				pygame.draw.rect(screen,(0,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),1)
				pygame.draw.line(screen,(0,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS),(SW-5*TS+i*TS+TS,SH-5*TS+j*TS+TS),2)
				pygame.draw.line(screen,(0,0,0),(SW-5*TS+i*TS+TS,SH-5*TS+j*TS),(SW-5*TS+i*TS,SH-5*TS+j*TS+TS),2)
			
			if (i,j) in highlight:
				pygame.draw.rect(screen,(255,0,0),(SW-5*TS+i*TS,SH-5*TS+j*TS,TS,TS),10)

def draw_text(*lines):
	for i,line in enumerate(lines):
		screen.blit(font.render(line,False,(0,0,128)),(0,32*i))

def render():
	pygame.display.flip()

def clicked_square(pos):
	if not (SW-5*TS <= pos[0] < SW and SH-5*TS <= pos[1] < SH): return (-1,-1)
	return (pos[0]-(SW-5*TS))/TS, (pos[1]-(SH-5*TS))/TS

def stage(highlight,showboard,*text):
	draw_background()
	if showboard: draw_board(highlight)
	draw_text(*text)
	render()
	return await_input()

def click_these(squares,right,*lines):
	while True:
		if all([board[s[1]][s[0]][1] for s in squares]): break
		clk = stage(squares,True,*lines)
		sq = clicked_square(clk.pos)
		if clk.right == right and sq in squares:
			board[sq[1]][sq[0]] = int(right),1
		elif sq == (-1,-1):
			stage([],True,
					"Whoops! Make sure you click on the board!",
					"[click]")
		elif sq not in squares:
			stage([],True,
					"We'll get to the other squares in a second - let's focus on the ",
					"highlighted ones for now!",
					"[click]")
		elif right and not clk.right:
			stage([],True,
					"Whoops! That was a left click. Be sure to use the RIGHT mouse button to ",
					"fill in spaces.",
					"[click]")
		elif not right and clk.right:
			stage([],True,
					"Whoops! That was a right click. Be sure to use the LEFT mouse button to ",
					"mark spaces as empty.",
					"[click]")
					
def on_your_own():
	while True:
		if all(sum([[s[1] for s in r] for r in board],[])): break
		clk = stage([],True)
		sq = clicked_square(clk.pos)
		if sq == (-1,-1):
			stage([],True,
					"Whoops! Make sure you click on the board!",
					"[click]")
		elif board[sq[1]][sq[0]][1]:
			stage([],True,
					"Whoops! That square has already been completed.",
					"[click]")
		elif board[sq[1]][sq[0]][0] != int(clk.right):
			stage([],True,
					"Whoops! That's incorrect. Remember to use the RIGHT mouse button to fill",
					"spaces and the LEFT mouse button to mark them as empty. Only click a",
					"space when you can logically deduce what's there.",
					"[click]")
		else:
			board[sq[1]][sq[0]] = board[sq[1]][sq[0]][0],1
			
	
pygame.init()
screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Tutorial")
font = pygame.font.Font(None,32)

board = [
	[(0,0),(1,0),(1,0),(1,0),(0,0)],
	[(0,0),(0,0),(1,0),(0,0),(0,0)],
	[(1,0),(1,0),(1,0),(0,0),(0,0)],
	[(1,0),(0,0),(1,0),(0,0),(0,0)],
	[(0,0),(0,0),(1,0),(0,0),(0,0)],
]
clues = [(2,),(1,1),(5,),(1,),(0,)],[(3,),(1,),(3,),(1,1),(1,)]

stage([],False, "Hi there!",
				"My name's Chips and I'm going to show you how to solve Pixel Pics puzzles.",
				"[click]")
stage([],False, "The goal is to reveal the hidden picture in each puzzle, by figuring out",
				"which squares are filled and which are empty.",
				"[click]")
stage([],True,  "Take a look at this one.",
				"[click]")
stage([],True,  "See the numbers along the edges? They tell you the lengths of the filled ",
				"blocks that can be found on that row or column, in order.",
				"[click]")
stage([(0,0),(0,1),(0,2),(0,3),(0,4)],True,  
				"So somewhere in this column there's a block of 2 filled squares",
				"[click]")
stage([(0,3),(1,3),(2,3),(3,3),(4,3)],True,
				"And somewhere in this row there are 2 separate filled squares",
				"[click]")
stage([],True,  "Sounds tricky, right? But it's really easy!",
				"[click]")
stage([],True,  "Pixel Pics puzzles NEVER REQUIRE ANY GUESSWORK - they can always ",
				"be solved by thinking logically. I'll show you how!",
				"[click]")
stage([(2,0),(2,1),(2,2),(2,3),(2,4)],True,
				"You see this column? The clue says that there is a single block of 5 ",
				"squares here.",
				"[click]")
stage([(2,0),(2,1),(2,2),(2,3),(2,4)],True,	
				"That's the whole height of the board! So we know for sure they must all be",
				"filled in.",
				"[click]")				
click_these([(2,0),(2,1),(2,2),(2,3),(2,4)],True,
				"Go ahead and fill in those squares by clicking on them with your right",
				"mouse button")					
stage([],True,	"Great!",
				"As you can see, the filled-in squares will help us to solve more of the",
				"puzzle",
				"[click]")
stage([(4,0),(4,1),(4,2),(4,3),(4,4)],True,
				"Do you see this column? The clue says '0' - that means that there are ",
				"no blocks at all in this column.",
				"[click]")
stage([(4,0),(4,1),(4,2),(4,3),(4,4)],True,
				"When we know for sure that a square isn't filled in, we can mark it with",
				"an 'X'.",
				"[click]")
click_these([(4,0),(4,1),(4,2),(4,3),(4,4)],False,
				"Go ahead and mark those squares empty with your left mouse button")
stage([],True,	"Excellent! These will help us deduce more of the puzzle, too",
				"[click]")
stage([(0,3),(1,3),(2,3),(3,3),(4,3)],True,
				"Let's take a look at this row. The clue says there are 2 separate ",
				"single-square blocks. Looks like we've already found one of them!",
				"[click]")
stage([(1,3),(3,3)],True,
				"Each block must be separated by at least 1 empty square. That means",
				"the spaces either side of the filled block must be empty!",
				"[click]")
click_these([(1,3),(3,3)],False,
				"Go ahead and mark these spaces as empty with your left mouse button")
stage([],True,	"Fabulous!",
				"[click]")
stage([(0,3)],True,
				"Sometimes there is only 1 remaining place a block could be. The other",
				"filled square must be in that first space.",
				"[click]")
click_these([(0,3)],True,
				"Go ahead and fill it!")
stage([],True,	"Bravo!",
				"[click]")
stage([(0,0),(1,0),(2,0),(3,0),(4,0)],True,
				"You see this row? The clue says there is a block of 3, but there are",
				"4 spaces! So we don't know for sure exactly where the block starts ",
				"and  ends.",
				"[click]")
stage([(0,0),(1,0),(2,0)],True,
				"Maybe it's over here...",
				"[click]")
stage([(1,0),(2,0),(3,0)],True,
				"...or maybe it's over here?",
				"[click]")
stage([(1,0),(2,0)],True,
				"Either way, there's an OVERLAP in the middle, so we know for sure that",
				"those spaces must be filled.",
				"[click]")
click_these([(1,0)],True,
				"Go ahead and fill that middle space!")
stage([],True,	"You got it!",
				"[click]")
stage([(0,1),(1,1),(2,1),(3,1),(4,1),(0,4),(1,4),(2,4),(3,4),(4,4)],True,
				"Take a look at these rows. We've already found the blocks mentioned in",
				"the clues!",
				"[click]")
stage([(0,1),(1,1),(3,1),(0,4),(1,4),(3,4)],True,
				"That means we know for sure the other spaces on these rows must be ",
				"empty.",
				"[click]")
click_these([(0,1),(1,1),(3,1),(0,4),(1,4),(3,4)],False,
				"Go ahead and mark the other spaces empty!")
stage([],True,	"Terrific!",
				"[click]")
stage([],True,	"Now there are only a few unknown spaces left. How about you take it from",
				"here?",
				"[click]")
stage([],True,	"Remember, only mark spaces that you know for sure. Good luck!",
				"[click]")
on_your_own()
stage([],True,	"Great work - you solved the puzzle and revealed the hidden picture!",
				"[click]")
stage([],False,	"That's all there is to it! Have fun playing Pixel Pics!")
