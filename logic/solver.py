"""
PixelPics - Nonogram game
(c) Stompy Blondie 2011/2012 http://stompyblondie.com
"""

import copy

# TODO: ignore solved sequences

class GuessesExceededException(Exception):
    pass

class ContradictionException(Exception):
    pass

class AmbiguousException(Exception):
    pass

class Sentinel(object):
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return self.name

EITHER = Sentinel("EITHER")
ROW = Sentinel("ROW")
COL = Sentinel("COL")


def test_block_positions(cells,hints,block,startpos,positions,known):
    """ 
    Takes sequence of cells, the hints, the block number where to start
    its position testing, the positions of the other blocks so far, and
    a sequence of cells states: None (untested) or True/False/EITHER
    representing the possible values the cell could be as determined so 
    far. The 'known' list is manipulated in place, and the number of 
    valid configurations of it and the subsequent blocks is returned.
    This is a generator which yields None until completed, at which 
    point it yields the result.
    """
    # Will yield each time a block is tested in a set of positions. 
    # i.e. for a single block, only one yield is made.
    validconfigs = 0

    # try the block in every position from pos to end
    for testpos in range(startpos,len(cells)-hints[block]+1):
        
        # revealed an existing block here?
        if testpos > 0 and cells[testpos-1]==True:
            # block has gone as far as it can go
            break
        
        # adjacent to an existing subsequent block here?
        if testpos < len(cells)-hints[block] and cells[testpos+hints[block]]==True:
            continue
        
        # covers any spaces here?
        moveon = False
        for i in range(testpos,testpos+hints[block]):
            if cells[i]==False:
                moveon = True
                break
        if moveon: 
            continue
        
        # is this the last block and are there any subsequent blocks filled?
        moveon = False
        if block == len(hints)-1:
            for i in range(testpos+hints[block],len(cells)):
                if cells[i]==True:
                    moveon = True
                    break
        if moveon:
            continue
            
        # block position is ok, record position
        positions[block] = testpos
        
        if block < len(hints)-1:                    
            # if more blocks, recurse to find all their possible positions
            n = None
            gen = test_block_positions(cells,hints,block+1,testpos+hints[block]+1,positions,known)
            while n is None:
                n = gen.next()
                yield 
            # if found valid configs for remaining blocks, count this 
            # as valid block position and add the configs to the total
            if n > 0: validconfigs += n
        else:
            # last block, so merge the state of the block positions into result
            # run over each cell
            b = 0
            for p in range(len(cells)):
                if p < positions[b]:
                    # not at block yet, so empty
                    v = False
                elif p < positions[b]+hints[b]:
                    # in block, so filled
                    v = True
                elif b < len(hints)-1:
                    # past block with more to go, so move to next block and use empty
                    b += 1
                    v = False
                else:
                    # past last block, so use empty
                    v = False
                    
                # merge cell value with recorded state
                if known[p] is None:
                    known[p] = v                
                elif (v==True and known[p]==False) or (v==False and known[p]==True):
                    known[p] = EITHER
                    
            # count this valid block position
            validconfigs += 1
                    
    # return the number of valid block configurations
    yield validconfigs


def backtrack_to_movable_hint(hs,hnum,anchors,anc):
    """ 
    Helper for process_seq_fast. Finds the latest previous hint block
    which can be moved forwards to cover the anchor immediately following
    it, starting with the hint and anchor specified. Returns the hint
    number to move and its new position.
    """
    while hnum >= 0:
        
        # can current hint block be moved enough, without uncovering 
        # its anchor, to cover the current anchor?
        if anchors[hnum] is None or anchors[hnum]+hs[hnum]-1 >= anc:
            return hnum,anc-(hs[hnum]-1)
        
        # otherwise loop to see if previous hint block can cover the 
        # current block's anchor, potentially allowing it to be moved
        anc = anchors[hnum]
        hnum -= 1
            
    # if there are no more hints, there's a contradiction
    raise ContradictionException()


def process_seq_fast(cells,hints):
    """ 
    Attempt to deduce as many filled and empty cells as possible from
    the given cells and hints. This implementation is designed to find
    most cells but sacrifices some discoveries for the sake of speed.
    This is a generator which yields None until complete, at which point
    the result is yielded.
    """
    retval = []
    
    # special case for empty hints - fill in the blanks
    if len(hints)==0:
        for i in range(len(cells)):
            if cells[i] != False:
                retval.append((i,False))
        yield retval
        return
            
    minends = [None]*len(hints)
    maxstarts = [None]*len(hints)
    
    # make reversed, indexable copies of cells and hints
    revcells = list(cells)[:]
    revcells.reverse()
    revhints = list(hints)[:]
    revhints.reverse()
    
    # make forwards and backwards pass
    for seq,hs,ends in [ (cells,hints,minends),(revcells,revhints,maxstarts) ]:
        
        pos = 0
        hnum = 0
        anchors = [None]*len(hs)
        
        # hint loop
        while True:
            
            # all hints been successfully placed?
            if hnum > len(hs):
                # exit hint loop
                break
            
            # iteration after last hint placed?
            elif hnum == len(hs):
                # iterate over remaining cells to check for filled
                while pos < len(seq):
                    if seq[pos]==True:
                        # found a filled after hint blocks. Go back to where a previous
                        # hint block should be moved to.
                        hnum,pos = backtrack_to_movable_hint(hs,len(hs)-1,anchors,pos)
                        break
                    pos += 1
                else:
                    # no filled cells after last hint advance in order to 
                    # exit on next iteration
                    hnum += 1
                
            # there are still hints to place
            else:
                
                gap = 0
                anc = None
                hint = hs[hnum]
                
                # iterate over cells to place blocks
                while True:
                    # if more than one cell beyond end without finding 
                    # place for hint, its a contradiction
                    if pos > len(seq):
                        raise ContradictionException()
                    # if current hint pos reveals anchor, a previous hint must be moved
                    elif anc is not None and pos-hint>anc:
                        # Go back to where a previous hint block should be moved to
                        hnum,pos = backtrack_to_movable_hint(hs,hnum-1,anchors,anc)
                        break
                    # if found empty after hint-sized gap, record place for hint
                    elif (pos==len(seq) or seq[pos]!=True) and gap>=hint:
                        ends[hnum] = pos-1
                        anchors[hnum] = anc
                        # leave the empty cell before next hint
                        pos += 1
                        # move on to next hint
                        hnum += 1
                        break
                    # add to gap for non-empty cell
                    elif pos<len(seq) and seq[pos]!=False:
                        gap += 1
                        # if the first filled cell in gap, record anchor
                        if seq[pos]==True and anc is None:
                            anc = pos
                    # reset gap for empty cell
                    elif pos<len(seq) and seq[pos]==False:
                        gap = 0
                    # next cell
                    pos += 1
                                
    # make maxstarts relative to start rather than end
    maxstarts = map(lambda i: len(cells)-1-i, maxstarts)
    maxstarts.reverse()
    
    # for each hint
    for i in range(len(hints)):
        start = maxstarts[i]
        end = minends[i]
        # iterate over overlapping cells
        if start <= end:
            for j in range(start,end+1):
                # add discovered cells to return value
                if cells[j] is None:
                    retval.append((j,True))
            # special case - if overlap is whole block, deduce start
            # and end spaces
            if end-start+1 == hints[i]:
                if( start-1 >= 0 and cells[start-1] is None 
                            and (start-1,False) not in retval):
                    retval.append((start-1,False))
                if( end+1 < len(cells) and cells[end+1] is None
                            and (end+1,False) not in retval):
                    retval.append((end+1,False))
                    
    # there can only be spaces before the first possible hint pos
    for i in range(0,minends[0]-(hints[0]-1)):
        if cells[i] is None and (i,False) not in retval:
            retval.append((i,False))

    # there can only be spaces after the last possible hint pos
    for i in range(maxstarts[-1]+hints[-1],len(cells)):
        if cells[i] is None and (i,False) not in retval:
            retval.append((i,False))
    
    yield retval
        

