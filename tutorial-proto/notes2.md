% Pixel Pics Tutorial Notes (v2)
% Mark Frimston
% 2014-04-12


In Tutorial
===========

* Aim of the game
* What the numbers signify
* Reveals a picture when complete
* Blocks have to have at least 1 space between
* If clue = row size, can fill it all
* Zero clue means fill with empty
* Counting from the edge `3 [ ][#][!][`
* Overlaps can be filled
* Empties can be marked for completed rows
* Can mark empties around completed blocks
* Panning, Zooming
* Left and right click
* Lose a life if wrong, fail if no more lives
* ~~Free mode doesnt have lives, doesnt tell you if you go wrong~~
* No guesswork required
* Connecting blocks `3 [ ][#][!][#][ ]`
* Spaces for out of range `2 [!][ ][#][ ][!]`
* Space where block wont fit `2 [ ][ ][x][!][x]`
* Block position can be decided by available space `3,1 [!][!][!][x][ ][ ][ ]`
* Splitting blocks `2,2 [ ][#][!][#][ ]`
* Start with the big numbers first
* Groups are in order


Feedback
========

* Too condescending 
* Not concise enough
* Contextual text bubbles to draw the eye
* Let user click at same time as given info
* Reference to "blocks" confusing - use "groups" instead
* Players might want to figure out the techniques themselves from first
  principles - they want that "eureka" moment


Notes
=====

* Possible approaches:
	1. Explain the technique, show the solution, ask player to implement
	2. Explain the technique, ask player to find solution
	3. Ask player to invent technique
* For both approaches, the technique could be introduced either in the 
  context of a board or on an isolated row


