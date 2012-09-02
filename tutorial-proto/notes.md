% Pixel Pics Tutorial Notes
% Mark Frimston
% 2012-09-02

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
* Free mode doesnt have lives, doesnt tell you if you go wrong
* No guesswork required
* Connecting blocks `3 [ ][#][!][#][ ]`
* Spaces for out of range `2 [!][ ][#][ ][!]`
* Space where block wont fit `2 [ ][ ][x][!][x]`
* Block position can be decided by available space `3,1 [!][!][!][x][ ][ ][ ]`
* Splitting blocks `2,2 [ ][#][!][#][ ]`
* Start with the big numbers first


Garden Faucet
=============

	        1
	     2  1  5  1  0
	  3 [ ][#][#][#][ ]
	  1 [ ][ ][#][ ][ ]
	  3 [#][#][#][ ][ ]
	1 1 [#][ ][#][ ][ ]
	  1 [ ][ ][#][ ][ ]

## 0 - Welcome

_(Chips appears)_

Hi there! My name's Chips and I'm going to show you how to solve Pixel Pics 
puzzles.

The goal is to reveal the hidden picture in each puzzle, by figuring out which 
squares are filled and which are empty.

Take a look at this one. _(puzzle appears)_

_(Indicates numbers)_ See the numbers along the edges? They tell you the 
lengths of the filled blocks that can be found on that row or column, in order.

_(Indicates first column)_ So somewhere in this column there's a block of 2 
filled squares

_(Indicates fourth row)_ And somewhere in this row there are 2 separate filled 
squares

Sounds tricky, right? But it's really easy! Pixel Pics puzzles 
**never require any guesswork** - they can always be solved by thinking 
logically.

I'll show you how!


## 1 - The 5

_(Indicates the 5 column)_ You see this column? The clue says that there is a 
single block of 5 squares here. That's the whole height of the board! So we 
know for sure they must all be filled in. 

Go ahead and fill in those squares in by clicking on them with your right mouse
button

	       5
	[ ][ ][#][ ][ ]
	[ ][ ][#][ ][ ]
	[ ][ ][#][ ][ ]
	[ ][ ][#][ ][ ]
	[ ][ ][#][ ][ ]

Great!

As you can see, the filled-in squares will help us to solve more of the puzzle


## 2 - The 0

_(Indicates zero column)_ Do you see this column? The clue says '0' - that 
means that there are no blocks at all in this column. When we know for sure 
that a square isn't filled in, we can mark it with an 'X'.

Go ahead and mark those squares empty with your left mouse button

	             0
	[ ][ ][#][ ][x]
	[ ][ ][#][ ][x]
	[ ][ ][#][ ][x]
	[ ][ ][#][ ][x]
	[ ][ ][#][ ][x]
	
Excellent!

These will help us deduce more of the puzzle, too


## 3 - Spaces between

_(Indicates 1,1 row)_ Let's take a look at this row. The clue says there are 2
separate single-square blocks. Looks like we've already found one of them!

Each block must be separated by at least 1 empty square. That means the spaces 
either side of the filled block must be empty!

Go ahead and mark these spaces as empty with your left mouse button

	    [ ][ ][#][ ][x]
	    [ ][ ][#][ ][x]
	    [ ][ ][#][ ][x]
	1 1 [ ][x][#][x][x]
	    [ ][ ][#][ ][x]
	    
Fabulous!

## 4 - Inferred blocks

_(Indicates 1,1 row)_ Sometimes there is only 1 remaining place a block could 
be. The other filled square must be in that first space.

Go ahead and fill it!

	    [ ][ ][#][ ][x]
	    [ ][ ][#][ ][x]
	    [ ][ ][#][ ][x]
	1 1 [#][x][#][x][x]
	    [ ][ ][#][ ][x]

Bravo!

## 5 - Overlap

_(Indicates 3 row)_ You see this row? The clue says there is a block of 3, but 
there are 4 spaces! So we don't know for sure exactly where the block starts 
and ends.

_(Shows 3-block on left)_ Maybe it's over here...

_(Shows 3-block on right)_ ...or maybe it's over here?

_(Indicates overlap)_ Either way, there's an _overlap_ in the middle, so we 
know for sure that those spaces must be filled.

Go ahead and fill the middle spaces!

	3 [ ][#][#][ ][x]
	  [ ][ ][#][ ][x]
	  [ ][ ][#][ ][x]
	  [#][x][#][x][x]
	  [ ][ ][#][ ][x]
	  
You got it!

## 6 - Completed rows

_(Indicates second and fifth rows)_ Take a look at these rows. We've already 
found the blocks mentioned in the clues! That means we know for sure the other
spaces on these rows must be empty. 

Go ahead and mark the other spaces as empty!

	  [ ][#][#][ ][x]
	1 [x][x][#][x][x]
	  [ ][ ][#][ ][x]
	  [#][x][#][x][x]
	1 [x][x][#][x][x]
	
Terrific!

## 7 - You take it from here!

Now there are only a few unknown spaces left. How about you take it from here?

Remember, only mark spaces that you know for sure. Good luck!

	      1
	   2  1     1
	3 [x][#][#][#][x]
	  [x][x][#][x][x]
	3 [#][#][#][x][x]
	  [#][x][#][x][x]
	  [x][x][#][x][x]

## 8 - The finished puzzle makes a picture

	    (>( )<)    
	 _____| | 
	|  ___  |
	|_|   | |
	 U    | |

Great work - you solved the puzzle and revealed the hidden picture!

That's all there is to it! Have fun playing Pixel Pics!