def process_seq_accurate(cells,hints):
    """ 
    Process the given sequence of cells, attempting to deduce the state
    of the unknown (None) values as filled (True) or empty (False) using 
    the given block hints and existing state of the cells. The deduced
    values are returned as a sequence of 2-tuples containing the cell
    index and True/False value. ContradictionException is raised if it 
    is impossible to place the hinted blocks in the given cell states.
    This is a generator which yields None until complete, at which point
    the result is yielded.
    """

    # special case - if no hints, fill in unknowns with empties
    if len(hints)==0:
        retval = []
        for i,v in enumerate(cells):
            if v!=False:
                retval.append((i,False))
        yield retval
        return

    # test possible positions recursively
    result = [None]*len(cells)
    gen = test_block_positions(cells,hints,0,0,[None]*len(hints),result)
    num_configs = None
    while num_configs is None:
        num_configs = gen.next()
        yield
    if num_configs == 0:
        # no valid configurations found, raise exception
        raise ContradictionException()
    
    # prepare return value
    retval = []
    for i,v in enumerate(result):
        if v in (True,False) and cells[i]!=v:
            retval.append((i,v))
            
    #print "%s,%s -> %s" % tuple(map(str,[cells,hints,retval]))
    yield retval
    return


def seq_priority_lifo(stack,board,cols,rows):
    return stack.pop()


def est_seq_solvability(length,hints):
    n = len(hints)
    if n==0:
        return length
    return (n+1)*sum(hints) + n*(n-length-1)
    

def make_heuristic_seq_pri(heuristic):
    def fn(stack,board,cols,rows):
        def evaluate_item((rc,num)):
            if rc==ROW:
                return heuristic(len(cols),rows[num])
            else:
                return heuristic(len(rows),cols[num])
        stack.sort(key=evaluate_item)
        return stack.pop()
    return fn


def seq_solve(cols,rows,board,processfirst,seq_processor,seq_priority_stgy,
        cache):
    """ 
    Attempts to apply the given sequence solver continuously to the
    rows and columns of the given board using the given row and column
    hints. The rows and columns in processfirst are processed first - 
    these are 2-tuples of ROW/COL and row or column number. The board 
    is manipulated in place, and True is returned if the board is solved.
    ContradictionException is raised if the board is found to contradict
    the hints. This is a generator which yields None until complete, then
    yields the result.
    """
    
    # create stack
    procstack = []
    
    # push each column onto processing stack
    for i in range(len(cols)):
        procstack.append((COL,i))
        
    # push each row onto processing stack
    for i in range(len(rows)):
        procstack.append((ROW,i))

    # re-add priority rows/cols to top of stack
    for c in processfirst:
        procstack.remove(c)
        procstack.append(c)

    # pop items from processing stack until empty
    while len(procstack) > 0:
        rc,num = seq_priority_stgy(procstack,board,cols,rows)
        # TODO: DRY!
        if rc == ROW:
            # process row
            procres = None
            cells,hints = [c for c in board[num]],rows[num]
            # attempt cache lookup
            if cache is not None and (tuple(cells),hints) in cache:
                procres = cache[tuple(cells),hints]
            else:
                proc = seq_processor(cells,hints)
                while procres is None:
                    procres = proc.next()
                    yield 
                if cache is not None:
                    cache[tuple(cells),hints] = procres
            for i,v in procres:
                # (re)push altered col onto top of stack to re-process
                if (COL,i) in procstack:
                    procstack.remove((COL,i))
                procstack.append((COL,i))
                # update board
                board[num][i] = v
        elif rc==COL:
            # process col
            procres = None
            cells,hints = [r[num] for r in board],cols[num]
            # attempt cache lookup
            if cache is not None and (tuple(cells),hints) in cache:
                procres = cache[tuple(cells),hints]
            else:
                proc = seq_processor([r[num] for r in board], cols[num])
                while procres is None:
                    procres = proc.next()
                    yield
                if cache is not None:
                    cache[tuple(cells),hints] = procres
            for i,v in procres:
                # (re)push altered row onto top of stack to re-process
                if (ROW,i) in procstack:
                    procstack.remove((ROW,i))
                procstack.append((ROW,i))
                # update board
                board[i][num] = v

    # check whether the board was solved
    solved = True
    for row in board:
        for col in row:
            if col is None:
                # found unknown - board is unsolved
                solved = False
                break
        if not solved: break
                
    # return whether solved or not
    yield solved


def solve_state(cols,rows,board,processfirst,seq_processors,seq_priority_stgy,
        guesses,cache):
    """ 
    Attempts to solve the given board, returning a new board and boolean
    stating whether it was solved or not. Raises ContradictionException 
    if the board is found to contradict the hints. AmbiguousException is 
    raised if the board is found to have more than one solution. 
    GuessesExceededException is raised if the board cannot be solved after
    exhausting the allowed guesses. This is a generator which yields None 
    until complete, then yields the result.
    """
    # attempt to line-solve the board, using available line-solvers
    for processor in seq_processors:
        solved = None
        proc = seq_solve(cols,rows,board,processfirst,processor,seq_priority_stgy,
                cache)
        while solved is None:
            solved = proc.next()
            yield
        if solved:
            yield board,True
            return
        
    # if guessing is disabled, return unsolved
    if guesses is None:
        yield board,False
        return
    # if guessing enabled but we're out of guesses, raise exception
    elif guesses==0:
        raise GuessesExceededException()
        
    # if not line solvable, find an unknown to guess at
    guesspos = None
    for j,row in enumerate(board):
        for i,cell in enumerate(row):
            if cell is None:
                guesspos = j,i
                break
        if guesspos is not None: break
    
    results = []
    
    # create copy of board with cell guessed True
    tgboard = copy.deepcopy(board)
    tgboard[guesspos[0]][guesspos[1]] = True
    try:
        # recurse to solve guess board
        res = None
        slv = solve_state(cols,rows,tgboard,
            [(ROW,guesspos[0]),(COL,guesspos[1])],seq_processors,
            seq_priority_stgy,guesses-1,cache)
        while res is None:
            res = slv.next()
            yield
        results.append(res)
    except ContradictionException:
        pass
        
    # create copy of board with cell guessed False
    fgboard = copy.deepcopy(board)
    fgboard[guesspos[0]][guesspos[1]] = False
    try: 
        # recurse to solve guess board
        res = None
        slv = solve_state(cols,rows,fgboard,
            [(ROW,guesspos[0]),(COL,guesspos[1])],seq_processors,
            seq_priority_stgy,guesses-1,cache)
        while res is None:
            res = slv.next()
            yield
        results.append(res)
    except ContradictionException:
        pass

    # count results
    if len(results)==0:
        # neither guess yielded a solution - board is an invalid state
        raise ContradictionException()
    elif len(results)==1:
        # one right guess, one wrong - return solution
        yield results[0]
    else:
        # two solutions - board is ambiguous
        raise AmbiguousException()