Garden Faucet
=============

	        1     1
	     2  1  3  3  0
	  3 [ ][#][#][#][ ]
	  1 [ ][ ][#][ ][ ]
	  4 [#][#][#][#][ ]
	1 1 [#][ ][ ][#][ ]
	  1 [ ][ ][ ][#][ ]

-------------------------------------------------------------------------------

Current
=======

	        1     
	     2  1  5  1  0
	  3 [ ][ ][ ][ ][ ]
	  1 [ ][ ][ ][ ][ ]
	  3 [ ][ ][ ][ ][ ]
	1 1 [ ][ ][ ][ ][ ]
	  1 [ ][ ][ ][ ][ ]

Hi there, I'm Chips! I'm going to show you how to solve PixelPics puzzles!

The goal is to reveal the hidden picture in each puzzle. This is done by 
figuring out which squares are filled and which are empty.

Take a look at this one.

See the numbers along the edges? They tell you the lengths of the filled blocks
that can be found on that row or column, in the order they appear.

	        1     
	     2  1  5  1  0
	  3 [!][ ][ ][ ][ ]
	  1 [!][ ][ ][ ][ ]
	  3 [!][ ][ ][ ][ ]
	1 1 [!][ ][ ][ ][ ]
	  1 [!][ ][ ][ ][ ]

This column has only one number, a 2! So somewhere in this column there's a 
single block of 2 filled squares.

	        1     
	     2  1  5  1  0
	  3 [ ][ ][ ][ ][ ]
	  1 [ ][ ][ ][ ][ ]
	  3 [ ][ ][ ][ ][ ]
	1 1 [!][!][!][!][!]
	  1 [ ][ ][ ][ ][ ]

This row has two separate numbers, each being a 1. So somewhere in this row 
there are two separated filled squares.

Sounds tricky right? It's actually really easy!

PixelPics puzzles never require any guesswork at all! They can always be solved
by thinking logically. I'll show you!

	        1     
	     2  1  5  1  0
	  3 [ ][ ][!][ ][ ]
	  1 [ ][ ][!][ ][ ]
	  3 [ ][ ][!][ ][ ]
	1 1 [ ][ ][!][ ][ ]
	  1 [ ][ ][!][ ][ ]

Let's start with this column. The clue says there's a single block of 5 squares
here.

That's the whole height of the board! So we know for sure that they must all be
filled in.

Go ahead and fill in those squares by clicking on them with your right mouse 
button!

Great! The squares that you figure out will help you solve more of the puzzle!

	        1      
	     2  1  5  1  0
	  3 [ ][ ][#][ ][!]
	  1 [ ][ ][#][ ][!]
	  3 [ ][ ][#][ ][!]
	1 1 [ ][ ][#][ ][!]
	  1 [ ][ ][#][ ][!]

Take a look at this column. The clue is 0, that means there are no filled 
squares in this column at all!

When we know for sure that a square isn't filled in, we can mark it with an 
'X'.

Go ahead and mark those squares as empty with your left mouse button!

Excellent! These will help us deduce more of the puzzle too.

	        1     
	     2  1  5  1  0
	  3 [ ][ ][#][ ][x]
	  1 [ ][ ][#][ ][x]
	  3 [ ][ ][#][ ][x]
	1 1 [!][!][#][!][x]
	  1 [ ][ ][#][ ][x]

Remember this row? The clue says there are 2 separated filled squares. Hey, 
we've already found one of them!

Each block of squares must be separated by at least 1 empty square. That means 
that the squares either side of the filled block must be empty!

Go ahead and mark those spaces as empty with your left mouse button.

Fabulous!

	        1     
	     2  1  5  1  0
	  3 [ ][ ][#][ ][x]
	  1 [ ][ ][#][ ][x]
	  3 [ ][ ][#][ ][x]
	1 1 [!][x][#][x][x]
	  1 [ ][ ][#][ ][x]

Sometimes there is only 1 remaining place a block of squares could be. So the 
other filled square must be in the highlighted space!

Go ahead and fill it!

Bravo!

	        1     
	     2  1  5  1  0
	  3 [!][!][#][!][x]
	  1 [ ][ ][#][ ][x]
	  3 [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	  1 [ ][ ][#][ ][x]

Check out this row. The clue says there's a single block of 3. But there are 4 
spaces! So we don't know for sure exactly where the block starts and ends.

	        1     
	     2  1  5  1  0
	  3 [!][!][!][ ][x]
	  1 [ ][ ][#][ ][x]
	  3 [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	  1 [ ][ ][#][ ][x]

Maybe it's over here...

	        1     
	     2  1  5  1  0
	  3 [ ][!][!][!][x]
	  1 [ ][ ][#][ ][x]
	  3 [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	  1 [ ][ ][#][ ][x]

Or maybe it's over here?

Either way there's an overlap of two squares in the middle. So we know for sure
that those squares must be filled!

Go ahead and fill that middle square to complete the overlap!

You got it!

	        1     
	     2  1  5  1  0
	  3 [ ][#][#][ ][x]
	  1 [!][!][#][!][x]
	  3 [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	  1 [!][!][#][!][x]

Take a look at these rows. We've already found the blocks mentioned in the 
clues! Notice that the clues change colour when we've solved them.

That means we know for sure that the other squares on these rows must be empty.

Go ahead and mark those squares as empty!

Teriffic!

	        1     
	     2  1  5  1  0
	  3 [ ][#][#][ ][x]
	  1 [x][x][#][x][x]
	  3 [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	  1 [x][x][#][x][x]

Now there are only a few unfilled squares left. How about you take it from 
here?

Remember, only mark squares that you know for sure. Good luck!


-------------------------------------------------------------------------------

New
===

	        1     1
	     2  1  3  3  0
	  3 [ ][ ][ ][ ][ ]
	  1 [ ][ ][ ][ ][ ]
	  4 [ ][ ][ ][ ][ ]
	1 1 [ ][ ][ ][ ][ ]
	  1 [ ][ ][ ][ ][ ]

Your goal is to deduce which squares are filled and which are empty

	       V  V  V  V  V
	          1     1
	       2  1  3  3  0
	>   3 [ ][ ][ ][ ][ ]
	>   1 [ ][ ][ ][ ][ ]
	>   4 [ ][ ][ ][ ][ ]
	> 1 1 [ ][ ][ ][ ][ ]
	>   1 [ ][ ][ ][ ][ ]

The numbers on each row and column indicate the groups of filled squares which 
can be found there

	        1     1  
	     2  1  3  3  0
	  3 [ ][ ][ ][ ][!]
	  1 [ ][ ][ ][ ][!]
	  4 [ ][ ][ ][ ][!]
	1 1 [ ][ ][ ][ ][!]
	  1 [ ][ ][ ][ ][!]
	  
Zero means there are no filled squares. Left click on these squares to mark 
them empty

(tick)

	        1     1  
	     2  1  3  3  0
	  3 [ ][ ][ ][ ][x]
	  1 [ ][ ][ ][ ][x]
	  4 [!][!][!][!][x]
	1 1 [ ][ ][ ][ ][x]
	  1 [ ][ ][ ][ ][x]

This row contains a group of 4 filled squares. There's only one place it 
could be. Right click these squares to mark them filled

(tick)

	        1     1
	     2  1  3  3  0
	  3 [!][!][!][!][x]
	  1 [ ][ ][ ][ ][x]
	  4 [#][#][#][#][x]
	1 1 [ ][ ][ ][ ][x]
	  1 [ ][ ][ ][ ][x]

This row contains a group of 3 filled squares. There are 2 places that it could
be

(alternating highlight)

	        1     1
	     2  1  3  3  0
	  3 [ ][!][!][ ][x]
	  1 [ ][ ][ ][ ][x]
	  4 [#][#][#][#][x]
	1 1 [ ][ ][ ][ ][x]
	  1 [ ][ ][ ][ ][x]

Therefore these 2 squares are definitely filled. Mark these squares as filled

(tick)

	              
	        1     1
	     2  1  3  3  0
	  3 [ ][#][#][!][x]
	  1 [ ][ ][ ][!][x]
	  4 [#][#][#][#][x]
	1 1 [ ][ ][ ][!][x]
	  1 [ ][ ][ ][!][x]

Groups always appear *in the order shown*. They are always *separated* by at 
least 1 empty square. 

	        1     1
	     2  1  3  3  0
	  3 [ ][#][#][!][x]
	  1 [ ][ ][ ][-][x]
	  4 [#][#][#][#][x]
	1 1 [ ][ ][ ][!][x]
	  1 [ ][ ][ ][!][x]

So, there is only 1 way these groups could be arranged. Mark the filled and 
empty squares as shown

(tick)

	          1     1
	       2  1  3  3  0
	    3 [ ][#][#][#][x]
	    1 [ ][ ][ ][x][x]
	    4 [#][#][#][#][x]
	  1 1 [ ][ ][!][#][x]
	    1 [ ][ ][ ][#][x]

Groups must be separated, so this filled square must have an empty square on 
either side of it. Mark the empty square as shown

(tick)

	        1     1
	     2  1  3  3  0
	  3 [ ][#][#][#][x]
	  1 [ ][!][ ][x][x]
	  4 [#][#][#][#][x]
	1 1 [ ][!][x][#][x]
	  1 [ ][!][ ][#][x]
	  
It's important to mark empty squares once all the filled squares on a row or 
column have been found. Mark these squares as empty

(tick)

	        1     1
	     2  1  3  3  0
	  3 [ ][#][#][#][x]
	  1 [ ][x][ ][x][x]
	  4 [#][#][#][#][x]
	1 1 [ ][x][x][#][x]
	  1 [ ][x][ ][#][x]

Now finish the rest of the puzzle using what you've learnt

(puzzle complete, reveal picture)

You have completed the tutorial. Now try the first puzzle category
