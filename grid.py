# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 12:53:01 2013

@author: Jarek
"""

# TODO: Check for three adjacent to indecisive two; two adjacent indecisive twos.
# TODO: Guessing/backtracking
# TODO: Count loose ends in area (might be hard this one..)

import sys
if sys.version_info >= (3, 0):
    import tkinter as tk
else:
    import Tkinter as tk


class Grid:

    LINE_KEYS = {
        'NO_LINE':0,
        'LINE':1,
        'NOT_ALLOWED':2
    }
    CORNER_KEYS = {
        'TOP_LEFT':0,
        'TOP_RIGHT':1,
        'BOT_LEFT':2,
        'BOT_RIGHT':3
    }
    CELL_POS_OVER_CORNER = {
        0:{'row':-1,'col':-1},
        1:{'row':-1,'col':1},
        2:{'row':1,'col':-1},
        3:{'row':1,'col':1}
    }
    DIRECTION_KEYS = {
        'LEFT':0,
        'UP':1,
        'DOWN':2,
        'RIGHT':3
    }
    POS_IN_DIRECTION = {
        0:{'row':0,'col':-1},
        1:{'row':-1,'col':0},
        2:{'row':1,'col':0},
        3:{'row':0,'col':1}
    }
    LINE_POS_FROM_DOT_IN_DIRECTION = {
        0:{'row':0,'col':-1,'vertical':False},
        1:{'row':-1,'col':0,'vertical':True},
        2:{'row':0,'col':0,'vertical':True},
        3:{'row':0,'col':0,'vertical':False}
    }

    @staticmethod
    def getOppositeCorner(corner):
        return 3-corner #Relying on key value constants beings set as above!!
    @staticmethod
    def getOtherCornerOnVertical(corner):
        if(corner<2):
            return corner + 2
        return corner - 2
    @staticmethod
    def getOppositeDirection(direction):
        return 3-direction #Relying on key value constants beings set as above!!

    def getCellVal(self, r, c):
        if r>=0 and c>=0 and r<self.ROWS and c<self.COLS:
            return self.cells[r][c]
        else:
            # Out of bounds! No cell exists here, so return something to reflect this.
            return ' '

    def clearCellVal(self, r, c):
        '''Useful once a cell's value can no longer provide any useful information'''
        self.cells[r][c] = ' '

    def getLineVal(self, r, c, vertical):
        if r>=0 and c>=0 and r<self.ROWS+1*(not vertical) and c<self.COLS+1*vertical:
            if(vertical):
                return self.vlines[r][c]
            else:
                return self.hlines[r][c]
        else:
            # Out of bounds! Line cannot go here, so return something to reflect this.
            return Grid.LINE_KEYS['NOT_ALLOWED']

    def setLineVal(self, r, c, vertical, val, overwrite):
        '''Sets a line's value. If overwrite is False, will only work if line is set to 'NO_LINE'''
        if(overwrite or self.getLineVal(r,c,vertical)==Grid.LINE_KEYS['NO_LINE']):
            col = self.BGCOL
            txt = '   '
            if(val==Grid.LINE_KEYS['LINE']):
                col = self.FGCOL
            elif(val==Grid.LINE_KEYS['NOT_ALLOWED']):
                txt = 'X'
            if r>=0 and c>=0 and r<self.ROWS+1*(not vertical) and c<self.COLS+1*vertical:
                if(vertical):
                    self.vlines[r][c] = val
                    self.vlinelabels[r][c].configure(bg=col,text=txt)
                else:
                    self.hlines[r][c] = val
                    self.hlinelabels[r][c].configure(bg=col,text=txt)

    def countLinesSurroundingCell(self, r, c, key):
        '''Counts the number of lines/blanks/notAlloweds surrounding a given cell'''
        count = 0
        if(self.getLineVal(r,c,True)==key): count=count+1
        if(self.getLineVal(r,c+1,True)==key): count=count+1
        if(self.getLineVal(r,c,False)==key): count=count+1
        if(self.getLineVal(r+1,c,False)==key): count=count+1
        return count

    def setLinesSurroundingCell(self, r, c, key):
        '''Sets the lines surrounding a given cell to the key iff they haven't been set yet'''
        self.setLineVal(r, c, True, key, False)
        self.setLineVal(r, c+1, True, key, False)
        self.setLineVal(r, c, False, key, False)
        self.setLineVal(r+1, c, False, key, False)
        # Clear the cell value as it will not need to be checked again.
        self.clearCellVal(r, c)

    def countLinesSurroundingDot(self, r, c, key):
        '''Counts the number of lines/blanks/notAlloweds surrounding a given dot'''
        count = 0
        if(self.getLineVal(r,c,True)==key): count=count+1
        if(self.getLineVal(r-1,c,True)==key): count=count+1
        if(self.getLineVal(r,c,False)==key): count=count+1
        if(self.getLineVal(r,c-1,False)==key): count=count+1
        return count

    def setLinesSurroundingDot(self, r, c, key):
        '''Sets the lines surrounding a given dot to the key iff they haven't been set yet'''
        self.setLineVal(r, c, True, key, False)
        self.setLineVal(r-1, c, True, key, False)
        self.setLineVal(r, c, False, key, False)
        self.setLineVal(r, c-1, False, key, False)

    def countCornerLinesInner(self, r, c, corner, key):
        '''Counts the number of lines/blanks/notAlloweds in a given corner of a given cell'''
        count = 0
        if(corner==self.CORNER_KEYS['TOP_LEFT'] or corner==self.CORNER_KEYS['BOT_LEFT']):
            if(self.getLineVal(r,c,True)==key): count=count+1
        else:
            if(self.getLineVal(r,c+1,True)==key): count=count+1
        if(corner==self.CORNER_KEYS['TOP_LEFT'] or corner==self.CORNER_KEYS['TOP_RIGHT']):
            if(self.getLineVal(r,c,False)==key): count=count+1
        else:
            if(self.getLineVal(r+1,c,False)==key): count=count+1
        return count

    def setCornerLinesInner(self, r, c, corner, key):
        '''Sets the lines in a given corner of a given cell to the key iff they haven't been set yet'''
        if(corner==self.CORNER_KEYS['TOP_LEFT'] or corner==self.CORNER_KEYS['BOT_LEFT']):
            self.setLineVal(r, c, True, key, False)
        else:
            self.setLineVal(r, c+1, True, key, False)
        if(corner==self.CORNER_KEYS['TOP_LEFT'] or corner==self.CORNER_KEYS['TOP_RIGHT']):
            self.setLineVal(r, c, False, key, False)
        else:
            self.setLineVal(r+1, c, False, key, False)

    def countCornerLinesOuter(self, r, c, corner, key):
        '''Counts the number of lines/blanks/notAlloweds coming out of a given corner of a given cell'''
        return self.countCornerLinesInner(r+self.CELL_POS_OVER_CORNER[corner]['row'], c+self.CELL_POS_OVER_CORNER[corner]['col'], Grid.getOppositeCorner(corner), key)

    def setCornerLinesOuter(self, r, c, corner, key):
        '''Sets the lines coming out of a given corner of a given cell to the key iff they haven't been set yet'''
        self.setCornerLinesInner(r+self.CELL_POS_OVER_CORNER[corner]['row'], c+self.CELL_POS_OVER_CORNER[corner]['col'], Grid.getOppositeCorner(corner), key)

    def sendLineOutThroughCorner(self, r, c, corner):
        '''Accepts assumption that a line will be coming into a given cell through a given corner'''
        # Move into next cell.
        r = r + self.CELL_POS_OVER_CORNER[corner]['row']
        c = c + self.CELL_POS_OVER_CORNER[corner]['col']
        corner = Grid.getOppositeCorner(corner)
        if(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==1):
            self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])
        elif(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])==1):
            self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
        val = self.getCellVal(r, c)
        if(val!=' '):
            if(val=='1'):
                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])
            if(val=='2'):
                if(self.countCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])==1):
                    self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])
                elif(self.countCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])==1):
                    self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])
                self.sendLineOutThroughCorner(r, c, Grid.getOppositeCorner(corner))
            if(val=='3'):
                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])

    def cornerCounterProof(self, r, c, corner):
        '''Tries to prove that a given corner cannot go at a given location'''
        # Move into next cell.
        r = r + self.CELL_POS_OVER_CORNER[corner]['row']
        c = c + self.CELL_POS_OVER_CORNER[corner]['col']
        val = self.getCellVal(r, c)
        if(val!=' '):
            if(val=='1'):
                if(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==2):
                    return True
            if(val=='2'):
                if(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])>=1):
                    return True
                return self.cornerCounterProof(r, c, corner)
            if(val=='3'):
                return True
        return False

    def indecisiveTwo(self, r, c, corner, assumeUniqueSoln):
        '''Accepts assumption that a two in a given cell must either face or face away from a given corner'''
        # Send lines out from other two corners.
        self.sendLineOutThroughCorner(r, c, Grid.getOtherCornerOnVertical(corner))
        self.sendLineOutThroughCorner(r, c, Grid.getOtherCornerOnVertical(Grid.getOppositeCorner(corner)))
        # If assuming a unique solution exists, check if there are any numbers adcjacent to this two.
        # If there are none, then set the two into the corner and add another corner that 'forces' the two
        # to take this alternative (logic: if there weren't, there'd be more than one solution).
        if(assumeUniqueSoln):
            numAdjacentNumbers = 0
            for d in range(4):
                if(self.getCellVal(r+self.POS_IN_DIRECTION[d]['row'], c+self.POS_IN_DIRECTION[d]['col'])!=' '):
                    numAdjacentNumbers += 1
            if(numAdjacentNumbers==0):
                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])
                self.setCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['LINE'])
                return
        # Move into next cell.
        r = r + self.CELL_POS_OVER_CORNER[corner]['row']
        c = c + self.CELL_POS_OVER_CORNER[corner]['col']
        corner = Grid.getOppositeCorner(corner)
        if(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==1):
            self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
        elif(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])==1):
            self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])
        else:
            val = self.getCellVal(r, c)
            if(val!=' '):
                if(val=='1'):
                    self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
                if(val=='2'):
                    self.indecisiveTwo(r, c, Grid.getOppositeCorner(corner), assumeUniqueSoln)
                if(val=='3'):
                    self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])

    def findOtherEnd(self, r, c, cameFrom):
        for d in range(4):
            rx = r + self.LINE_POS_FROM_DOT_IN_DIRECTION[d]['row']
            cx = c + self.LINE_POS_FROM_DOT_IN_DIRECTION[d]['col']
            if(self.getLineVal(rx,cx,self.LINE_POS_FROM_DOT_IN_DIRECTION[d]['vertical'])==Grid.LINE_KEYS['LINE'] and
              d!=cameFrom):
                rx = r + self.POS_IN_DIRECTION[d]['row']
                cx = c + self.POS_IN_DIRECTION[d]['col']
                if(self.countLinesSurroundingDot(rx, cx, Grid.LINE_KEYS['LINE'])==1):
                    return [rx, cx]
                else:
                    return self.findOtherEnd(rx, cx, Grid.getOppositeDirection(d))
                break


    def solve(self, assumeUniqueSoln=True):
        numUnresolvesNumbers = 0
        # Iterate over every cell and for those with values, try do something
        for r in range(self.ROWS):
            for c in range(self.COLS):
                val = self.getCellVal(r, c)
                if(val!=' '):
                    numUnresolvesNumbers += 1
                    # Most basic check: See if there is only one way to satisfy
                    # a value's rule. If so, draw the appropriate lines.
                    if(self.countLinesSurroundingCell(r, c, Grid.LINE_KEYS['LINE'])==int(val)):
                        self.setLinesSurroundingCell(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])
                    elif(self.countLinesSurroundingCell(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])==4-int(val)):
                        self.setLinesSurroundingCell(r, c, Grid.LINE_KEYS['LINE'])
                    # Tricks for Ones:
                    if(val=='1'):
                        for corner in range(4):
                            # Dead end corner.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==2):
                                self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
                                self.sendLineOutThroughCorner(r, c, Grid.getOppositeCorner(corner))
                            # Line coming in.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==1 and
                              self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['LINE'])==1):
                                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])
                    # Tricks for Twos:
                    if(val=='2'):
                        for corner in range(4):
                            # Dead end corner.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==2 and
                              self.countLinesSurroundingCell(r, c, Grid.LINE_KEYS['NO_LINE'])==4):
                                self.indecisiveTwo(r, c, Grid.getOppositeCorner(corner), assumeUniqueSoln)
                            # Line coming in.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['LINE'])==1):
                                if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==1):
                                    # Definitely coming in.
                                    if(self.countCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])==1):
                                        self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])
                                    elif(self.countCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])==1):
                                        self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])
                                    self.sendLineOutThroughCorner(r, c, Grid.getOppositeCorner(corner))
                                elif(self.countCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['NOT_ALLOWED'])==1):
                                    # Possibly coming in, but there is a 'NOT_ALLOWED' on the opposite corner.
                                    self.setCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
                                else:
                                    # Check if a line is coming in from the other end.
                                    rx = r
                                    cx = c
                                    while(True):
                                        if(self.countCornerLinesOuter(rx, cx, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])==1):
                                            self.setCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
                                            break
                                        # Move into next cell.
                                        rx = rx + self.CELL_POS_OVER_CORNER[corner]['row']
                                        cx = cx + self.CELL_POS_OVER_CORNER[corner]['col']
                                        if(self.getCellVal(rx, cx)!='2'):
                                            break
                            # Check if this two can face away from the opposite corner. Only do this check if we can use it (needs a 'not allowed')
                            if(self.countCornerLinesInner(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==1):
                                if(self.cornerCounterProof(r, c, Grid.getOppositeCorner(corner))):
                                    self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])
                    # Tricks for Threes:
                    if(val=='3'):
                        for corner in range(4):
                            # Dead end corner.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])==2):
                                self.setCornerLinesInner(r, c, corner, Grid.LINE_KEYS['LINE'])
                                self.sendLineOutThroughCorner(r, c, Grid.getOppositeCorner(corner))
                            # Line coming in.
                            if(self.countCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['LINE'])==1):
                                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])
                                self.setCornerLinesOuter(r, c, corner, Grid.LINE_KEYS['NOT_ALLOWED'])
                            # Corner counterproof
                            if(self.cornerCounterProof(r, c, corner)):
                                self.setCornerLinesInner(r, c, Grid.getOppositeCorner(corner), Grid.LINE_KEYS['LINE'])
                        # Threes side by side.
                        if(self.getCellVal(r-1, c)=='3' or self.getCellVal(r+1, c)=='3'):
                            self.setLineVal(r, c, False, Grid.LINE_KEYS['LINE'], False)
                            self.setLineVal(r+1, c, False, Grid.LINE_KEYS['LINE'], False)
                            self.setLineVal(r+1*(self.getCellVal(r+1, c)=='3'), c-1, False, Grid.LINE_KEYS['NOT_ALLOWED'], False)
                            self.setLineVal(r+1*(self.getCellVal(r+1, c)=='3'), c+1, False, Grid.LINE_KEYS['NOT_ALLOWED'], False)
                        elif(self.getCellVal(r, c-1)=='3' or self.getCellVal(r, c+1)=='3'):
                            self.setLineVal(r, c, True, Grid.LINE_KEYS['LINE'], False)
                            self.setLineVal(r, c+1, True, Grid.LINE_KEYS['LINE'], False)
                            self.setLineVal(r-1, c+1*(self.getCellVal(r, c+1)=='3'), True, Grid.LINE_KEYS['NOT_ALLOWED'], False)
                            self.setLineVal(r+1, c+1*(self.getCellVal(r, c+1)=='3'), True, Grid.LINE_KEYS['NOT_ALLOWED'], False)
        print('%i unresolved numbers remaining' % numUnresolvesNumbers)

        # Iterate over every dot and see if there are any cases where
        # some of the lines surrounding a dot can be determined.
        for r in range(self.ROWS+1):
            for c in range(self.COLS+1):
                # Dead end.
                if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])==3):
                    self.setLinesSurroundingDot(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])
                # Only one valid direction for line to go.
                if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['LINE'])==1):
                    if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])==2):
                        self.setLinesSurroundingDot(r, c, Grid.LINE_KEYS['LINE'])
                # Line already passing through, mark other two edges as impassable.
                if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['LINE'])==2):
                    self.setLinesSurroundingDot(r, c, Grid.LINE_KEYS['NOT_ALLOWED'])

        # Iterate over every dot and see if there are any mini loops forming that
        # can be resolved. (But first count how many loose ends we have!)
        numLooseEnds = 0
        for r in range(self.ROWS+1):
            for c in range(self.COLS+1):
                if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['LINE'])==1):
                    numLooseEnds += 1
        if(numLooseEnds>2):
            for r in range(self.ROWS+1):
                for c in range(self.COLS+1):
                    if(self.countLinesSurroundingDot(r, c, Grid.LINE_KEYS['LINE'])==1):
                        [rx, cx] = self.findOtherEnd(r, c, -1)
                        # TODO: Make this part more sophisticated (atm only checks for adjacent ends)
                        if(r==rx and abs(c-cx)==1):
                            self.setLineVal(r, c-1*(cx<c), False, Grid.LINE_KEYS['NOT_ALLOWED'], False)
                        if(c==cx and abs(r-rx)==1):
                            self.setLineVal(r-1*(rx<r), c, True, Grid.LINE_KEYS['NOT_ALLOWED'], False)


    def __init__(self, puzzle, bgcol='white', fgcol='black'):
        # Set up some constants.
        self.PUZZLE = [list(line.replace('\n','')) for line in open(puzzle)]
        self.ROWS = len(self.PUZZLE)
        self.COLS = len(self.PUZZLE[0])
        self.FGCOL = fgcol
        self.BGCOL = bgcol

        # Make a duplicate of the puzzle. Here we will remove cell values once their rule is satisfied.
        self.cells = list(self.PUZZLE)
        # Set up two 2D arrays that will record whether or not a line is there (or whether one can go there)
        self.vlines = [[Grid.LINE_KEYS['NO_LINE'] for _ in range(self.COLS+1)] for _ in range(self.ROWS+1)]
        self.hlines = [[Grid.LINE_KEYS['NO_LINE'] for _ in range(self.COLS+1)] for _ in range(self.ROWS+1)]
        # Set up pointer arrays to link the above line data to the corresponding labels.
        self.vlinelabels = [[None for _ in range(self.COLS+1)] for _ in range(self.ROWS+1)]
        self.hlinelabels = [[None for _ in range(self.COLS+1)] for _ in range(self.ROWS+1)]

        self.root = tk.Tk()
        self.root.configure(bg=bgcol)
        self.root.title("Slitherlink")

        # Set initial windowsize s.t. cells are all square.
        self.root.geometry(str(self.COLS*30) + 'x' + str(self.ROWS*30))

        # Initialise grid with dots, default values and blank edges.
        for r in range(2 * self.ROWS + 1):
            for c in range(2 * self.COLS + 1):
                if(r%2==1 and c%2==1): # Boxes w/ numbers
                    tk.Label(self.root, font=('arial', 18), text=self.PUZZLE[r//2][c//2], borderwidth=5, bg=bgcol).grid(row=r, column=c,sticky='nsew')
                elif(r%2==0 and c%2==0): # Dots between boxes (always static)
                    tk.Label(self.root, font=('arial',1), borderwidth=0, bg=fgcol).grid(row=r, column=c,sticky='nsew')
                else: # Lines between boxes ()
                    lbl = tk.Label(self.root, font=('arial',5), text='   ', borderwidth=0, bg=bgcol)
                    lbl.grid(row=r, column=c,sticky='nsew')
                    if(r%2==1):
                        self.vlinelabels[r//2][c//2] = lbl
                    else:
                        self.hlinelabels[r//2][c//2] = lbl

        # Ensure columns and rows resize themselves when window is resized, but make boxes resize at 20x the rate of dots.
        for r in range(2 * self.ROWS + 1):
            tk.Grid.rowconfigure(self.root,r,weight=r%2*19+1)
        for c in range(2 * self.COLS + 1):
            tk.Grid.columnconfigure(self.root,c,weight=c%2*19+1)

        # Add key event(s)
        def mouseClick(event):
            self.solve()
        self.root.bind("<Button-1>", mouseClick)

        # Draw it!
        self.root.mainloop()

'''DRIVER'''
if __name__ == '__main__':
    _ = Grid(puzzle='Puzzles/p6.txt')