def solve(cols,rows,guesses=10,caching=True,seq_processors=[process_seq_fast,process_seq_accurate],
        seq_priority_stgy=make_heuristic_seq_pri(est_seq_solvability)):
    """ 
    Attempts to solve the given hints using the given sequence processor 
    and returns the board and a boolean stating whether completed or not. 
    Raises ContradictionException if the hints are found to be impossible. 
    Raises AmbiguousException if the hints have multiple solutions. 
    Raises GuessesExceededException if the board cannot be solved after 
    exhausting the allowed number of guesses. This is a generator which 
    yields None until complete, then yields the result.
    """
    # initialise empty board
    board = [[None]*len(cols) for r in range(len(rows))]

    # solve recursively
    res = None
    cache = {} if caching else None
    gen = solve_state(cols,rows,board,[],seq_processors,seq_priority_stgy,
        guesses,cache)
    while res is None:
        res = gen.next()
        yield

    yield res


def verify_puzzle(puzzle,solver=solve):
    """ 
    Attempts to solve the given puzzle. This is a generator which yields
    None untils complete, then yields True if the puzzle was successfully
    solved. The following exceptions may be raised:
        ContradictionException - if the puzzle hints are contradictory
        AmbiguousException - if more than one puzzle solution is found
        GuessesExceededException - if the solved made too many guesses
    """
    cols = list(puzzle.column_numbers)
    rows = list(puzzle.row_numbers)
    for _list in (cols, rows):
        for i,x in enumerate(_list):
            if x == (0,):
                _list[i] = ()
    result = None
    gen = solver(cols,rows)
    while result is None:
        result = gen.next()
        yield
        
    board,solved = result
    yield solved

    
    

if __name__ == "__main__":
    import unittest
    import mock
    import pdb
    import puzzle
    
    DANCER = ([(2,1),(2,1,3),(7,),(1,3),(2,1)],
                [(2,),(2,1),(1,1),(3,),(1,1),(1,1),(2,),(1,1),(1,2),(2,)])
                    
    CAT = ([(5,),(5,3),(2,3,4),(1,7,2),(8,),(9,),(9,),(8,),(7,),(8,),(9,),(10,),(13,),(6,2),(4,),(6,),(6,),(5,),(6,),(6,)],
            [(2,),(2,),(1,),(1,),(1,3),(2,5),(1,7,1,1),(1,8,2,2),(1,9,5),(2,16),(1,17),(7,11),(5,5,3),(5,4),(3,3),(2,2),(2,1),(1,1),(2,2),(2,2)])
        
    SMILEY4X4 = ([(1,1),(1,),(1,),(1,1)],[(1,1),(),(1,1),(2,)])
    
    SMILEY5X6 = ([(3,1),(3,1),(1,),(3,1),(3,1)],[(2,2),(2,2),(2,2),(),(1,1),(3,)])

    UHINT_GUESS = ([(2,1),(1,),(3,1),(1,1,1),(4,)],[(1,3),(1,1,1),(3,),(1,),(1,1),(2,)])
    UHINT_GUESS_SOL = [
            [ True, False,True, True, True  ],
            [ True, False,True, False,True  ],
            [ False,False,True, True, True  ],
            [ False,False,False,False,True  ],
            [ True, False,False,True, False ],
            [ False,True, True, False,False ]   
        ]
    UHINT_GUESS_GS = [[
            [ False,False,False,False,False ],
            [ False,False,False,False,False ],
            [ False,False,False,False,False ],
            [ False,False,False,False,False ],
            [ True, True, True, True, False ],
            [ True, True, True, True, False ]   
        ]]
    
    UHINT_2_GUESS = ([(2,1),(1,1),(1,2,1),(1,1,1),(1,2),(3,2)],[(1,1),(2,),(1,),(1,4),(1,1,2),(),(2,1),(1,1,1)])
    UHINT_2_GUESS_SOL = [
            [ False,True, False,False,True, False ],
            [ False,False,True, True, False,False ],
            [ False,False,False,False,False,True  ],
            [ True, False,True, True, True, True  ],
            [ True, False,True, False,True, True  ],
            [ False,False,False,False,False,False ],
            [ False,True, True, False,False,True  ],
            [ True, False,False,True, False,True  ]
        ]
    UHINT_2_GUESS_GS = [[
            [ False,True, True, True, True, False ],
            [ False,True, True, True, True, False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ]
        ],[ 
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ False,False,False,False,False,False ],
            [ True, True, True, True, False,False ],
            [ True, True, True, True, False,False ]
        ]]
    
    HEART = ([(2,),(4,),(4,),(4,),(2,)],[(1,1),(5,),(5,),(3,),(1,)])
    HEART_SOL = [
        [ False,True, False,True, False ],
        [ True, True, True, True, True  ],
        [ True, True, True, True, True  ],
        [ False,True, True, True, False ],
        [ False,False, True, False,False ],
    ]
    
    class TestFastSequenceProcessor(unittest.TestCase):
        
        def test_invokable(self):
            # test generator can be called
            r = None
            proc = process_seq_fast([None]*10,DANCER[0][0])
            while r is None:
                r = proc.next()
        
        def test_returns_value(self):
            # test that method returns a list of 2-tuples
            r = None
            proc = process_seq_fast([None,None,None,None,None],(3,))
            while r is None:
                r = proc.next()
            self.assertEquals(list,type(r))
            self.assertEquals(tuple,type(r[0]))
        
        def test_single_box(self):
            # test we can find the possible overlap of a single block
            cells = [None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(4,))
            while r is None:
                r = proc.next()
            self.assertEquals([(1,True),(2,True),(3,True)],r)
            self.assertTrue( all([(i,True) in r for i in (1,2,3)]) )
            self.assertTrue( not any([(i,True) in r for i in (0,4)]) )
        
        def test_single_box_no_overlap(self):
            # test that nothing is inferred for a single block without 
            # overlapping possibilities
            cells = [None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,))
            while r is None:
                r = proc.next()
            self.assertEquals([],r)
        
        def test_multiple_boxes(self):
            # test we can find the possible overlap of multiple blocks
            cells = [None,None,None,None,None,None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(4,3))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (2,3,7)]) )
            self.assertTrue( not any([(i,True) in r for i in (0,1,4,5,6,8,9)]) )
        
        def test_multiple_boxes_no_overlap(self):
            # test that we infer nothing from multiple non-overlapping blocks
            cells = [None,None,None,None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertEquals([],r)
        
        def test_existing_block(self):
            # test that a single existing filled cell is handled correctly
            # in terms of block deduction
            cells = [None,None,None,None,True,None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(4,3))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (2,3,7,8)]) )
            self.assertTrue( not any([(i,True) in r for i in (0,1,4,5,6,9)]) )
        
        def test_existing_space(self):
            # test that a single existing empty cell is handled correctly
            # in terms of block deduction
            cells = [None,None,None,None,False,None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(4,3)) 
            while r is None:    
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (0,1,2,3,7)]) )
            self.assertTrue( not any([(i,True) in r for i in (4,5,6,8,9)]) )
            self.assertTrue( not any([(i,False) in r for i in (4,)]) )
        
        def test_single_block_already_in_position(self):
            # test that solver accepts a single block already in position
            # as the correct place for it
            cells = [None,True,True,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,))
            while r is None:
                r = proc.next()
            self.assertTrue( not any([(i,True) in r for i in range(6)]) )
        
        def test_one_of_multiple_blocks_in_position(self):
            # test that a single pre-solved block of multiple blocks is handled
            cells = [None,None,None,None,None,True,True,None]
            r = None
            proc = process_seq_fast(cells,(3,2))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (1,2)]) )
            self.assertTrue( not any([(i,True) in r for i in (0,3,4,5,6,7)]) )
        
        def test_all_of_multiple_blocks_in_position(self):
            # test that multiple pre-solved blocks are accepted
            cells = [None,True,True,None,None,True,True,True]
            r = None
            proc = process_seq_fast(cells,(2,3)) 
            while r is None:
                r = proc.next()
            self.assertTrue( not any([(i,True) in r for i in range(8)]) )
        
        def test_all_spaces_in_position(self):
            # test that blocks are filled where all spaces are pre-solved
            cells = [None,None,False,False,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,3))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (0,1,4,5,6)]) )
            self.assertTrue( not any([(i,True) in r for i in (2,3)]) )
            self.assertTrue( not any([(i,False) in r for i in (2,3)]) )
        
        def test_blank_cols(self):
            # test that the processor handles blank lines i.e. empty hint tuple
            r = None
            proc = process_seq_fast([False,False,None,None,False],())
            while r is None:
                r = proc.next()
            self.assertEquals([(2,False),(3,False)],r)
        
        def test_raises_exception_on_contradiction(self):
            # test that the processor raises ContradictionException if
            # it is impossible to fit the hinted blocks into the given cells
            def do_gen():
                r = None
                proc = process_seq_fast([None,None,True,None,False,None],(2,2))
                while r is None:
                    r = proc.next()
            self.assertRaises(ContradictionException,do_gen)
        
        def test_must_be_last_block_logic(self):
            # test that the processor takes into account that if there are
            # remaining filled cells after the intended position for the last
            # block, then it is not a valid position
            cells = [None,True,None,None,None,None,None,True]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertTrue( (6,True) in r )
            self.assertTrue( not any([(i,True) in r for i in (0,1,2,3,4,5,7)]) )
        
        def test_must_be_n_to_last_block_logic(self):
            # test that the processor takes into account that if the is an 
            # impossible configuration of filled cells after any intended
            # block position, it is not a valid position
            cells = [None,None,None,None,True,None,None,True,None,True]
            r = None
            proc = process_seq_fast(cells,(1,2,1))
            while r is None:
                r = proc.next()
            self.assertTrue( (6,True) in r )
            self.assertTrue( not any([(i,True) in r for i in (0,1,2,3,4,5,7,8,9)]) )
        
        def test_cover_filled_logic(self):
            # test that the processor backtracks on its assumptions if a 
            # filled cell would be left without a block covering it
            #
            # ||.| | |.|#|| |.| | | || 2,3
            #     ^ ^   !      ^ ^ ^
            cells = [False,None,None,False,True,None,False,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,3))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,True) in r for i in (5,7,8,9)]) )
            self.assertTrue( not any([(i,True) in r for i in (0,1,2,3,4,6)]) )
            self.assertTrue( not any([(i,False) in r for i in (0,3,6)]) )
        
        def test_spaces_decuded_before_definite_blocks(self):
            # test that the processor deduces that there must be a space 
            # before any fully-determined blocks
            cells = [None,None,None,None,True,True,None,None,True,None]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertTrue( (3,False) in r )
            self.assertFalse((7,False) in r )
        
        def test_spaces_deduced_after_definite_blocks(self):
            # test that the processor deduces that there must be a space
            # before any fully-determined blocks
            cells = [None,None,None,None,True,True,None,None,True,None]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertTrue( (6,False) in r )
            self.assertFalse( (9,False) in r )
        
        def test_no_duplicates_for_definite_block_spaces(self):
            # test that the processor does not return the same space
            # more than once where hints share a definite start/end space
            cells = [False,None,None,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertEquals(1, r.count((3,False)))
            
        def test_spaces_deduced_before_first_block(self):
            # test that the processor deduces that there can only be spaces
            # before the possible positions of the first hint block
            cells = [None,None,None,None,True,None,None,None,True,None]
            r = None
            proc = process_seq_fast(cells,(3,3))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,False) in r for i in (0,1)]) )
    
        def test_spaces_deduced_after_last_block(self):
            # test that the processor deduces that there can only be spaces
            # after the possible positions of the last hint block
            cells = [None,True,None,None,True,None,None,None]
            r = None
            proc = process_seq_fast(cells,(2,2))
            while r is None:
                r = proc.next()
            self.assertTrue( all([(i,False) in r for i in (6,7)]) )
            
    
    class TestAccurateSequenceProcessor(unittest.TestCase):
    
        def test_invokable(self):
            # test generator can be called
            r = None
            proc = process_seq_accurate([None]*10,DANCER[0][0])
            while r is None:
                r = proc.next()
                
        def test_returns_value(self):
            # test that method returns a list of 2-tuples
            r = None
            proc = process_seq_accurate([None,None,None,None,None],(3,))
            while r is None:
                r = proc.next()
            self.assertEquals(list,type(r))
            self.assertEquals(tuple,type(r[0]))
        
        def test_single_box(self):
            # test we can find the possible overlap of a single block
            cells = [None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(4,))
            while r is None:
                r = proc.next()
            self.assertEquals([(1,True),(2,True),(3,True)],r)
        
        def test_single_box_no_overlap(self):
            # test that nothing is inferred for a single block without overlapping possibilities
            cells = [None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(2,)) 
            while r is None:
                r = proc.next()
            self.assertEquals([],r)
                
        def test_multiple_boxes(self):
            # test we can find the possible overlap of multiple blocks
            cells = [None,None,None,None,None,None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(4,3)) 
            while r is None:
                r = proc.next()
            self.assertEquals([(2,True),(3,True),(7,True)],r)
        
        def test_multiple_boxes_no_overlap(self):
            # test that we infer nothing from multiple non-overlapping blocks
            cells = [None,None,None,None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(2,2)) 
            while r is None:
                r = proc.next()
            self.assertEquals([],r)
        
        def test_existing_block(self):
            # test that a single existing filled cell is handled correctly
            cells = [None,None,None,None,True,None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(4,3)) 
            while r is None:
                r = proc.next()
            self.assertEquals([(0,False),(2,True),(3,True),(7,True),(8,True)],r)
        
        def test_existing_space(self):
            # test that a single existing empty cell is handled correctly
            cells = [None,None,None,None,False,None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(4,3))
            while r is None:
                r = proc.next()
            self.assertEquals([(0,True),(1,True),(2,True),(3,True),(7,True)],r)
        
        def test_single_block_already_in_position(self):
            # test that the spaces are filled in for a single pre-solved block
            cells = [None,True,True,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(2,)) 
            while r is None:
                r = proc.next()
            self.assertEquals([(0,False),(3,False),(4,False),(5,False)],r)
        
        def test_one_of_multiple_blocks_in_position(self):
            # test that a single pre-solved block of multiple blocks is handled
            cells = [None,None,None,None,None,True,True,None]
            r = None
            proc = process_seq_accurate(cells,(3,2))
            while r is None:
                r = proc.next()
            self.assertEquals([(1,True),(2,True),(4,False),(7,False)],r)
        
        def test_all_of_multiple_blocks_in_position(self):
            # test that spaces are filled in for multiple pre-solved blocks
            cells = [None,True,True,None,None,True,True,True]
            r = None
            proc = process_seq_accurate(cells,(2,3))
            while r is None:
                r = proc.next()
            self.assertEquals([(0,False),(3,False),(4,False)],r)
        
        def test_all_spaces_in_position(self):
            # test that blocks are filled where all spaces are pre-solved
            cells = [None,None,False,False,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(2,3))
            while r is None:
                r = proc.next()
            self.assertEquals([(0,True),(1,True),(4,True),(5,True),(6,True)],r)
        
        def test_blank_cols(self):
            # test that the processor handles blank lines i.e. empty hint tuple
            r = None
            proc = process_seq_accurate([False,False,None,None,False],())
            while r is None:
                r = proc.next()
            self.assertEquals([(2,False),(3,False)],r)
        
        def test_raises_exception_on_contradiction(self):
            # test that the processor raises ContradictionException if
            # it is impossible to fit the hinted blocks into the given cells
            def do_gen():
                r = None
                proc = process_seq_accurate([None,None,True,None,False,None],(2,2))
                while r is None:
                    r = proc.next()
            self.assertRaises(ContradictionException,do_gen)
        
        def test_non_overlap_inferred_space(self):
            # test that we can infer spaces that wouldn't be inferred by a simple 
            # "push everything left then push everything right" technique, as described
            # here: http://www.comp.lancs.ac.uk/~ss/nonogram/ls-fast
            cells = [   
                        None,None,None,False,False,
                        True,True,True,True,True,
                        True,True,True,True,False,
                        False,False,False,False,False,
                        False,None,None,None,True,
                        False,None,False,None
                    ]
            r = None
            proc = process_seq_accurate(cells,(9,1,1,1))
            while r is None:
                r = proc.next()
            self.assertEquals([(0,False),(1,False),(2,False),(23,False)],r)
        
        def test_non_overlap_inferred_block(self):
            # test that we can infer blocks that wouldn't be inferred by a simple
            # "push everything left then push everything right" technique, as described
            # here: http://www.comp.lancs.ac.uk/~ss/nonogram/ls-fast
            cells = [
                        None,None,None,None,None,
                        None,None,None,None,None,
                        None,None,None,None,None,
                        True,False,None,False,False,
                        False,False,False,None,None,
                        None,None,None,None,True,
                        True,False,None,None,None,
                        None,None,None,False,False,
                        False,None,None,None,True,
                        False
                    ]
            r = None
            proc = process_seq_accurate(cells,(5,6,3,1,1))
            while r is None:
                r = proc.next()
            self.assertEquals([(9,False),(11,True),(12,True),(13,True),(14,True),
                                (17,False),(23,False),(24,False),(28,True),(43,False)],r)
        
        def test_splits_processing_accross_iterations(self):
            # test that it takes multiple iterations of the generator for the
            # processor to yield the result.
            cells = [None,None,None,None,None,None,None]
            r = None
            proc = process_seq_accurate(cells,(3,2))
            count = 0
            while r is None:
                r = proc.next()
                count += 1
            self.assertTrue( count > 1 )
            
        
    class TestSolver(unittest.TestCase):
                
        def seqpri(self,stack,board,cols,rows):
            return stack.pop()
        
        def fill_nothing_gen(self,cells,hint):
            yield []
                
        def fill_blanks_gen(self,cells,hint):
            ret = []
            for i in range(len(cells)):
                if cells[i]==None:
                    ret.append((i,True))
            yield ret
                
        def test_returns_board_and_flag(self):
            # test that the returned value (on success) is
            # board consisting of a nested list of booleans
            # and 'solved' boolean
            s = mock.Mock(side_effect=self.fill_blanks_gen)
            result = None
            slv = solve(DANCER[0],DANCER[1],None,False,[s],self.seqpri)
            while result is None:
                result = slv.next()
            self.assertEquals(tuple, type(result))
            self.assertEquals(2, len(result))
            self.assertEquals(list, type(result[0]))
            for row in result[0]:
                self.assertEquals(list, type(row))
                for val in row:
                    self.assertEquals(bool, type(val))
            self.assertEquals(bool, type(result[1]))
        
        def test_returns_correct_size(self):
            # test that the nested list returned is the size of board
            s = mock.Mock(side_effect=self.fill_blanks_gen)
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            self.assertEquals(10,len(result))
            for row in result:
                self.assertEquals(5,len(row))
        
        def test_returns_correct_size_2(self):
            # test returned board size with different values
            s = mock.Mock(side_effect=self.fill_blanks_gen)
            res = None
            proc = solve(CAT[0],CAT[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            self.assertEquals(20,len(result))
            for row in result:
                self.assertEquals(20,len(row))
        
        def test_tries_every_row_and_col(self):
            # test that the processor is invoked exactly once 
            # for each row and col (for a do-nothing processor, 
            # guessing disabled)
            s = mock.Mock(side_effect=self.fill_nothing_gen)
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            self.assertEquals(10+5,len(s.call_args_list))
            for col in DANCER[0]:
                self.assertTrue((([None]*10,col),{}) in s.call_args_list)
            for row in DANCER[1]:
                self.assertTrue((([None]*5,row),{}) in s.call_args_list)
        
        def test_stores_seqproc_results(self):
            # test that the processor's results are reflected in
            # the returned board
            #        7
            #    0 1 2 3 4 
            #   0
            #21 1    F T T
            #   2
            #   3    T
            #   4
            #   5
            #   6    F
            #   7
            #   8           
            #   9
            def processor_gen(cells,hint):
                if len(cells)==10 and hint == (7,):
                    yield [(3,True),(6,False)]
                elif len(cells)==5 and hint == (2,1):
                    yield [(2,False),(3,True),(4,True)]
                else:
                    yield []
                
            s = mock.Mock(side_effect=processor_gen)
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            
            self.assertEquals([None,False,None,True,None,None,False,None,None,None],[r[2] for r in result] )
            self.assertEquals( [None,None,False,True,True], result[1] )
            self.assertEquals( [None,None,None,None,None,None,None,None,None,None],[r[0] for r in result] )
            self.assertEquals( [None,None,None,None,None],result[4] )
        
        def test_seqproc_causes_re_process(self):
            # test that for each sequence processor result, the corresponding
            # row/col is processed again with the new information, in any order
            #         2
            #         1   1 2
            #         3 7 3 1
            #
            #       0 1 2 3 4
            #     0
            # 21  1      >T>T
            #     2     v
            #  3  3  >F T
            #     4
            #     5     v
            #  2  6     F
            #     7
            #     8
            #     9
            class Processor(object):
                def __init__(self):
                    self.done_7_col = False
                    self.done_21_row = False
                    self.done_3_row = False
                def processor_gen(self,cells,hint):
                    if len(cells)==10 and hint==(7,) and not self.done_7_col:
                        self.done_7_col = True
                        yield [(3,True),(6,False)]
                    elif len(cells)==5 and hint==(2,1) and not self.done_21_row:
                        self.done_21_row = True
                        yield [(3,True),(4,True)]
                    elif len(cells)==5 and hint==(3,) and not self.done_3_row and cells[2]==True:
                        self.done_3_row = True
                        yield [(1,False)]
                    else:
                        yield []
                                
            s = mock.Mock(side_effect=Processor().processor_gen)
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res

            self.assertTrue((([None,None,None,None,None,None,None,None,None,None],(7,)),{}) in s.call_args_list)
            self.assertTrue((([None,None,None,None,None],(2,1)),{}) in s.call_args_list)
            
            self.assertTrue((([None,None,True,None,None],(3,)),{}) in s.call_args_list)
            self.assertTrue((([None,None,False,None,None],(2,)),{}) in s.call_args_list)
            
            self.assertTrue((([None,True,None,None,None,None,None,None,None,None],(1,3)),{}) in s.call_args_list)
            self.assertTrue((([None,True,None,None,None,None,None,None,None,None],(2,1)),{}) in s.call_args_list)
            
            self.assertTrue((([None,None,None,False,None,None,None,None,None,None],(2,1,3)),{}) in s.call_args_list)
        
        def test_makes_guess(self):
            # test that the solver guesses the state of unknown cells when 
            # line-solving is exhausted
            
            def processor_gen(cells,hints):
                deduced = {
                    (5,(2,2)):  [True,True,False,True,True],
                    (5,()):     [False,False,False,False,False],
                    (5,(1,1)):  [None,None,False,None,None],
                    (5,(3,)):   [None,None,True,None,None],
                    (6,(3,1)):  [True,True,True,False,None,None],
                    (6,(1,)):   [False,False,False,False,False,True],
                }[len(cells),hints]
                r = []
                for i,c in enumerate(cells):
                    if c is None and deduced[i] is not None:
                        r.append((i,deduced[i]))
                yield r 
        
            s = mock.Mock(side_effect=processor_gen)
            try:
                res = None
                proc = solve(SMILEY5X6[0],SMILEY5X6[1],-1,False,[s],self.seqpri)
                while res is None:
                    res = proc.next()
                result,solved = res
            except: pass
            self.assertEquals(1, s.call_args_list.count( (([True,None,False,None,None],(1,1)),{}) ))
        
        def test_works_off_guess(self):
            # test that the solver tries to line-solve after guessing
        
            def processor_gen(cells,hints):
                deduced = {
                    (5,(2,2)):  [True,True,False,True,True],
                    (5,()):     [False,False,False,False,False],
                    (5,(1,1)):  [None,None,False,None,None],
                    (5,(3,)):   [None,None,True,None,None],
                    (6,(3,1)):  [True,True,True,False,None,None],
                    (6,(1,)):   [False,False,False,False,False,True],
                }[len(cells),hints]
                r = []
                for i,c in enumerate(cells):
                    if c is None and deduced[i] is not None:
                        r.append((i,deduced[i]))
                yield r 
        
            s = mock.Mock(side_effect=processor_gen)
            try:
                res = None
                proc = solve(SMILEY5X6[0],SMILEY5X6[1],-1,False,[s],self.seqpri)
                while res is None:
                    res = proc.next()
                result,solved = res
            except: pass
            self.assertTrue( (([True,True,True,False,True,None],(3,1)),{}) in s.call_args_list )
            self.assertTrue( (([True,None,False,None,None],(1,1)),{}) in s.call_args_list )
        
        class GuessProcessor(object):
        
            def __init__(self,cols,rows,solution,guesses,on_guess):
                self.cols = cols
                self.rows = rows
                self.solution = solution
                self.guesses = guesses
                self.current_guess = None
                self.on_guess = on_guess
                
            def processor_gen(self,cells,hints):
                # establish list of cell coords
                if len(cells)==len(self.cols):
                    rownum = self.rows.index(hints)
                    s = [(rownum,i) for i in range(len(cells))]
                else:
                    colnum = self.cols.index(hints)
                    s = [(i,colnum) for i in range(len(cells))]
                # check if call includes guess
                guessed = []
                for i,(r,c) in enumerate(s):
                    for g,guess in enumerate(self.guesses):
                        if guess[r][c]==True and cells[i] is not None:
                            guessed.append((g,i,r,c))
                # its a guess if there is exactly 1 cell in sequence which is 
                # known in a guess-only area
                if len(guessed) == 1:
                    g,i,r,c = guessed[0]
                    self.current_guess = g
                    self.on_guess(g, self.solution[r][c] == cells[i])

                # assemble return value
                res = []
                for i,(r,c) in enumerate(s):
                    otherguesses = range(len(self.guesses))
                    if self.current_guess is not None:
                        otherguesses.remove(self.current_guess)
                    if( cells[i] is None and not any(
                            [self.guesses[g][r][c] for g in otherguesses]) ):
                        res.append((i,self.solution[r][c]))
                yield res
    
        def test_accepts_guess_with_1_contradiction(self):
            # test that puzzle is solved if 1 guess holds true
            # and the other is contradictory
            
            def on_guess(g,correct):
                if not correct:
                    raise ContradictionException()
                            
            p = TestSolver.GuessProcessor(UHINT_GUESS[0],UHINT_GUESS[1],
                    UHINT_GUESS_SOL, UHINT_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            res = None
            proc = solve(UHINT_GUESS[0],UHINT_GUESS[1],-1,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            self.assertEquals(True,solved)
        
        def test_rejects_guess_with_2_contradictions(self):
            # tests that the solver raises exception if it encounters
            # a contradiction for both of its guesses
        
            def on_guess(g,correct):
                raise ContradictionException()
                            
            p = TestSolver.GuessProcessor(UHINT_GUESS[0],UHINT_GUESS[1],
                    UHINT_GUESS_SOL, UHINT_GUESS_GS, on_guess)          
            s = mock.Mock(side_effect=p.processor_gen)
            
            def do_gen():
                res = None
                proc = solve(UHINT_GUESS[0],UHINT_GUESS[1],-1,False,[s],self.seqpri)
                while res is None:
                    res = proc.next()
            self.assertRaises(ContradictionException,do_gen)
        
        def test_throws_ambiguous_for_2_solutions(self):
            # test that the solver throws an exception if it finds a 
            # solution for both of its two guesses
                            
            p = TestSolver.GuessProcessor(UHINT_GUESS[0],UHINT_GUESS[1],
                    UHINT_GUESS_SOL, UHINT_GUESS_GS, lambda g,c: None)
            s = mock.Mock(side_effect=p.processor_gen)
            
            def do_gen():
                res = None
                proc = solve(UHINT_GUESS[0],UHINT_GUESS[1],-1,False,[s],self.seqpri)
                while res is None:
                    res = proc.next()
            self.assertRaises(AmbiguousException,do_gen)
        
        def test_recursive_guessing(self):
            # test that if the solver fails to line-solve after a guess,
            # it makes further guesses
            
            guessed = set([])
            
            def on_guess(g,correct):
                if not correct:
                    raise ContradictionException()
                guessed.add(g)
            
            p = TestSolver.GuessProcessor(UHINT_2_GUESS[0],UHINT_2_GUESS[1],
                    UHINT_2_GUESS_SOL, UHINT_2_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            
            res = None
            proc = solve(UHINT_2_GUESS[0],UHINT_2_GUESS[1],-1,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            
            self.assertEquals(True,solved)
            self.assertTrue( 0 in guessed )
            self.assertTrue( 1 in guessed )
        
        def test_discard_guess_on_recursive_contradiction(self):
            # test that that if the solver gets 2 contradictions for a
            # recursive guess, it unwinds and recurses on the other guess
            # instead
            
            guessstate = [0]
            
            def on_guess(g,correct):
                # guess area 0, first guess
                if g==0 and guessstate[0]<=1:
                    guessstate[0] = 1
                # guess area 1, context of first guess
                elif g==1 and guessstate[0]<=2:
                    guessstate[0] = 2
                    # wrong guess is wrong
                    if not correct: raise ContradictionException()
                # guess area 0, second guess
                elif g==0 and guessstate[0]>=2:
                    guessstate[0] = 3
                # guess area 1, context of second guess
                elif g==1 and guessstate[0]>=3:
                    guessstate[0] = 4
                    # both guesses are wrong
                    raise ContradictionException()
            
            p = TestSolver.GuessProcessor(UHINT_2_GUESS[0],UHINT_2_GUESS[1],
                    UHINT_2_GUESS_SOL, UHINT_2_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            
            res = None
            proc = solve(UHINT_2_GUESS[0],UHINT_2_GUESS[1],-1,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result,solved = res
            
            self.assertEquals(True,solved)
        
        def test_raise_ambiguous_on_recursive_ambiguous(self):
            # test that the solver raises ambiguous exception if a recursive
            # guess yields ambiguity
            
            guessstate = [0]
            
            def on_guess(g,correct):
                # guess area 0, first guess
                if g==0 and guessstate[0]<=1:
                    guessstate[0] = 1
                # guess area 1, context of first guess
                elif g==1 and guessstate[0]<=2:
                    guessstate[0] = 2
                    # wrong guess is wrong
                    if not correct: raise ContradictionException()
                # guess area 0, second guess
                elif g==0 and guessstate[0]>=2:
                    guessstate[0] = 3
                # guess area 1, context of second guess
                elif g==1 and guessstate[0]>=3:
                    guessstate[0] = 4
                    # both guesses are correct
                
            p = TestSolver.GuessProcessor(UHINT_2_GUESS[0],UHINT_2_GUESS[1],
                    UHINT_2_GUESS_SOL, UHINT_2_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            
            def do_gen():
                res = None
                proc = solve(UHINT_2_GUESS[0],UHINT_2_GUESS[1],-1,False,[s],self.seqpri)
                while res is None:
                    res = proc.next()
            self.assertRaises(AmbiguousException,do_gen)
        
        def test_return_value_for_guess_recursion(self):
            # test the solver returns the solution in the correct format after
            # recursing for guesses
            
            guessstate = [0]
            
            def on_guess(g,correct):
                # guess area 0, first guess
                if g==0 and guessstate[0]<=1:
                    guessstate[0] = 1
                # guess area 1, context of first guess
                elif g==1 and guessstate[0]<=2:
                    guessstate[0] = 2
                    # wrong guess is wrong
                    if not correct: raise ContradictionException()
                # guess area 0, second guess
                elif g==0 and guessstate[0]>=2:
                    guessstate[0] = 3
                # guess area 1, context of second guess
                elif g==1 and guessstate[0]>=3:
                    guessstate[0] = 4
                    # both guesses are wrong
                    raise ContradictionException()
                    
            p = TestSolver.GuessProcessor(UHINT_2_GUESS[0], UHINT_2_GUESS[1],
                    UHINT_2_GUESS_SOL, UHINT_2_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            
            res = None
            proc = solve(UHINT_2_GUESS[0],UHINT_2_GUESS[1],-1,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
            result = res
            
            self.assertEquals(tuple,type(result))
            self.assertEquals(2,len(result))
            self.assertEquals(list,type(result[0]))
            self.assertEquals(bool,type(result[1]))
        
        def test_uses_seq_pri_strategy(self):
            # test that solver uses supplied sequence priority strategy
            # to determine order that rows and cols are checked
                        
            order = [(ROW,6),(COL,1),(ROW,9),(COL,3),(COL,4),(ROW,0),(ROW,3),
                (ROW,1),(ROW,2),(ROW,4),(COL,2),(ROW,5),(ROW,7),(COL,0),(ROW,8)]
    
            def stgy(stack,board,cols,rows):
                stack.sort(key=lambda i: order.index(i), reverse=True)
                return stack.pop()
    
            s = mock.Mock(side_effect=self.fill_nothing_gen)
            p = mock.Mock(side_effect=stgy)
            
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s],p)
            while res is None:
                res = proc.next()

            self.assertEquals(len(order), len(s.call_args_list))
            
            hints_ordered = [DANCER[0][num] if rc==COL else DANCER[1][num] for rc,num in order]
            hints_passed = [args[0][1] for args in s.call_args_list]
            self.assertEquals(hints_ordered, hints_passed)
        
        def test_uses_multiple_seq_processors(self):
            # test that the solver uses the sequence processors specified
            # in the list. They should be used in order.
            
            calls = []
            
            def solver1_gen(cells,hints):
                calls.append((1,cells,hints))
                yield []
            def solver2_gen(cells,hints):
                calls.append((2,cells,hints))
                yield []
            
            s1 = mock.Mock(side_effect=solver1_gen)
            s2 = mock.Mock(side_effect=solver2_gen)
            
            res = None
            proc = solve(DANCER[0],DANCER[1],None,False,[s1,s2],self.seqpri)
            while res is None:
                res = proc.next()
            
            crlen = len(DANCER[0])+len(DANCER[1])
            self.assertEquals(2*crlen, len(calls))
            for i in calls[0:crlen]:
                self.assertEquals(1,i[0])
            for i in calls[crlen:]:
                self.assertEquals(2,i[0])
                
        def test_uses_sequence_cache_when_enabled(self):
            # test that the solver caches sequence results and reads 
            # them before invoking the line-solver, if caching selected
            
            def processor_gen(cells,hints):
                # blank 4-hint yields solved mid 3 cells
                if (cells,hints) == ([None,None,None,None,None],(4,)):
                    yield [(1,True),(2,True),(3,True)]
                # 5-hint with 2nd solved, as a result of 4-hint
                elif (cells,hints) == ([None,True,None,None,None],(5,)):
                    yield [(0,True),(2,True),(3,True)]
                # yield nothing for other queries
                else:
                    yield []    
            
            s = mock.Mock(side_effect=processor_gen)
            
            res = None
            proc = solve(HEART[0],HEART[1],None,True,[s],self.seqpri)
            while res is None:
                res = proc.next()
                
            self.assertEquals(1,s.call_args_list.count( (([None,None,None,None,None],(4,)),{}) ))
            self.assertEquals(1,s.call_args_list.count( (([None,None,None,None,None],(5,)),{}) ))
            self.assertEquals(1,s.call_args_list.count( (([None,None,None,True,None],(5,)),{}) ))
            for item in s.call_args_list:
                self.assertEquals(1,s.call_args_list.count(item))
        
        def test_doesnt_use_sequence_cache_when_disabled(self):
            # test that the solver doesn't cache sequence processor
            # results if caching is disabled
            
            def processor_gen(cells,hints):
                # blank 4-hint yields solved mid 3 cells
                if (cells,hints) == ([None,None,None,None,None],(4,)):
                    yield [(1,True),(2,True),(3,True)]
                # 5-hint with 2nd solved, as a result of 4-hint
                elif (cells,hints) == ([None,True,None,None,None],(5,)):
                    yield [(0,True),(2,True),(3,True)]
                # yield nothing for other queries
                else:
                    yield []    
            
            s = mock.Mock(side_effect=processor_gen)
            
            res = None
            proc = solve(HEART[0],HEART[1],None,False,[s],self.seqpri)
            while res is None:
                res = proc.next()
                
            self.assertGreater(s.call_args_list.count( (([None,None,None,None,None],(4,)),{}) ),1)
            self.assertGreater(s.call_args_list.count( (([None,None,None,True,None],(5,)),{}) ),1)

        def test_throws_guesses_exceeded_exception(self):
            # test that the solver throws GuessesExceededException if
            # it cannot solve the puzzle after making the specified
            # number of guesses
            
            guessed = []
            
            def on_guess(g,correct):
                if not correct:
                    raise ContradictionException()
                guessed.append(g)
            
            p = TestSolver.GuessProcessor(UHINT_2_GUESS[0],UHINT_2_GUESS[1],
                    UHINT_2_GUESS_SOL, UHINT_2_GUESS_GS, on_guess)
            s = mock.Mock(side_effect=p.processor_gen)
            
            def do_solve():
                res = None
                proc = solve(UHINT_2_GUESS[0],UHINT_2_GUESS[1],1,
                    False,[s],self.seqpri)
                while res is None:  
                    res = proc.next()
            
            self.assertRaises(GuessesExceededException,do_solve)


    class TestHeuristicSeqPriority(unittest.TestCase):
    
        def test_returns_highest_rated(self):
        
            board = [   [None,None,None,None],
                        [None,None,None,None],
                        [None,None,None,None]   ]
            cols = [(3,),(2,),(1,),()]
            rows = [(1,),(2,),(3,)]
            stack = [(COL,0),(ROW,0),(ROW,1),(COL,1),(COL,2)]
            
            def hstc(length,hints):
                return {
                    (3,(3,)): 10,
                    (3,(2,)): 20,
                    (3,(1,)): 3,
                    (3,()): 55,
                    (4,(1,)): 16,
                    (4,(2,)): 8,
                    (4,(3,)): 32,
                }[length,hints]
        
            result = make_heuristic_seq_pri(hstc)(stack,board,cols,rows)
            self.assertEquals((COL,1),result)
            
            
    class TestSolvabilityHeuristic(unittest.TestCase):
        #T=(n+1)*sum(i=1,n,a[i])+n*(n-L-1)
        
        def test_empty_line(self):
            # test heuristic returns length of line, if empty
            result = est_seq_solvability(5,())
            self.assertEquals(5,result)

        def test_full_line(self):
            # test heuristic returns length of line, if full
            result = est_seq_solvability(5,(5,))
            self.assertEquals(5,result)         
                        
        def test_solvability_some_vs_none(self):
            # test heuristic returns higher score if line is solvable than
            # when it isn't
            result_a = est_seq_solvability(10,(3,4))
            result_b = est_seq_solvability(6,(2,))
            self.assertTrue(result_a > result_b)
                        
        def test_solvability_some_vs_more(self):
            # test that the heuristic returns gives higher score for more
            # solvable line where both are solvable
            result_a = est_seq_solvability(6,(2,2))
            result_b = est_seq_solvability(10,(3,4))
            self.assertTrue(result_b > result_a)
            
        def test_solvability_easy_vs_hard(self):
            # test that heuristic returns higher score for line that takes
            # less effort to solve for the same number of filled cells.
            #    | | | | |#|#| | | | |  6
            #    | | | | | | |#|#| | |  1,1,4
            result_a = est_seq_solvability(10,(6,))
            result_b = est_seq_solvability(10,(1,1,4))
            self.assertTrue(result_a > result_b)


    HEART_PUZZLE = puzzle.Puzzle()
    HEART_PUZZLE.name = "Heart"
    HEART_PUZZLE.width = 5
    HEART_PUZZLE.height = 5
    HEART_PUZZLE.cells = [
        [ (False,(1,1,1)),(True,(1,0,0)),(False,(1,1,1)),(True,(1,0,0)),(False,(1,1,1)) ],
        [ (True,(1,0,0)),(True,(1,0.5,0.5)),(True,(1,0,0)),(True,(1,0,0)),(True,(0.5,0,0)) ],
        [ (True,(1,0,0)),(True,(1,0,0)),(True,(1,0,0)),(True,(1,0,0)),(True,(0.5,0,0)) ],
        [ (False,(1,1,1)),(True,(1,0,0)),(True,(1,0,0)),(True,(0.5,0,0)),(False,(1,1,1)) ],
        [ (False,(1,1,1)),(False,(1,1,1)),(True,(0.5,0,0)),(False,(1,1,1)),(False,(1,1,1)) ]
    ]
    HEART_PUZZLE.row_numbers = [(1,1),(5,),(5,),(3,),(1,)]
    HEART_PUZZLE.column_numbers = [(2,),(4,),(4,),(4,),(2,)]
            

    class TestPuzzleVerifier(unittest.TestCase):
    
        def test_hints_extracted(self):
            # test that the wrapper extracts the puzzle hints and passes them
            # to the solver correctly
            
            def svr_gen(cols,rows):
                yield
                yield
                yield [[None]*5]*5,False
            
            s = mock.Mock(side_effect=svr_gen)
            
            p = HEART_PUZZLE

            res = None
            proc = verify_puzzle(p,s)
            while res is None:
                res = proc.next()
            
            self.assertEquals(1,len(s.call_args_list))
            self.assertEquals( (([(2,),(4,),(4,),(4,),(2,)],[(1,1),(5,),(5,),(3,),(1,)]),{}),
                s.call_args_list[0] )
        
        def test_solved_returned(self):
            # test that the wrapper correctly yields the board's solved status
            
            def svr_gen(cols,rows):
                yield
                yield HEART_SOL,True
                
            s = mock.Mock(side_effect=svr_gen)
            p = HEART_PUZZLE
            
            res = None
            proc = verify_puzzle(p,s)
            while res is None:
                res = proc.next()
                
            self.assertEquals(True, res)
                        
        def test_contradiction_exception_raised(self):
            # test that wrapper allows ContradictionException to bubble up
            
            def svr_gen(cols,rows):
                yield
                raise ContradictionException()
                
            s = mock.Mock(side_effect=svr_gen)
            p = HEART_PUZZLE
                        
            def do_gen():
                res = None
                proc = verify_puzzle(p,s)
                while res is None:
                    res = proc.next()
                    
            self.assertRaises(ContradictionException,do_gen)
            
        def test_ambiguous_exception_raised(self):
            # test that the wrapper allows AmbiguousException to bubble up
                        
            def svr_gen(cols,rows):
                yield
                raise AmbiguousException()
                
            s = mock.Mock(side_effect=svr_gen)
            p = HEART_PUZZLE
            
            def do_gen():
                res = None
                proc = verify_puzzle(p,s)
                while res is None:
                    res = proc.next()
                    
            self.assertRaises(AmbiguousException,do_gen)
                        
        def test_guesses_exceeded_exception_raised(self):
            # test that the wrapper allows GuessesExceededException to bubble up
            
            def svr_gen(cols,rows):
                yield
                raise GuessesExceededException()
                
            s = mock.Mock(side_effect=svr_gen)
            
            p = HEART_PUZZLE
            
            def do_gen():
                res = None
                proc = verify_puzzle(p,s)
                while res is None:
                    res = proc.next()
                    
            self.assertRaises(GuessesExceededException,do_gen)
            
                        
    unittest.main()
